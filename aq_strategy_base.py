# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CANONICAL STRATEGY BASE SPECIFICATION
Module: aq_strategy_base.py
Author: Angkor Quant Institutional Infrastructure
Standard: The 84 Pillars and Unified Polymorphic Strategy Lifecycle
Zero-Coercion Sizing Delegation and Dynamic Position Management
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
import operator
import pandas as pd

from aq_risk_sizer import CentralRiskSizer, RiskSizingDecision


@dataclass(frozen=True)
class SignalDecision:
    direction: Optional[str]
    raw_score: float
    calibrated_probability: float
    entry_price: float
    stop_loss_price: float
    take_profit_target: float
    metadata: Dict[str, Any]


class StrategyBase(ABC):
    def __init__(self, symbol: str, risk_sizer: CentralRiskSizer) -> None:
        self.symbol = symbol.upper().strip()
        self.risk_sizer = risk_sizer
        self.is_active = True

    @abstractmethod
    def evaluate_entry_signal(
        self,
        current_bar: pd.Series,
        historical_window: pd.DataFrame,
        macro_features: Dict[str, float]
    ) -> SignalDecision:
        """Evaluates market structure and generates a formal SignalDecision."""
        raise NotImplementedError

    def compute_position_allocation(
        self,
        account_equity: float,
        target_risk_fraction: float,
        signal: SignalDecision,
        contract_multiplier: float,
        min_deal_lot: float,
        lot_step: float,
        max_lot_limit: float,
        current_portfolio_heat: float = 0.0
    ) -> RiskSizingDecision:
        """Delegates position sizing strictly to the CentralRiskSizer without caller coercion."""
        if not signal.direction:
            return RiskSizingDecision(
                status=None,
                is_admissible=False,
                allocated_lot=0.0,
                monetary_risk_amount=0.0,
                effective_risk_percentage=0.0,
                rejection_reason="No directional trade signal present."
            )

        return self.risk_sizer.calculate_admissible_lot(
            account_equity=account_equity,
            target_risk_fraction=target_risk_fraction,
            entry_price=signal.entry_price,
            stop_loss_price=signal.stop_loss_price,
            contract_multiplier=contract_multiplier,
            min_deal_lot=min_deal_lot,
            lot_step=lot_step,
            max_lot_limit=max_lot_limit,
            current_portfolio_heat=current_portfolio_heat
        )

    def evaluate_breakeven_armor(
        self,
        direction: str,
        entry_price: float,
        current_price: float,
        spread: float
    ) -> Optional[float]:
        """Calculates fee-cleared breakeven armor level with anti-whipsaw buffer."""
        spread_clearing_floor = operator.mul(spread, 0.50)

        if direction == "BUY" and current_price > entry_price:
            return round(operator.add(entry_price, spread_clearing_floor), 4)
        elif direction == "SELL" and current_price < entry_price:
            return round(operator.sub(entry_price, spread_clearing_floor), 4)
        return None
