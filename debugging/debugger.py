"""
Zeal Code - Debugging and Testing Module
Helps identify and fix bugs, generates test cases, and provides debugging assistance
"""

import ast
import re
import unittest
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import textwrap
import sys
import io


@dataclass
class DebugAnalysis:
    """Debugging analysis result"""
    issues: List[Dict]
    suggested_fixes: List[Dict]
    test_cases: List[Dict]
    confidence: float = 0.0


class Debugger:
    """Core debugging and testing functionality"""
    
    def __init__(self):
        """Initialize debugger"""
        self.code_analyzer = CodeAnalyzer()  # Assuming CodeAnalyzer exists from previous module
        self.test_generator = TestGenerator()
    
    def analyze_code_for_bugs(self, code: str, language: str) -> DebugAnalysis:
        """Analyze code for potential bugs and issues"""
        try:
            # Analyze code structure and identify potential issues
            metrics = self.code_analyzer.analyze_code(code, language)
            
            # Identify bugs and issues
            issues = self._identify_bugs(code, language, metrics)
            
            # Generate suggested fixes
            suggested_fixes = self._generate_fixes(code, language, issues)
            
            # Generate test cases
            test_cases = self.test_generator.generate_test_cases(code, language, issues)
            
            return DebugAnalysis(
                issues=issues,
                suggested_fixes=suggested_fixes,
                test_cases=test_cases,
                confidence=0.8
            )
        except Exception as e:
            raise RuntimeError(f"Debug analysis failed: {str(e)}")
    
    def _identify_bugs(self, code: str, language: str, metrics: CodeMetrics) -> List[Dict]:
        """Identify potential bugs and issues in code"""
        issues = []
        
        # Check for common bugs based on complexity
        if metrics.complexity_score > 15:
            issues.append({
                'type': 'logic_error',
                'severity': 'medium',
                'message': 'High complexity may indicate potential logic errors',
                'location': 'General',
                'suggestion': 'Review complex logic paths for off-by-one errors or edge cases'
            })
        
        # Check for potential null/undefined issues
        if language.lower() in ['javascript', 'typescript', 'java', 'c#', 'swift', 'kotlin']:
            null_issues = self._check_null_issues(code, language)
            issues.extend(null_issues)
        
        # Check for potential infinite loops
        loop_issues = self._check_infinite_loops(code, language)
        issues.extend(loop_issues)
        
        # Check for division by zero
        division_issues = self._check_division_by_zero(code, language)
        issues.extend(division_issues)
        
        # Language-specific bug detection
        if language.lower() == 'python':
            python_issues = self._python_bug_detection(code)
            issues.extend(python_issues)
        elif language.lower() == 'javascript':
            js_issues = self._javascript_bug_detection(code)
            issues.extend(js_issues)
        elif language.lower() == 'java':
            java_issues = self._java_bug_detection(code)
            issues.extend(java_issues)
        
        return issues
    
    def _generate_fixes(self, code: str, language: str, issues: List[Dict]) -> List[Dict]:
        """Generate suggested fixes for identified issues"""
        fixes = []
        
        for issue in issues:
            if issue['type'] == 'null_error':
                fixes.append({
                    'issue_type': 'null_error',
                    'fix': 'Add null/undefined checks before usage',
                    'example': self._generate_null_check_example(language)
                })
            elif issue['type'] == 'infinite_loop':
                fixes.append({
                    'issue_type': 'infinite_loop',
                    'fix': 'Add proper termination conditions',
                    'example': self._generate_loop_fix_example(language)
                })
            elif issue['type'] == 'division_by_zero':
                fixes.append({
                    'issue_type': 'division_by_zero',
                    'fix': 'Add divisor validation',
                    'example': self._generate_division_fix_example(language)
                })
            elif issue['type'] == 'logic_error':
                fixes.append({
                    'issue_type': 'logic_error',
                    'fix': 'Review and simplify complex logic',
                    'example': 'Break down functions, add assertions'
                })
        
        return fixes
    
    def _check_null_issues(self, code: str, language: str) -> List[Dict]:
        """Check for potential null/undefined issues"""
        issues = []
        
        if language.lower() == 'javascript' or language.lower() == 'typescript':
            # Check for direct property access without null check
            null_accesses = re.findall(r'\.\w+\s*=', code)
            if null_accesses:
                issues.append({
                    'type': 'null_error',
                    'severity': 'high',
                    'message': 'Potential null/undefined property access',
                    'location': 'General',
                    'suggestion': 'Add null checks or use optional chaining'
                })
        
        elif language.lower() == 'java' or language.lower() == 'c#':
            # Check for method calls on potentially null objects
            null_calls = re.findall(r'\.\w+\s*\(', code)
            if null_calls:
                issues.append({
                    'type': 'null_error',
                    'severity': 'high',
                    'message': 'Potential null method calls',
                    'location': 'General',
                    'suggestion': 'Add null checks before method calls'
                })
        
        return issues
    
    def _check_infinite_loops(self, code: str, language: str) -> List[Dict]:
        """Check for potential infinite loops"""
        issues = []
        
        # Look for while loops without clear termination
        while_loops = re.findall(r'while\s*\(.*\)\s*\{', code)
        for loop in while_loops:
            if 'true' in loop or '1' in loop:
                issues.append({
                    'type': 'infinite_loop',
                    'severity': 'high',
                    'message': 'Potential infinite loop detected',
                    'location': 'While loop',
                    'suggestion': 'Add proper termination condition'
                })
        
        # Look for for loops that might not terminate
        for_loops = re.findall(r'for\s*\(.*\)\s*\{', code)
        for loop in for_loops:
            if 'true' in loop:
                issues.append({
                    'type': 'infinite_loop',
                    'severity': 'high',
                    'message': 'Potential infinite loop detected',
                    'location': 'For loop',
                    'suggestion': 'Add proper termination condition'
                })
        
        return issues
    
    def _check_division_by_zero(self, code: str, language: str) -> List[Dict]:
        """Check for potential division by zero"""
        issues = []
        
        # Look for division operations
        divisions = re.findall(r'/\s*\w+', code)
        for div in divisions:
            var = div.split()[-1]
            if var and not var.isdigit() and var != '0':
                # Check if variable could be zero
                if re.search(rf'{var}\s*=\s*0', code):
                    issues.append({
                        'type': 'division_by_zero',
                        'severity': 'high',
                        'message': f'Potential division by zero with variable {var}',
                        'location': 'Division operation',
                        'suggestion': 'Add divisor validation'
                    })
        
        return issues
    
    def _python_bug_detection(self, code: str) -> List[Dict]:
        """Python-specific bug detection"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for mutable default arguments
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            for func in functions:
                for arg in func.args.defaults:
                    if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                        issues.append({
                            'type': 'python_bug',
                            'severity': 'medium',
                            'message': 'Mutable default argument detected',
                            'location': f'Function {func.name}',
                            'suggestion': 'Use None as default and initialize inside function'
                        })
            
            # Check for potential attribute errors
            attribute_accesses = [node for node in ast.walk(tree) if isinstance(node, ast.Attribute)]
            for access in attribute_accesses:
                if isinstance(access.value, ast.Name):
                    # Check if the variable might be None
                    var_name = access.value.id
                    if re.search(rf'{var_name}\s*=\s*None', code):
                        issues.append({
                            'type': 'attribute_error',
                            'severity': 'medium',
                            'message': f'Potential attribute error on None object',
                            'location': f'Attribute access on {var_name}',
                            'suggestion': 'Add None check before attribute access'
                        })
            
        except SyntaxError:
            issues.append({
                'type': 'syntax',
                'severity': 'high',
                'message': 'Python syntax error',
                'location': 'General',
                'suggestion': 'Fix syntax errors before debugging'
            })
        
        return issues
    
    def _javascript_bug_detection(self, code: str) -> List[Dict]:
        """JavaScript-specific bug detection"""
        issues = []
        
        # Check for == instead of ===
        loose_comparisons = re.findall(r'==\s*', code)
        if loose_comparisons:
            issues.append({
                'type': 'js_bug',
                'severity': 'low',
                'message': 'Loose equality (==) detected',
                'location': 'General',
                'suggestion': 'Use strict equality (===) for better type safety'
            })
        
        # Check for variable hoisting issues
        undeclared_vars = re.findall(r'var\s+\w+\s*=', code)
        if undeclared_vars:
            issues.append({
                'type': 'js_bug',
                'severity': 'medium',
                'message': 'Potential variable hoisting issues',
                'location': 'Variable declarations',
                'suggestion': 'Declare variables before use or use let/const'
            })
        
        return issues
    
    def _java_bug_detection(self, code: str) -> List[Dict]:
        """Java-specific bug detection"""
        issues = []
        
        # Check for missing semicolons
        if ';' not in code:
            issues.append({
                'type': 'java_bug',
                'severity': 'high',
                'message': 'Missing semicolons detected',
                'location': 'General',
                'suggestion': 'Add semicolons to terminate statements'
            })
        
        # Check for potential array index out of bounds
        array_accesses = re.findall(r'\[\d+\]', code)
        if array_accesses:
            issues.append({
                'type': 'java_bug',
                'severity': 'medium',
                'message': 'Potential array index issues',
                'location': 'Array access',
                'suggestion': 'Add bounds checking for array operations'
            })
        
        return issues
    
    def _generate_null_check_example(self, language: str) -> str:
        """Generate null check example for the given language"""
        examples = {
            'javascript': 'if (obj && obj.property) { ... }',
            'typescript': 'if (obj?.property) { ... }',
            'java': 'if (obj != null && obj.getProperty() != null) { ... }',
            'c#': 'if (obj != null && obj.Property != null) { ... }',
            'swift': 'if let property = obj?.property { ... }',
            'kotlin': 'obj?.property?.let { ... }'
        }
        return examples.get(language.lower(), 'Add null check before usage')
    
    def _generate_loop_fix_example(self, language: str) -> str:
        """Generate loop fix example for the given language"""
        examples = {
            'python': 'while condition and counter < max_iterations: ...',
            'javascript': 'while (condition && counter < maxIterations) { ... }',
            'java': 'while (condition && counter < MAX_ITERATIONS) { ... }'
        }
        return examples.get(language.lower(), 'Add proper termination condition')
    
    def _generate_division_fix_example(self, language: str) -> str:
        """Generate division fix example for the given language"""
        examples = {
            'python': 'if divisor != 0: result = dividend / divisor',
            'javascript': 'if (divisor !== 0) { result = dividend / divisor; }',
            'java': 'if (divisor != 0) { result = dividend / divisor; }'
        }
        return examples.get(language.lower(), 'Add divisor validation')


class TestGenerator:
    """Generates test cases for code"""
    
    def generate_test_cases(self, code: str, language: str, issues: List[Dict]) -> List[Dict]:
        """Generate test cases based on code and identified issues"""
        test_cases = []
        
        # Generate basic test cases
        basic_tests = self._generate_basic_tests(code, language)
        test_cases.extend(basic_tests)
        
        # Generate tests for specific issues
        for issue in issues:
            issue_tests = self._generate_issue_specific_tests(code, language, issue)
            test_cases.extend(issue_tests)
        
        return test_cases
    
    def _generate_basic_tests(self, code: str, language: str) -> List[Dict]:
        """Generate basic test cases"""
        tests = []
        
        # Simple input/output tests
        tests.append({
            'type': 'basic',
            'description': 'Test with normal input',
            'input': 'test_data',
            'expected_output': 'expected_result',
            'priority': 'high'
        })
        
        # Edge case tests
        tests.append({
            'type': 'edge',
            'description': 'Test with empty input',
            'input': 'empty_data',
            'expected_output': 'empty_result',
            'priority': 'medium'
        })
        
        # Error case tests
        tests.append({
            'type': 'error',
            'description': 'Test with invalid input',
            'input': 'invalid_data',
            'expected_error': 'error_type',
            'priority': 'high'
        })
        
        return tests
    
    def _generate_issue_specific_tests(self, code: str, language: str, issue: Dict) -> List[Dict]:
        """Generate tests specific to identified issues"""
        tests = []
        
        if issue['type'] == 'null_error':
            tests.append({
                'type': 'null',
                'description': 'Test with null/undefined input',
                'input': 'null_value',
                'expected_behavior': 'handle_gracefully',
                'priority': 'high'
            })
        
        elif issue['type'] == 'infinite_loop':
            tests.append({
                'type': 'termination',
                'description': 'Test loop termination',
                'input': 'loop_test_data',
                'max_iterations': 100,
                'priority': 'critical'
            })
        
        elif issue['type'] == 'division_by_zero':
            tests.append({
                'type': 'division',
                'description': 'Test division by zero handling',
                'input': 'zero_divisor',
                'expected_behavior': 'handle_error',
                'priority': 'critical'
            })
        
        return tests


# Example usage
if __name__ == "__main__":
    debugger = Debugger()
    
    # Test Python code debugging
    python_code = '''
    def divide_numbers(a, b):
        return a / b
    
    def process_data(data):
        result = []
        for item in data:
            if item > 0:
                result.append(divide_numbers(item, 2))
        return result
    '''
    
    result = debugger.analyze_code_for_bugs(python_code, 'python')
    print("Debug Analysis Results:")
    print(f"Issues: {result.issues}")
    print(f"Suggested Fixes: {result.suggested_fixes}")
    print(f"Test Cases: {result.test_cases}")