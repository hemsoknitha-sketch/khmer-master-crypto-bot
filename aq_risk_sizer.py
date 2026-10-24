# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CENTRAL INSTITUTIONAL RISK SIZER
Module: aq_risk_sizer.py
Author: Angkor Quant Institutional Infrastructure
Standard: The 84 Pillars and Invariants 34, 35, 52, 74, 76, 82
Zero-Coercion Admissibility and Discrete Risk Quantization Engine
"""

from dataclasses import dataclass
from enum import Enum
import math
import operator
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger("CentralRiskSizer")


class RiskSizingStatus(Enum):
    APPROVED = "APPROVED"
    REJECTED_CAPITAL_DEFICIT = "REJECTED_CAPITAL_DEFICIT"
    REJECTED_INVALID_PRICE_GEOMETRY = "REJECTED_INVALID_PRICE_GEOMETRY"
    REJECTED_BELOW_MINIMUM_LOT = "REJECTED_BELOW_MINIMUM_LOT"
    REJECTED_PORTFOLIO_HEAT_LIMIT = "REJECTED_PORTFOLIO_HEAT_LIMIT"


@dataclass(frozen=True)
class RiskSizingDecision:
    status: RiskSizingStatus
    is_admissible: bool
    allocated_lot: float
    monetary_risk_amount: float
    effective_risk_percentage: float
    rejection_reason: Optional[str] = None


class CentralRiskSizer:
    MAX_RISK_OVERRUN_RATIO = 1.25

    def __init__(self, risk_budget_tolerance_ratio: float = 0.0) -> None:
        self.risk_budget_tolerance_ratio = risk_budget_tolerance_ratio
        self._stats = {
            "total_evaluations": 0,
            "approved_trades": 0,
            "rejected_trades": 0,
        }

    def calculate_admissible_lot(
        self,
        account_equity: float,
        target_risk_fraction: float,
        entry_price: float,
        stop_loss_price: float,
        contract_multiplier: float,
        min_deal_lot: float,
        lot_step: float,
        max_lot_limit: float,
        current_portfolio_heat: float = 0.0,
        max_portfolio_heat: float = 0.06,
    ) -> RiskSizingDecision:
        self._stats["total_evaluations"] += 1

        if account_equity <= 0.0 or target_risk_fraction <= 0.0:
            self._stats["rejected_trades"] += 1
            return RiskSizingDecision(
                status=RiskSizingStatus.REJECTED_CAPITAL_DEFICIT,
                is_admissible=False,
                allocated_lot=0.0,
                monetary_risk_amount=0.0,
                effective_risk_percentage=0.0,
                rejection_reason="Account equity or risk fraction non-positive.",
            )

        if current_portfolio_heat >= max_portfolio_heat:
            self._stats["rejected_trades"] += 1
            return RiskSizingDecision(
                status=RiskSizingStatus.REJECTED_PORTFOLIO_HEAT_LIMIT,
                is_admissible=False,
                allocated_lot=0.0,
                monetary_risk_amount=0.0,
                effective_risk_percentage=0.0,
                rejection_reason="Portfolio aggregate heat limit reached.",
            )

        price_delta = abs(operator.sub(entry_price, stop_loss_price))
        if price_delta <= 1e-8 or contract_multiplier <= 0.0:
            self._stats["rejected_trades"] += 1
            return RiskSizingDecision(
                status=RiskSizingStatus.REJECTED_INVALID_PRICE_GEOMETRY,
                is_admissible=False,
                allocated_lot=0.0,
                monetary_risk_amount=0.0,
                effective_risk_percentage=0.0,
                rejection_reason="Price delta or contract multiplier zero or invalid.",
            )

        risk_capital_budget = operator.mul(account_equity, target_risk_fraction)
        unit_risk_exposure = operator.mul(price_delta, contract_multiplier)
        raw_lot = risk_capital_budget / unit_risk_exposure

        step_precision = max(0, -int(math.floor(math.log10(lot_step)))) if lot_step < 1.0 else 0
        step_multiplier = 1.0 / lot_step
        quantized_steps = math.floor(operator.mul(raw_lot, step_multiplier))
        quantized_lot = round(quantized_steps / step_multiplier, step_precision)

        if quantized_lot < min_deal_lot:
            min_lot_monetary_risk = operator.mul(
                min_deal_lot, operator.mul(price_delta, contract_multiplier)
            )
            max_tolerated_risk = operator.mul(
                risk_capital_budget, operator.add(1.0, self.risk_budget_tolerance_ratio)
            )

            if min_lot_monetary_risk > max_tolerated_risk:
                self._stats["rejected_trades"] += 1
                rejection_message = (
                    f"Required min lot {min_deal_lot} generates monetary risk {min_lot_monetary_risk:.2f}, "
                    f"exceeding budget {risk_capital_budget:.2f}."
                )
                return RiskSizingDecision(
                    status=RiskSizingStatus.REJECTED_BELOW_MINIMUM_LOT,
                    is_admissible=False,
                    allocated_lot=0.0,
                    monetary_risk_amount=min_lot_monetary_risk,
                    effective_risk_percentage=min_lot_monetary_risk / account_equity,
                    rejection_reason=rejection_message,
                )
            quantized_lot = min_deal_lot

        final_lot = min(quantized_lot, max_lot_limit)
        calculated_monetary_risk = operator.mul(
            final_lot, operator.mul(price_delta, contract_multiplier)
        )
        calculated_risk_percentage = calculated_monetary_risk / account_equity

        self._stats["approved_trades"] += 1
        return RiskSizingDecision(
            status=RiskSizingStatus.APPROVED,
            is_admissible=True,
            allocated_lot=final_lot,
            monetary_risk_amount=calculated_monetary_risk,
            effective_risk_percentage=calculated_risk_percentage,
            rejection_reason=None,
        )

    def get_telemetry(self) -> Dict[str, Any]:
        return dict(self._stats)
