"""
Zeal Code - Natural Language Processing Module
Handles text parsing, understanding, and intent recognition
"""

import re
from typing import Dict, List, Optional, Tuple
import spacy
from transformers import pipeline


class NLPProcessor:
    """Core NLP processing class for code assistant"""
    
    def __init__(self):
        """Initialize NLP components"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.text_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            print(f"Warning: NLP model loading failed - {e}")
            self.nlp = None
            self.text_classifier = None
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess input text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters (keep basic punctuation)
        text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        return text
    
    def analyze_intent(self, text: str) -> Dict:
        """Analyze user intent from text"""
        if not text or not self.text_classifier:
            return {"intent": "unknown", "confidence": 0.0}
        
        cleaned_text = self.preprocess_text(text)
        if not cleaned_text:
            return {"intent": "unknown", "confidence": 0.0}
        
        try:
            result = self.text_classifier(cleaned_text[:512])  # Limit to model max length
            return {
                "intent": result[0]['label'],
                "confidence": result[0]['score'],
                "text": cleaned_text
            }
        except Exception as e:
            print(f"Intent analysis failed: {e}")
            return {"intent": "unknown", "confidence": 0.0}
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        if not text or not self.nlp:
            return []
        
        doc = self.nlp(text)
        keywords = []
        
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN']:
                keywords.append(token.lemma_.lower())
        
        return list(set(keywords))  # Remove duplicates
    
    def parse_code_request(self, text: str) -> Dict:
        """Parse code-related requests and extract parameters"""
        intent = self.analyze_intent(text)
        keywords = self.extract_keywords(text)
        
        # Simple pattern matching for common code requests
        patterns = {
            'generate': r'(generate|create|write|make|build|implement) (code|function|class|script)',
            'explain': r'(explain|describe|show|tell me about) (code|function|class|script)',
            'review': r'(review|analyze|check|audit) (code|function|class|script)',
            'debug': r'(debug|fix|solve|troubleshoot) (bug|error|issue|problem)',
            'refactor': r'(refactor|improve|optimize) (code|function|class|script)',
            'test': r'(test|write test|create test) (case|suite)'
        }
        
        request_type = "unknown"
        for action, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                request_type = action
                break
        
        return {
            "request_type": request_type,
            "intent": intent["intent"],
            "confidence": intent["confidence"],
            "keywords": keywords,
            "text": text
        }
    
    def get_code_language(self, text: str) -> Optional[str]:
        """Detect programming language from text"""
        language_patterns = {
            'python': r'\.py\b|python\b|pip\b|import\b',
            'javascript': r'\.js\b|javascript\b|node\.js\b|npm\b',
            'java': r'\.java\b|java\b|javac\b|class\b',
            'c++': r'\.cpp\b|\.h\b|c\+\+|cpp\b',
            'c#': r'\.cs\b|c#\b|dotnet\b',
            'ruby': r'\.rb\b|ruby\b|gem\b',
            'go': r'\.go\b|go\b|golang\b',
            'rust': r'\.rs\b|rust\b',
            'php': r'\.php\b|php\b',
            'swift': r'\.swift\b|swift\b',
            'kotlin': r'\.kt\b|kotlin\b',
            'typescript': r'\.ts\b|typescript\b'
        }
        
        for lang, pattern in language_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return lang
        
        return None
    
    def extract_code_requirements(self, text: str) -> Dict:
        """Extract specific requirements from code-related requests"""
        parsed = self.parse_code_request(text)
        language = self.get_code_language(text)
        
        # Extract function/class names and parameters
        function_pattern = r'(function|class|def|func)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(function_pattern, text, re.IGNORECASE)
        
        return {
            "request_type": parsed["request_type"],
            "language": language,
            "functions": [match[1] for match in matches],
            "keywords": parsed["keywords"],
            "confidence": parsed["confidence"]
        }


# Example usage
if __name__ == "__main__":
    processor = NLPProcessor()
    test_text = "Write a Python function to sort a list of numbers"
    result = processor.parse_code_request(test_text)
    print(f"Code request analysis: {result}")
    print(f"Detected language: {processor.get_code_language(test_text)}")