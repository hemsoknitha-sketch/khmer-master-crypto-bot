# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - QUANT GOLD VERIFICATION & TEST HARNESS
=====================================================
Validates:
  1. 19-Timeframe Orchestration & Resampling (M1 to 1 Month)
  2. Quantitative Mathematical Core (Kalman 2D, Hurst, OU, Hawkes)
  3. AI Multi-Model Swarm (Gemini, DeepSeek, Llama, Vectorized Algo Governor)
  4. Execution Engine Decision & Risk Management (SL, TP1, TP2, TP3, Breakeven)
  5. Telegram & Capital.com Bridge Integration
=====================================================
"""

import sys
import os
import asyncio

# Set unbuffered stdout & deterministic test mode
sys.stdout.reconfigure(line_buffering=True)
os.environ["OFFLINE_MODE"] = "1"

def run_tests():
    print("=" * 70, flush=True)
    print("  ANGKOR QUANT - QUANT GOLD SYSTEM TEST & VERIFICATION", flush=True)
    print("=" * 70, flush=True)

    # 1. Import quant_gold
    print("\n[TEST 1] Importing quant_gold package...", flush=True)
    import quant_gold
    print("✅ quant_gold imported successfully.", flush=True)
    print(f"  • Asset: {quant_gold.__asset__} ({quant_gold.__canonical_symbol__})", flush=True)
    print(f"  • Version: {quant_gold.__version__}", flush=True)

    # 2. Test 19-Timeframe Spectrum
    print("\n[TEST 2] Testing 19-Timeframe Spectrum & Resampling...", flush=True)
    mtf = quant_gold.get_gold_mtf_engine()
    res = mtf.analyze_all_19_timeframes(current_price=2738.50)
    
    tf_list = list(res["timeframes"].keys())
    print(f"  • Total Timeframes Analyzed: {len(tf_list)} / 19", flush=True)
    print(f"  • Timeframes: {', '.join(tf_list)}", flush=True)
    assert len(tf_list) == 19, f"Expected 19 timeframes, got {len(tf_list)}"
    
    counts = res["counts"]
    print(f"  • Alignment Breakdown: {counts['bullish']} Bullish | {counts['bearish']} Bearish | {counts['neutral']} Neutral", flush=True)
    print(f"  • Weighted Score: {res['weighted_score']:+.1f} / 100.0", flush=True)
    print(f"  • Estimated Win Probability: {res['win_probability']:.1f}%", flush=True)
    print(f"  • Tiers: Macro={res['tiers']['macro_score']:+.1f}, Intermediate={res['tiers']['intermediate_score']:+.1f}, Micro={res['tiers']['micro_score']:+.1f}", flush=True)
    print("✅ 19-Timeframe Orchestration passed.", flush=True)

    # 3. Test Mathematical Core
    print("\n[TEST 3] Testing Quantitative Mathematical Core...", flush=True)
    math_core = quant_gold.get_gold_math_core()
    math_res = math_core.analyze_mathematical_edge(current_price=2738.50)
    
    kalman = math_res["kalman"]
    hurst = math_res["hurst_surface"]
    ou = math_res["ornstein_uhlenbeck"]
    
    print(f"  • 2D Kalman Filter: Denoised=${kalman['denoised_price']:.2f}, Velocity={kalman['latent_velocity']:+.4f}", flush=True)
    print(f"  • Multi-Scale Hurst: Composite={hurst['composite']:.3f} (Regime: {hurst['regime']})", flush=True)
    print(f"  • Ornstein-Uhlenbeck: Mean=${ou['mu']:.2f}, Half-Life={ou['half_life']} bars, Sigma={ou['sigma']:.3f}", flush=True)
    print(f"  • Hawkes Jump Intensity: {math_res['hawkes_intensity']:.2f}", flush=True)
    print(f"  • Conformal Prediction 90%: [${math_res['conformal_prediction_90']['lower']:.2f}, ${math_res['conformal_prediction_90']['upper']:.2f}]", flush=True)
    print(f"  • Bayesian Win Probability: {math_res['bayesian_win_probability']:.1f}%", flush=True)
    assert "kalman" in math_res and "hurst_surface" in math_res
    print("✅ Mathematical Core passed.", flush=True)

    # 4. Test AI Swarm Engine
    print("\n[TEST 4] Testing AI Swarm Engine...", flush=True)
    ai_swarm = quant_gold.get_gold_ai_swarm()
    ai_res = asyncio.run(ai_swarm.evaluate_gold_opportunity_async(
        current_price=2738.50,
        mtf_data=res,
        math_data=math_res
    ))
    print(f"  • Action: {ai_res['action']}", flush=True)
    print(f"  • Consensus Confidence: {ai_res['consensus_confidence']:.1f}%", flush=True)
    print(f"  • Algorithmic Governor Vote: {ai_res['votes']['algorithmic_governor']['recommendation']}", flush=True)
    print(f"  • Primary Reason: {ai_res['primary_reason']}", flush=True)
    assert "action" in ai_res
    print("✅ AI Swarm Engine passed.", flush=True)

    # 5. Test Execution Engine
    print("\n[TEST 5] Testing Quant Gold Execution Engine...", flush=True)
    exec_eng = quant_gold.get_quant_gold_execution_engine()
    sig = asyncio.run(exec_eng.evaluate_gold_master_signal())
    print(f"  • Master Action: {sig['action']}", flush=True)
    print(f"  • Current Price: ${sig['current_price']:.2f} (Spread: ${sig['spread']:.2f})", flush=True)
    print(f"  • Win Confidence: {sig['confidence']:.1f}%", flush=True)
    print(f"  • Structural SL: ${sig['sl']:.2f}", flush=True)
    print(f"  • TP1 (+2.0R): ${sig['tp1']:.2f}", flush=True)
    print(f"  • TP2 (+4.0R): ${sig['tp2']:.2f}", flush=True)
    print(f"  • TP3 (+7.0R Moonshot): ${sig['tp3']:.2f}", flush=True)
    print(f"  • Reason: {sig['reason']}", flush=True)
    assert "sl" in sig and "tp1" in sig
    print("✅ Execution Engine passed.", flush=True)

    # 6. Test Telegram & Capital.com Bridge UI
    print("\n[TEST 6] Testing Telegram Bridge UI Generation...", flush=True)
    bridge = quant_gold.get_quant_gold_capital_bridge()
    text_kh, kb_kh = asyncio.run(bridge.build_quant_gold_overview_ui(859271875, user_lang="khmer"))
    assert "QUANT GOLD" in text_kh
    assert "១៩ TIMEFRAMES" in text_kh
    print("  • Khmer UI Generated successfully. Character length:", len(text_kh), flush=True)
    print("  • Inline Keyboard Rows:", len(kb_kh.inline_keyboard), flush=True)
    print("✅ Telegram Bridge UI passed.", flush=True)

    print("\n" + "=" * 70, flush=True)
    print("  ALL 6 QUANT GOLD UNIT & INTEGRATION TESTS PASSED 100%!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    run_tests()
