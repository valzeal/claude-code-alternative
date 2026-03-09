#!/usr/bin/env python3
"""Test the enhanced code analyzer"""

import sys
sys.path.append('.')

from code_analysis.enhanced_analyzer import EnhancedCodeAnalyzer

# Test Python code with issues
python_code = '''
def process_data(data):
    """Process some data"""
    result = []
    for item in data:
        if item > 0:
            if item < 100:
                if item % 2 == 0:
                    result.append(item * 2)
    return result

# Security risk
user_input = "print('hello')"
'''

analyzer = EnhancedCodeAnalyzer()
metrics = analyzer.analyze_code(python_code, 'python')

print("=" * 60)
print("Enhanced Python Code Analysis (Phase 3)")
print("=" * 60)
print(f"Lines of code: {metrics.lines_of_code}")
print(f"Cyclomatic complexity: {metrics.complexity_score}")
print(f"Functions: {metrics.functions_count}")
print(f"Classes: {metrics.classes_count}")
print(f"Maintainability Index: {metrics.maintainability_index:.1f}/100")
print(f"Technical Debt Ratio: {metrics.technical_debt_ratio:.2%}")
print(f"\nPotential issues: {metrics.potential_issues}")
print(f"Code smells: {metrics.code_smells}")
print(f"Security issues: {metrics.security_issues}")
print("=" * 60)
