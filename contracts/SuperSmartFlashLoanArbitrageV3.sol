// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SuperSmartFlashLoanArbitrageV3
 * @dev Institutional Multi-DEX Flash Loan & Aave V3 Native Liquidation Arbitrage Suite (Arbitrum One)
 * -----------------------------------------------------------------------------------
 * Resolves the 5 Hard Engineering Bottlenecks:
 *   1. Zero-Fee Flash Loans via Balancer V2 Vault (0.00% fee vs Aave 0.05%)
 *   2. Native Aave V3 Liquidation Bounty Extraction (liquidationCall with 5%-10% protocol bonus)
 *   3. Expanded Multi-DEX Routing: Uniswap V3, Camelot V2/V3, SushiSwap V3
 *   4. Ultra-Low Fee Tiers (1 bps / 5 bps) for Stablecoin & Correlated Peg Arbitrage
 *   5. Single-Block EVM Atomic Invariant (require(finalBalance >= totalRepay + minProfit))
 *      Guaranteeing 0.00% principal risk.
 * -----------------------------------------------------------------------------------
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

// ----------------------------------------------------------------------
// AAVE V3 INTERFACES
// ----------------------------------------------------------------------
interface IPoolAddressesProvider {
    function getPool() external view returns (address);
}

interface IAavePool {
    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;

    function liquidationCall(
        address collateralAsset,
        address debtAsset,
        address user,
        uint256 debtToCover,
        bool receiveAToken
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

// ----------------------------------------------------------------------
// BALANCER V2 VAULT INTERFACES (0.00% FEE FLASH LOANS)
// ----------------------------------------------------------------------
interface IBalancerVault {
    function flashLoan(
        address recipient,
        IERC20[] memory tokens,
        uint256[] memory amounts,
        bytes memory userData
    ) external;
}

interface IFlashLoanRecipient {
    function receiveFlashLoan(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory userData
    ) external;
}

// ----------------------------------------------------------------------
// DEX ROUTER INTERFACES
// ----------------------------------------------------------------------
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

    function getAmountsOut(uint256 amountIn, address[] calldata path)
        external
        view
        returns (uint256[] memory amounts);
}

interface ISushiSwapV3Router {
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

// ----------------------------------------------------------------------
// MAIN SMART CONTRACT V3
// ----------------------------------------------------------------------
contract SuperSmartFlashLoanArbitrageV3 is IFlashLoanSimpleReceiver, IFlashLoanRecipient {
    using SafeERC20 for IERC20;

    address public immutable owner;
    IPoolAddressesProvider public immutable ADDRESSES_PROVIDER;
    IAavePool public immutable AAVE_POOL;
    IBalancerVault public immutable BALANCER_VAULT;

    ISwapRouter public immutable uniswapRouter;
    ICamelotRouter public immutable camelotRouter;
    ISushiSwapV3Router public immutable sushiSwapRouter;

    mapping(address => bool) public authorizedCallers;

    enum OperationType {
        CYCLIC_ARBITRAGE,
        AAVE_LIQUIDATION
    }

    struct ArbitrageExecutionParams {
        address intermediateToken;
        uint24 poolFee;
        uint256 minProfit;
        address recipient;
        uint8 dexRoute; // 1: Uni->Camelot, 2: Camelot->Uni, 3: Uni->Sushi, 4: Sushi->Uni
    }

    struct LiquidationExecutionParams {
        address collateralAsset;
        address userToLiquidate;
        uint256 debtToCover;
        uint256 minProfit;
        address recipient;
        uint8 dexRoute; // 1: Uni V3, 2: Camelot V2, 3: Sushi V3
        uint24 poolFee; // fee tier for collateral -> debt swap (e.g. 500 = 0.05%, 3000 = 0.30%)
    }

    struct CallbackPayload {
        uint8 opType; // 0: CYCLIC_ARBITRAGE, 1: AAVE_LIQUIDATION
        bytes innerData;
    }

    event FlashLoanExecuted(
        string indexed provider,
        address indexed asset,
        uint256 amountBorrowed,
        uint256 premiumPaid,
        uint256 netProfit,
        address indexed recipient
    );

    event LiquidationExecuted(
        string indexed provider,
        address indexed borrower,
        address collateralAsset,
        address debtAsset,
        uint256 debtCovered,
        uint256 collateralReceived,
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
     * @notice Constructor initializes Arbitrum One Lending Pools & DEX Routers
     * Default Arbitrum Addresses:
     *   _addressProvider: 0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb (Aave V3)
     *   _balancerVault:   0xBA12222222228d8Ba445958a75a0704d566BF2C8 (Balancer V2 Vault 0% fee)
     *   _uniswapRouter:   0xE592427A0AEce92De3Edee1F18E0157C05861564 (Uniswap V3)
     *   _camelotRouter:   0xc873fEcbd354f5A56E00E710B90EF4201db2448d (Camelot V2)
     *   _sushiRouter:     0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506 (SushiSwap V3)
     */
    constructor(
        address _addressProvider,
        address _balancerVault,
        address _uniswapRouter,
        address _camelotRouter,
        address _sushiRouter
    ) {
        owner = msg.sender;
        ADDRESSES_PROVIDER = IPoolAddressesProvider(_addressProvider);
        AAVE_POOL = IAavePool(IPoolAddressesProvider(_addressProvider).getPool());
        BALANCER_VAULT = IBalancerVault(_balancerVault);

        uniswapRouter = ISwapRouter(_uniswapRouter);
        camelotRouter = ICamelotRouter(_camelotRouter);
        sushiSwapRouter = ISushiSwapV3Router(_sushiRouter);

        authorizedCallers[msg.sender] = true;
    }

    function setCallerAuthorization(address _caller, bool _status) external onlyOwner {
        authorizedCallers[_caller] = _status;
        emit CallerAuthorizationChanged(_caller, _status);
    }

    // ----------------------------------------------------------------------
    // 1. TRIGGER BALANCER 0.00% FEE FLASH LOAN (PRIORITY 1)
    // ----------------------------------------------------------------------
    function requestBalancerFlashLoan(
        address asset,
        uint256 amount,
        bytes calldata params
    ) external onlyAuthorized {
        IERC20[] memory tokens = new IERC20[](1);
        tokens[0] = IERC20(asset);

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;

        CallbackPayload memory payload = CallbackPayload({
            opType: uint8(OperationType.CYCLIC_ARBITRAGE),
            innerData: params
        });

        BALANCER_VAULT.flashLoan(address(this), tokens, amounts, abi.encode(payload));
    }

    // ----------------------------------------------------------------------
    // 2. TRIGGER AAVE V3 FLASH LOAN (PRIORITY 2 FALLBACK)
    // ----------------------------------------------------------------------
    function requestFlashLoan(
        address asset,
        uint256 amount,
        bytes calldata params
    ) external onlyAuthorized {
        CallbackPayload memory payload = CallbackPayload({
            opType: uint8(OperationType.CYCLIC_ARBITRAGE),
            innerData: params
        });

        AAVE_POOL.flashLoanSimple(address(this), asset, amount, abi.encode(payload), 0);
    }

    // ----------------------------------------------------------------------
    // 3. TRIGGER FLASH LIQUIDATION (AAVE V3 UNDERWATER ACCOUNTS)
    // ----------------------------------------------------------------------
    function requestFlashLiquidation(
        address debtAsset,
        uint256 debtAmount,
        bytes calldata params,
        bool useBalancer
    ) external onlyAuthorized {
        CallbackPayload memory payload = CallbackPayload({
            opType: uint8(OperationType.AAVE_LIQUIDATION),
            innerData: params
        });

        bytes memory encodedPayload = abi.encode(payload);

        if (useBalancer) {
            IERC20[] memory tokens = new IERC20[](1);
            tokens[0] = IERC20(debtAsset);
            uint256[] memory amounts = new uint256[](1);
            amounts[0] = debtAmount;
            BALANCER_VAULT.flashLoan(address(this), tokens, amounts, encodedPayload);
        } else {
            AAVE_POOL.flashLoanSimple(address(this), debtAsset, debtAmount, encodedPayload, 0);
        }
    }

    // ----------------------------------------------------------------------
    // BALANCER CALLBACK (0% FEE)
    // ----------------------------------------------------------------------
    function receiveFlashLoan(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory userData
    ) external override {
        require(msg.sender == address(BALANCER_VAULT), "Caller must be Balancer Vault");

        address asset = address(tokens[0]);
        uint256 amount = amounts[0];
        uint256 fee = feeAmounts[0]; // 0% on Arbitrum One!

        _dispatchOperation(asset, amount, fee, userData, "BALANCER_0%_FEE");

        // Repay loan
        IERC20(asset).safeTransfer(address(BALANCER_VAULT), amount + fee);
    }

    // ----------------------------------------------------------------------
    // AAVE V3 CALLBACK (0.05% FEE)
    // ----------------------------------------------------------------------
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(AAVE_POOL), "Caller must be Aave Pool");
        require(initiator == address(this), "Initiator must be this contract");

        _dispatchOperation(asset, amount, premium, params, "AAVE_V3");

        // Approve repayment to Aave Pool
        uint256 totalRepay = amount + premium;
        IERC20(asset).safeApprove(address(AAVE_POOL), totalRepay);
        return true;
    }

    // ----------------------------------------------------------------------
    // DISPATCHER: ARBITRAGE VS LIQUIDATION
    // ----------------------------------------------------------------------
    function _dispatchOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        bytes memory rawData,
        string memory providerName
    ) internal {
        if (rawData.length >= 64) {
            try this.decodePayload(rawData) returns (CallbackPayload memory payload) {
                if (payload.opType == uint8(OperationType.AAVE_LIQUIDATION)) {
                    _executeLiquidationLogic(asset, amount, premium, payload.innerData, providerName);
                    return;
                } else {
                    _executeArbitrageLogic(asset, amount, premium, payload.innerData, providerName);
                    return;
                }
            } catch {
                _executeArbitrageLogic(asset, amount, premium, rawData, providerName);
                return;
            }
        } else {
            _executeArbitrageLogic(asset, amount, premium, rawData, providerName);
        }
    }

    function decodePayload(bytes memory data) external pure returns (CallbackPayload memory) {
        return abi.decode(data, (CallbackPayload));
    }

    // ----------------------------------------------------------------------
    // INTERNAL MULTI-DEX CYCLIC ARBITRAGE ENGINE
    // ----------------------------------------------------------------------
    function _executeArbitrageLogic(
        address asset,
        uint256 amount,
        uint256 premium,
        bytes memory params,
        string memory providerName
    ) internal {
        ArbitrageExecutionParams memory p = abi.decode(params, (ArbitrageExecutionParams));

        uint256 intermediateBought = 0;
        uint256 finalAssetReceived = 0;

        // Leg 1: Swap borrowed asset -> intermediateToken
        if (p.dexRoute == 1 || p.dexRoute == 3) {
            IERC20(asset).safeApprove(address(uniswapRouter), amount);
            intermediateBought = uniswapRouter.exactInputSingle(ISwapRouter.ExactInputSingleParams({
                tokenIn: asset,
                tokenOut: p.intermediateToken,
                fee: p.poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: amount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        } else if (p.dexRoute == 2) {
            IERC20(asset).safeApprove(address(camelotRouter), amount);
            address[] memory path = new address[](2);
            path[0] = asset;
            path[1] = p.intermediateToken;

            uint256 balBefore = IERC20(p.intermediateToken).balanceOf(address(this));
            camelotRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
                amount,
                0,
                path,
                address(this),
                address(0),
                block.timestamp + 120
            );
            intermediateBought = IERC20(p.intermediateToken).balanceOf(address(this)) - balBefore;
        } else if (p.dexRoute == 4) {
            IERC20(asset).safeApprove(address(sushiSwapRouter), amount);
            intermediateBought = sushiSwapRouter.exactInputSingle(ISushiSwapV3Router.ExactInputSingleParams({
                tokenIn: asset,
                tokenOut: p.intermediateToken,
                fee: p.poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: amount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        }

        require(intermediateBought > 0, "Leg 1 swap returned 0 tokens");

        // Leg 2: Swap intermediateToken back -> original asset
        if (p.dexRoute == 1) {
            IERC20(p.intermediateToken).safeApprove(address(camelotRouter), intermediateBought);
            address[] memory path = new address[](2);
            path[0] = p.intermediateToken;
            path[1] = asset;

            uint256 balBefore = IERC20(asset).balanceOf(address(this));
            camelotRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
                intermediateBought,
                0,
                path,
                address(this),
                address(0),
                block.timestamp + 120
            );
            finalAssetReceived = IERC20(asset).balanceOf(address(this)) - balBefore;
        } else if (p.dexRoute == 2) {
            IERC20(p.intermediateToken).safeApprove(address(uniswapRouter), intermediateBought);
            finalAssetReceived = uniswapRouter.exactInputSingle(ISwapRouter.ExactInputSingleParams({
                tokenIn: p.intermediateToken,
                tokenOut: asset,
                fee: p.poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: intermediateBought,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        } else if (p.dexRoute == 3) {
            IERC20(p.intermediateToken).safeApprove(address(sushiSwapRouter), intermediateBought);
            finalAssetReceived = sushiSwapRouter.exactInputSingle(ISushiSwapV3Router.ExactInputSingleParams({
                tokenIn: p.intermediateToken,
                tokenOut: asset,
                fee: p.poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: intermediateBought,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        } else if (p.dexRoute == 4) {
            IERC20(p.intermediateToken).safeApprove(address(uniswapRouter), intermediateBought);
            finalAssetReceived = uniswapRouter.exactInputSingle(ISwapRouter.ExactInputSingleParams({
                tokenIn: p.intermediateToken,
                tokenOut: asset,
                fee: p.poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: intermediateBought,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        }

        // ATOMIC INVARIANT REVERT SAFETY CHECK
        uint256 totalRepay = amount + premium;
        require(finalAssetReceived >= totalRepay, "Arbitrage did not cover loan + premium");

        uint256 netProfit = finalAssetReceived - totalRepay;
        require(netProfit >= p.minProfit, "Net profit below minimum hurdle");

        address recipient = p.recipient == address(0) ? owner : p.recipient;
        IERC20(asset).safeTransfer(recipient, netProfit);

        emit FlashLoanExecuted(providerName, asset, amount, premium, netProfit, recipient);
    }

    // ----------------------------------------------------------------------
    // COLLATERAL SWAP HELPER (AVOIDS STACK TOO DEEP)
    // ----------------------------------------------------------------------
    function _swapCollateralToDebt(
        address collateralAsset,
        address debtAsset,
        uint256 collateralAmount,
        uint8 dexRoute,
        uint24 poolFee
    ) internal returns (uint256) {
        if (dexRoute == 1) {
            // Uniswap V3
            IERC20(collateralAsset).safeApprove(address(uniswapRouter), collateralAmount);
            return uniswapRouter.exactInputSingle(ISwapRouter.ExactInputSingleParams({
                tokenIn: collateralAsset,
                tokenOut: debtAsset,
                fee: poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: collateralAmount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        } else if (dexRoute == 2) {
            // Camelot V2
            IERC20(collateralAsset).safeApprove(address(camelotRouter), collateralAmount);
            address[] memory path = new address[](2);
            path[0] = collateralAsset;
            path[1] = debtAsset;

            uint256 balBefore = IERC20(debtAsset).balanceOf(address(this));
            camelotRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
                collateralAmount,
                0,
                path,
                address(this),
                address(0),
                block.timestamp + 120
            );
            return IERC20(debtAsset).balanceOf(address(this)) - balBefore;
        } else {
            // SushiSwap V3
            IERC20(collateralAsset).safeApprove(address(sushiSwapRouter), collateralAmount);
            return sushiSwapRouter.exactInputSingle(ISushiSwapV3Router.ExactInputSingleParams({
                tokenIn: collateralAsset,
                tokenOut: debtAsset,
                fee: poolFee,
                recipient: address(this),
                deadline: block.timestamp + 120,
                amountIn: collateralAmount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            }));
        }
    }

    // ----------------------------------------------------------------------
    // INTERNAL AAVE V3 LIQUIDATION EXECUTION ENGINE
    // ----------------------------------------------------------------------
    function _executeLiquidationLogic(
        address debtAsset,
        uint256 debtAmount,
        uint256 premium,
        bytes memory params,
        string memory providerName
    ) internal {
        LiquidationExecutionParams memory p = abi.decode(params, (LiquidationExecutionParams));

        // 1. Approve & Liquidate in isolated scope to free stack slots
        uint256 collateralReceived;
        {
            IERC20(debtAsset).safeApprove(address(AAVE_POOL), p.debtToCover);
            uint256 colBalBefore = IERC20(p.collateralAsset).balanceOf(address(this));
            AAVE_POOL.liquidationCall(
                p.collateralAsset,
                debtAsset,
                p.userToLiquidate,
                p.debtToCover,
                false
            );
            collateralReceived = IERC20(p.collateralAsset).balanceOf(address(this)) - colBalBefore;
            require(collateralReceived > 0, "Liquidation yielded 0 collateral");
        }

        // 2. Swap seized collateral back into debtAsset on DEX via helper function
        uint256 debtAssetReceived = _swapCollateralToDebt(
            p.collateralAsset,
            debtAsset,
            collateralReceived,
            p.dexRoute,
            p.poolFee
        );

        // 3. ATOMIC INVARIANT REVERT SAFETY CHECK:
        uint256 totalRepay = debtAmount + premium;
        require(debtAssetReceived >= totalRepay, "Liquidation did not cover loan + premium");

        uint256 netProfit = debtAssetReceived - totalRepay;
        require(netProfit >= p.minProfit, "Net liquidation bonus below hurdle");

        // 4. Send net liquidation bonus directly to recipient
        address recipient = p.recipient == address(0) ? owner : p.recipient;
        IERC20(debtAsset).safeTransfer(recipient, netProfit);

        emit LiquidationExecuted(
            providerName,
            p.userToLiquidate,
            p.collateralAsset,
            debtAsset,
            p.debtToCover,
            collateralReceived,
            netProfit,
            recipient
        );
    }

    // Emergency token rescue
    function rescueToken(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner, amount);
    }

    function rescueNative() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    receive() external payable {}
}
