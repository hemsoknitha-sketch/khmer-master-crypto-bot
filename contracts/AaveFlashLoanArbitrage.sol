// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AaveFlashLoanArbitrage
 * @dev Institutional Flash Loan & Multi-DEX Arbitrage Engine on Arbitrum One (Aave V3)
 * -----------------------------------------------------------------------------------
 * Atomic Invariant:
 * 1. Borrows asset (USDT/USDC/WETH) from Aave V3 Pool via flashLoanSimple.
 * 2. Swaps on primary DEX (e.g. Uniswap V3).
 * 3. Swaps back on secondary DEX (e.g. Camelot / SushiSwap).
 * 4. Repays Aave loan + 0.05% fee in the exact same block.
 * 5. Requires netProfit >= minProfit specified by caller. Reverts atomically if unprofitable.
 * 6. Transfers 100% net profit directly to user's recipient wallet!
 */

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}

library SafeERC20 {
    function safeTransfer(IERC20 token, address to, uint256 value) internal {
        require(token.transfer(to, value), "SafeERC20: transfer failed");
    }
    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        require(token.transferFrom(from, to, value), "SafeERC20: transferFrom failed");
    }
    function safeApprove(IERC20 token, address spender, uint256 value) internal {
        require(token.approve(spender, value), "SafeERC20: approve failed");
    }
}

interface IPoolAddressesProvider {
    function getPool() external view returns (address);
}

interface IPool {
    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

interface IFlashLoanSimpleReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool);
}

interface ISwapRouter {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut);
}

interface ICamelotRouter {
    function swapExactTokensForTokensSupportingFeeOnTransferTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        address referrer,
        uint256 deadline
    ) external;
    function getAmountsOut(uint256 amountIn, address[] calldata path) external view returns (uint256[] memory amounts);
}

contract AaveFlashLoanArbitrage is IFlashLoanSimpleReceiver {
    using SafeERC20 for IERC20;

    address public immutable owner;
    IPoolAddressesProvider public immutable ADDRESSES_PROVIDER;
    IPool public immutable POOL;

    ISwapRouter public immutable uniswapRouter;
    ICamelotRouter public immutable camelotRouter;

    // Execution authorization
    mapping(address => bool) public authorizedCallers;

    event FlashLoanExecuted(
        address indexed asset,
        uint256 amountBorrowed,
        uint256 premiumPaid,
        uint256 netProfit,
        address indexed recipient
    );

    event CallerAuthorizationChanged(address indexed caller, bool status);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner authorized");
        _;
    }

    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedCallers[msg.sender], "Caller not authorized");
        _;
    }

    /**
     * @notice Constructor initializes Aave V3 and DEX Routers on Arbitrum One
     * Default Arbitrum Addresses:
     *   _addressProvider: 0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb (Aave V3 Arbitrum)
     *   _uniswapRouter:   0xE592427A0AEce92De3Edee1F18E0157C05861564 (Uniswap V3 SwapRouter)
     *   _camelotRouter:   0xc873fEcbd354f5A56E00E710B90EF4201db2448d (Camelot Router V2)
     */
    constructor(
        address _addressProvider,
        address _uniswapRouter,
        address _camelotRouter
    ) {
        owner = msg.sender;
        ADDRESSES_PROVIDER = IPoolAddressesProvider(_addressProvider);
        POOL = IPool(IPoolAddressesProvider(_addressProvider).getPool());
        uniswapRouter = ISwapRouter(_uniswapRouter);
        camelotRouter = ICamelotRouter(_camelotRouter);
        authorizedCallers[msg.sender] = true;
    }

    function setCallerAuthorization(address _caller, bool _status) external onlyOwner {
        authorizedCallers[_caller] = _status;
        emit CallerAuthorizationChanged(_caller, _status);
    }

    /**
     * @notice Entry point for Keeper Relayer to trigger an on-chain flash loan arbitrage.
     * @param asset The borrowed token address (e.g. USDT, USDC, WETH)
     * @param amount Loan amount (e.g. 50,000 USDT)
     * @param params ABI-encoded parameters: (address intermediateToken, uint24 poolFee, uint256 minProfit, address recipient, uint8 dexRoute)
     */
    function requestFlashLoan(
        address asset,
        uint256 amount,
        bytes calldata params
    ) external onlyAuthorized {
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            params,
            0
        );
    }

    /**
     * @notice Callback invoked by Aave V3 Pool with borrowed funds.
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Callback caller must be Aave Pool");
        require(initiator == address(this), "Initiator must be this contract");

        // Decode execution parameters
        (
            address intermediateToken,
            uint24 poolFee,
            uint256 minProfit,
            address recipient,
            uint8 dexRoute
        ) = abi.decode(params, (address, uint24, uint256, address, uint8));

        uint256 totalRepay = amount + premium;

        // Execute Multi-DEX Arbitrage Path
        if (dexRoute == 1) {
            // Path 1: Uniswap V3 (Buy intermediate) -> Camelot (Sell back to asset)
            _swapUniswapV3(asset, intermediateToken, poolFee, amount);
            uint256 intermBalance = IERC20(intermediateToken).balanceOf(address(this));
            _swapCamelot(intermediateToken, asset, intermBalance);
        } else {
            // Path 2: Camelot (Buy intermediate) -> Uniswap V3 (Sell back to asset)
            _swapCamelot(asset, intermediateToken, amount);
            uint256 intermBalance = IERC20(intermediateToken).balanceOf(address(this));
            _swapUniswapV3(intermediateToken, asset, poolFee, intermBalance);
        }

        // Verify balance after arbitrage
        uint256 finalAssetBalance = IERC20(asset).balanceOf(address(this));
        require(finalAssetBalance >= totalRepay, "Arbitrage did not cover loan + premium: Reverting");

        uint256 netProfit = finalAssetBalance - totalRepay;
        require(netProfit >= minProfit, "Net profit below minimum hurdle: Reverting to protect capital");

        // Approve Aave Pool to withdraw repayment
        IERC20(asset).safeApprove(address(POOL), totalRepay);

        // Transfer 100% net profit directly to user recipient wallet!
        if (netProfit > 0 && recipient != address(0)) {
            IERC20(asset).safeTransfer(recipient, netProfit);
        }

        emit FlashLoanExecuted(asset, amount, premium, netProfit, recipient);
        return true;
    }

    function _swapUniswapV3(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn
    ) internal returns (uint256) {
        IERC20(tokenIn).safeApprove(address(uniswapRouter), amountIn);
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            fee: fee,
            recipient: address(this),
            deadline: block.timestamp + 300,
            amountIn: amountIn,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });
        return uniswapRouter.exactInputSingle(params);
    }

    function _swapCamelot(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) internal {
        IERC20(tokenIn).safeApprove(address(camelotRouter), amountIn);
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;

        camelotRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amountIn,
            0,
            path,
            address(this),
            address(0),
            block.timestamp + 300
        );
    }

    /**
     * @notice Emergency withdrawal in case of stuck tokens (onlyOwner)
     */
    function rescueTokens(address token, uint256 amount, address to) external onlyOwner {
        IERC20(token).safeTransfer(to, amount);
    }

    function withdrawETH(address payable to) external onlyOwner {
        to.transfer(address(this).balance);
    }

    receive() external payable {}
}
