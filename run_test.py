#!/usr/bin/env python3
"""
Quick test script for Claude Code Alternative
"""

from code_generation.code_generator import CodeGenerator
from nlp_module.nlp_processor import NLPProcessor

def test_code_generation():
    """Test code generation functionality"""
    print("=" * 60)
    print("Testing Claude Code Alternative")
    print("=" * 60)

    # Test 1: Code Generation
    print("\n1. Testing Code Generation...")
    generator = CodeGenerator()

    test_requests = [
        ("python", "Write a Python function to sort a list of numbers"),
        ("javascript", "Create a JavaScript function to calculate sum of array"),
        ("java", "Generate a Java function to find elements in array")
    ]

    for language, request in test_requests:
        print(f"\n  Language: {language}")
        print(f"  Request: {request}")
        result = generator.generate_code(request, language)
        print(f"  ✅ Generated {len(result.generated_functions)} function(s)")
        print(f"  Confidence: {result.confidence:.2f}")

    # Test 2: NLP Processing
    print("\n2. Testing NLP Processing...")
    nlp = NLPProcessor()

    test_text = "Create a Python function to sort a list of numbers"
    analysis = nlp.extract_code_requirements(test_text)

    print(f"  Request Type: {analysis['request_type']}")
    print(f"  Language: {analysis.get('language', 'Not detected')}")
    print(f"  Keywords: {', '.join(analysis['keywords'])}")

    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)

if __name__ == "__main__":
    test_code_generation()
