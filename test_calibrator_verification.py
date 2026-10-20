import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
import capital_probability_calibrator as cpc

def main():
    calib = cpc.CapitalProbabilityCalibrator
    verif = calib.verify_out_of_sample_calibration()
    print("======================================================================")
    print("  ANGKOR QUANT - EMPIRICAL CALIBRATION VERIFICATION REPORT")
    print("======================================================================")
    print(f"Test Sample Count:              {verif.get('test_sample_count')}")
    print(f"Naive Heuristic Brier Score:    {verif.get('naive_brier_score')}")
    print(f"Calibrated Model Brier Score:   {verif.get('calibrated_brier_score')}")
    print(f"Brier Error Reduction:          {verif.get('brier_improvement_pct')}%")
    print(f"Expected Calibration Error (ECE): {verif.get('expected_calibration_error_ece')}")
    
    v70 = verif.get('verification_70_pct_bin', {})
    print("\n----------------------------------------------------------------------")
    print("  VERIFICATION OF ~70% WIN PROBABILITY PREDICTION ON OUT-OF-SAMPLE DATA")
    print("----------------------------------------------------------------------")
    print(f"Samples in ~70% Bin (>= 65%):   {v70.get('samples_count')}")
    print(f"Mean Predicted Win Probability: {v70.get('mean_predicted_prob', 0)*100:.2f}%")
    print(f"Empirical Realized Win Rate:    {v70.get('actual_realized_win_rate', 0)*100:.2f}%")
    print(f"Calibration Gap:                {v70.get('calibration_gap', 0)*100:.2f}%")
    print(f"Verification Verdict:           {'VERIFIED [MATHEMATICALLY SOUND]' if v70.get('is_verified') else 'NEEDS_REFINEMENT'}")
    
    print("\n----------------------------------------------------------------------")
    print("  RELIABILITY DIAGRAM BINS (OUT-OF-SAMPLE TEST SET)")
    print("----------------------------------------------------------------------")
    for b in verif.get('reliability_bins', []):
        pred_pct = b['mean_predicted'] * 100
        act_pct = b['actual_win_rate'] * 100
        gap_pct = b['gap'] * 100
        print(f"  Bin [{b['bin_range']}]: Pred = {pred_pct:5.1f}% | Actual = {act_pct:5.1f}% | Gap = {gap_pct:4.1f}% | N = {b['samples']}")
    print("======================================================================\n")

if __name__ == '__main__':
    main()
