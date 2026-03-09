"""
Zeal Code - Code Review and Refactoring Module
Analyzes code quality, identifies issues, and suggests improvements
"""

import ast
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import textwrap


@dataclass
class CodeReviewResult:
    """Code review analysis result"""
    issues: List[Dict]
    suggestions: List[Dict]
    metrics: Dict
    refactored_code: Optional[str] = None
    confidence: float = 0.0


class CodeReviewer:
    """Core code review and refactoring functionality"""
    
    def __init__(self):
        """Initialize code reviewer"""
        self.code_analyzer = CodeAnalyzer()  # Assuming CodeAnalyzer exists from previous module
        self.refactoring_rules = self._load_refactoring_rules()
    
    def review_code(self, code: str, language: str) -> CodeReviewResult:
        """Review code and provide analysis"""
        try:
            # Analyze code structure and quality
            metrics = self.code_analyzer.analyze_code(code, language)
            
            # Identify issues and suggestions
            issues = self._identify_issues(code, language, metrics)
            suggestions = self._generate_suggestions(code, language, metrics)
            
            # Generate refactored code if needed
            refactored_code = self._refactor_code(code, language, issues) if issues else None
            
            return CodeReviewResult(
                issues=issues,
                suggestions=suggestions,
                metrics=metrics.__dict__,
                refactored_code=refactored_code,
                confidence=0.85  # Confidence in analysis
            )
        except Exception as e:
            raise RuntimeError(f"Code review failed: {str(e)}")
    
    def _identify_issues(self, code: str, language: str, metrics: CodeMetrics) -> List[Dict]:
        """Identify code quality issues"""
        issues = []
        
        # Check complexity
        if metrics.complexity_score > 15:
            issues.append({
                'type': 'complexity',
                'severity': 'high' if metrics.complexity_score > 20 else 'medium',
                'message': f'High cyclomatic complexity detected ({metrics.complexity_score})',
                'suggestion': 'Consider breaking down complex functions'
            })
        
        # Check code documentation
        if metrics.code_to_comment_ratio < 0.1:
            issues.append({
                'type': 'documentation',
                'severity': 'medium',
                'message': f'Low code documentation ratio ({metrics.code_to_comment_ratio:.2f})',
                'suggestion': 'Add more comments and docstrings'
            })
        
        # Check function length
        if metrics.lines_of_code > 50:
            issues.append({
                'type': 'length',
                'severity': 'medium',
                'message': f'Long function detected ({metrics.lines_of_code} lines)',
                'suggestion': 'Consider splitting into smaller functions'
            })
        
        # Language-specific issues
        if language.lower() == 'python':
            issues.extend(self._python_specific_issues(code))
        elif language.lower() == 'javascript':
            issues.extend(self._javascript_specific_issues(code))
        elif language.lower() == 'java':
            issues.extend(self._java_specific_issues(code))
        
        return issues
    
    def _generate_suggestions(self, code: str, language: str, metrics: CodeMetrics) -> List[Dict]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # General suggestions based on metrics
        if metrics.complexity_score > 10:
            suggestions.append({
                'type': 'refactoring',
                'priority': 'high',
                'message': 'Consider refactoring complex functions',
                'details': 'Break down functions into smaller, more focused units'
            })
        
        if metrics.code_to_comment_ratio < 0.15:
            suggestions.append({
                'type': 'documentation',
                'priority': 'medium',
                'message': 'Improve code documentation',
                'details': 'Add docstrings, comments, and type hints'
            })
        
        # Language-specific suggestions
        if language.lower() == 'python':
            suggestions.extend(self._python_suggestions(code))
        elif language.lower() == 'javascript':
            suggestions.extend(self._javascript_suggestions(code))
        elif language.lower() == 'java':
            suggestions.extend(self._java_suggestions(code))
        
        return suggestions
    
    def _refactor_code(self, code: str, language: str, issues: List[Dict]) -> Optional[str]:
        """Refactor code based on identified issues"""
        if not issues:
            return None
        
        # Simple refactoring based on common issues
        refactored_lines = code.split('\n')
        new_lines = []
        
        for line in refactored_lines:
            # Add docstrings to functions (simplified)
            if re.search(r'def\s+\w+\s*\(.*\)\s*:', line) or re.search(r'function\s+\w+\s*\(.*\)\s*\{', line):
                new_lines.append(line)
                new_lines.append("    \"\"\"Generated docstring\"\"\"")
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _python_specific_issues(self, code: str) -> List[Dict]:
        """Python-specific code issues"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for unused imports
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            function_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            # Check for magic numbers
            magic_numbers = re.findall(r'\b\d+\b', code)
            if len(magic_numbers) > 10:
                issues.append({
                    'type': 'style',
                    'severity': 'low',
                    'message': 'Many magic numbers detected',
                    'suggestion': 'Consider using named constants'
                })
            
            # Check for long function names
            long_functions = [f for f in function_defs if len(f.name) > 20]
            if long_functions:
                issues.append({
                    'type': 'style',
                    'severity': 'low',
                    'message': 'Long function names detected',
                    'suggestion': 'Use more descriptive but concise names'
                })
            
        except SyntaxError:
            issues.append({
                'type': 'syntax',
                'severity': 'high',
                'message': 'Python syntax error',
                'suggestion': 'Fix syntax errors before proceeding'
            })
        
        return issues
    
    def _python_suggestions(self, code: str) -> List[Dict]:
        """Python-specific suggestions"""
        suggestions = []
        
        # Type hint suggestions
        if 'def ' in code and ': ' not in code.split('def ')[-1].split('(')[0]:
            suggestions.append({
                'type': 'python',
                'priority': 'medium',
                'message': 'Consider adding type hints',
                'details': 'Use type annotations for better code clarity'
            })
        
        # Docstring suggestions
        if 'def ' in code and not re.search(r'\"\"\".*\"\"\"', code):
            suggestions.append({
                'type': 'python',
                'priority': 'medium',
                'message': 'Add docstrings to functions',
                'details': 'Include function purpose, parameters, and return values'
            })
        
        return suggestions
    
    def _javascript_specific_issues(self, code: str) -> List[Dict]:
        """JavaScript-specific code issues"""
        issues = []
        
        # Check for global variables
        global_vars = re.findall(r'var\s+\w+\s*=', code)
        if global_vars:
            issues.append({
                'type': 'scope',
                'severity': 'medium',
                'message': 'Global variables detected',
                'suggestion': 'Use let/const and avoid global scope pollution'
            })
        
        # Check for callback hell
        callbacks = re.findall(r'\)\s*=>\s*\{[^}]*\}\s*\(', code)
        if len(callbacks) > 3:
            issues.append({
                'type': 'async',
                'severity': 'medium',
                'message': 'Potential callback hell detected',
                'suggestion': 'Consider using async/await or promises'
            })
        
        return issues
    
    def _javascript_suggestions(self, code: str) -> List[Dict]:
        """JavaScript-specific suggestions"""
        suggestions = []
        
        # Arrow function suggestions
        if 'function(' in code:
            suggestions.append({
                'type': 'javascript',
                'priority': 'low',
                'message': 'Consider using arrow functions',
                'details': 'More concise and modern syntax'
            })
        
        # Const/let suggestions
        if 'var ' in code:
            suggestions.append({
                'type': 'javascript',
                'priority': 'medium',
                'message': 'Consider using const/let instead of var',
                'details': 'Better scoping and mutability control'
            })
        
        return suggestions
    
    def _java_specific_issues(self, code: str) -> List[Dict]:
        """Java-specific code issues"""
        issues = []
        
        # Check for raw types
        if 'ArrayList' in code and '<>' in code:
            issues.append({
                'type': 'type_safety',
                'severity': 'medium',
                'message': 'Raw type usage detected',
                'suggestion': 'Use generics for type safety'
            })
        
        # Check for long class names
        class_names = re.findall(r'class\s+\w+', code)
        long_classes = [c for c in class_names if len(c.split()[1]) > 20]
        if long_classes:
            issues.append({
                'type': 'style',
                'severity': 'low',
                'message': 'Long class names detected',
                'suggestion': 'Use more concise class names'
            })
        
        return issues
    
    def _java_suggestions(self, code: str) -> List[Dict]:
        """Java-specific suggestions"""
        suggestions = []
        
        # Generics suggestions
        if 'ArrayList' in code and '<>' in code:
            suggestions.append({
                'type': 'java',
                'priority': 'medium',
                'message': 'Add type parameters to collections',
                'details': 'Use generics for better type safety'
            })
        
        # Method extraction suggestions
        if len(code.split('\n')) > 100:
            suggestions.append({
                'type': 'java',
                'priority': 'medium',
                'message': 'Consider extracting methods',
                'details': 'Break down large classes into smaller, focused methods'
            })
        
        return suggestions
    
    def _load_refactoring_rules(self) -> Dict:
        """Load refactoring rules and patterns"""
        return {
            'complexity_reduction': {
                'pattern': r'function\s+\w+\s*\(.*\)\s*\{[^}]{50,}\}',
                'replacement': 'Extract to smaller functions'
            },
            'documentation_improvement': {
                'pattern': r'def\s+\w+\s*\(.*\)\s*:',
                'replacement': 'Add docstring and type hints'
            },
            'variable_renaming': {
                'pattern': r'var\s+temp\s*=',
                'replacement': 'Use more descriptive variable names'
            }
        }


# Example usage
if __name__ == "__main__":
    reviewer = CodeReviewer()
    
    # Test Python code review
    python_code = '''
    def sort_numbers(numbers):
        """Sort a list of numbers"""
        return sorted(numbers)
    
    def calculate_sum(numbers):
        result = 0
        for num in numbers:
            result += num
        return result
    
    # Main function
    if __name__ == "__main__":
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        print(sort_numbers(nums))
        print(calculate_sum(nums))
    '''
    
    result = reviewer.review_code(python_code, 'python')
    print("Code Review Results:")
    print(f"Issues: {result.issues}")
    print(f"Suggestions: {result.suggestions}")
    print(f"Metrics: {result.metrics}")