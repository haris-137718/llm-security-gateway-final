class PolicyEngine:
    def decide(self, rule_score: float, semantic_score: float, pii_entities: list):
        final_risk = max(rule_score, semantic_score) + (len(pii_entities) * 0.25)
        
        if final_risk >= 0.8 or rule_score > 0.7 or semantic_score > 0.75:
            return {"decision": "BLOCK", "final_risk": round(final_risk, 3), "reason_codes": ["INJECTION_DETECTED"]}
        elif len(pii_entities) > 0:
            return {"decision": "MASK", "final_risk": round(final_risk, 3), "reason_codes": ["PII_DETECTED"]}
        else:
            return {"decision": "ALLOW", "final_risk": round(final_risk, 3), "reason_codes": []}
