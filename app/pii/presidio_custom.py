from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

class CustomPresidio:
    def __init__(self):
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        
        # Custom CNIC Recognizer
        cnic_pattern = Pattern(name="cnic_pattern", regex=r"\b\d{5}-\d{7}-\d\b", score=0.9)
        registry.add_recognizer(PatternRecognizer(supported_entity="CNIC", patterns=[cnic_pattern]))
        
        # Student ID
        student_pattern = Pattern(name="student_id", regex=r"\b(FA|SP|FA2[0-9])-\w+-\d{3}\b", score=0.85)
        registry.add_recognizer(PatternRecognizer(supported_entity="STUDENT_ID", patterns=[student_pattern]))
        
        self.analyzer = AnalyzerEngine(registry=registry)
        self.anonymizer = AnonymizerEngine()
    
    def analyze(self, text: str):
        return self.analyzer.analyze(text=text, language="en", score_threshold=0.6)
    
    def anonymize(self, text: str, results):
        return self.anonymizer.anonymize(text=text, analyzer_results=results).text
