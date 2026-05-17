import re

class RuleDetector:
    def score(self, text: str) -> float:
        text_lower = text.lower()
        keywords = ["ignore previous", "system prompt", "jailbreak", "unrestricted", 
                   "bypass safety", "reveal instructions", "forget all", "hidden prompt"]
        score = sum(0.3 for kw in keywords if kw in text_lower)
        if re.search(r'\d{5}-\d{7}-\d', text):  # CNIC pattern
            score += 0.2
        return min(score, 1.0)
