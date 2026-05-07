from typing import List, Dict, Any
from pydantic import BaseModel

class ConfidenceScore(BaseModel):
    score: int # 0-100
    reasons: List[str]
    status: str # "high", "moderate", "low"

class ConfidenceEngine:
    """
    Operational trust scoring.
    Calculates confidence based on validation passes and repair history.
    """
    def calculate(self, validation_results: List[Dict[str, Any]], repair_count: int) -> ConfidenceScore:
        score = 100
        reasons = []
        
        # Deduct for repairs
        if repair_count > 0:
            penalty = min(repair_count * 10, 40)
            score -= penalty
            reasons.append(f"environment_repaired ({repair_count} times)")
        else:
            reasons.append("pristine_execution")

        # Check validation results
        all_passed = True
        for res in validation_results:
            if res.get("success"):
                reasons.append(f"validation_passed: {res.get('type', 'generic')}")
            else:
                all_passed = False
                score -= 20
                reasons.append(f"validation_failed: {res.get('type', 'generic')}")
        
        if all_passed and score > 90:
            reasons.append("high_confidence_target_reached")

        score = max(0, min(100, score))
        
        status = "high"
        if score < 50:
            status = "low"
        elif score < 80:
            status = "moderate"
            
        return ConfidenceScore(score=score, reasons=reasons, status=status)
