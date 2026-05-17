from fastapi import FastAPI
from pydantic import BaseModel
import time
from app.detectors.rule_detector import RuleDetector
from app.detectors.semantic_detector import SemanticDetector
from app.pii.presidio_custom import CustomPresidio
from app.policy.policy_engine import PolicyEngine
from app.utils.language import detect_language

app = FastAPI(title="LLM Security Gateway")

rule_detector = RuleDetector()
semantic_detector = SemanticDetector()
presidio = CustomPresidio()
policy_engine = PolicyEngine()

class AnalyzeRequest(BaseModel):
    input_id: str
    prompt: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    start = time.time()
    
    lang = detect_language(request.prompt)
    rule_score = rule_detector.score(request.prompt)
    semantic_score = semantic_detector.score(request.prompt)
    
    pii_results = presidio.analyze(request.prompt)
    pii_list = [{"type": r.entity_type, "text": r.text, "score": r.score} for r in pii_results]
    
    policy_result = policy_engine.decide(rule_score, semantic_score, pii_results)
    
    safe_text = None
    if policy_result["decision"] == "MASK":
        safe_text = presidio.anonymize(request.prompt, pii_results)
    
    latency = round((time.time() - start) * 1000, 2)
    
    return {
        "input_id": request.input_id,
        "language": lang,
        "rule_score": round(rule_score, 3),
        "semantic_score": round(semantic_score, 3),
        "pii_entities": pii_list,
        "final_risk": policy_result["final_risk"],
        "decision": policy_result["decision"],
        "safe_text": safe_text,
        "reason_codes": policy_result["reason_codes"],
        "latency_ms": latency
    }
