"""
Claude Code Alternative - Code Analysis Engine
Analyzes code structure, quality, and provides insights
"""

import ast
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CodeMetrics:
    """Code metrics and analysis results"""
    lines_of_code: int
    complexity_score: float
    functions_count: int
    classes_count: int
    imports_count: int
    docstrings_count: int
    comments_count: int
    code_to_comment_ratio: float
    potential_issues: List[str]


class CodeAnalyzer:
    """Core code analysis functionality"""
    
    def __init__(self):
        """Initialize code analyzer"""
        self.supported_languages = {
            'python': self._analyze_python,
            'javascript': self._analyze_javascript,
            'java': self._analyze_java,
            'c++': self._analyze_cpp,
            'c#': self._analyze_csharp,
            'ruby': self._analyze_ruby,
            'go': self._analyze_go,
            'rust': self._analyze_rust,
            'php': self._analyze_php,
            'swift': self._analyze_swift,
            'kotlin': self._analyze_kotlin,
            'typescript': self._analyze_typescript
        }
    
    def analyze_code(self, code: str, language: str) -> CodeMetrics:
        """Analyze code and return metrics"""
        analyzer = self.supported_languages.get(language.lower())
        if not analyzer:
            raise ValueError(f"Unsupported language: {language}")
        
        return analyzer(code)
    
    def _analyze_python(self, code: str) -> CodeMetrics:
        """Analyze Python code"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return CodeMetrics(0, 0, 0, 0, 0, 0, 0, 0, ["Syntax error in Python code"])
        
        lines = code.split('\n')
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        
        # Count docstrings and comments
        docstrings = 0
        comments = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                docstrings += 1
            elif isinstance(node, ast.Comment):
                comments += 1
        
        # Simple complexity calculation (basic cyclomatic complexity)
        complexity = len(functions) * 2  # Simplified
        
        # Code to comment ratio
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        # Identify potential issues
        issues = []
        if complexity > 10:
            issues.append("High cyclomatic complexity detected")
        if ratio < 0.1:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=len(functions),
            classes_count=len(classes),
            imports_count=len(imports),
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_javascript(self, code: str) -> CodeMetrics:
        """Analyze JavaScript code"""
        lines = code.split('\n')
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'const\s+\w+\s*=\s*\(.*\)\s*=>\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*\s+from\s+.*;', code)) + \
                 len(re.findall(r'require\s*\(\s*.*\s*\)', code))
        
        # Simple complexity (basic function count)
        complexity = functions * 1.5
        
        # Comment detection
        comments = len(re.findall(r'//.*|/\*[\s\S]*?\*/', code))
        docstrings = 0  # JavaScript doesn't have formal docstrings like Python
        
        # Code to comment ratio
        total_lines = len(lines)
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 15:
            issues.append("High function complexity detected")
        if ratio < 0.08:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_java(self, code: str) -> CodeMetrics:
        """Analyze Java code"""
        lines = code.split('\n')
        functions = len(re.findall(r'public\s+\w+\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'private\s+\w+\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'protected\s+\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = functions * 2
        
        comments = len(re.findall(r'//.*|/\*[\s\S]*?\*/', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 20:
            issues.append("High method complexity detected")
        if ratio < 0.15:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_cpp(self, code: str) -> CodeMetrics:
        """Analyze C++ code"""
        lines = code.split('\n')
        functions = len(re.findall(r'\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'#include\s+<.*>|#include\s+\".*\"', code))
        
        complexity = functions * 1.8
        
        comments = len(re.findall(r'//.*|/\*[\s\S]*?\*/', code))
        docstrings = 0
        
        total_lines = len(lines)
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 18:
            issues.append("High function complexity detected")
        if ratio < 0.1:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_csharp(self, code: str) -> CodeMetrics:
        """Analyze C# code"""
        lines = code.split('\n')
        functions = len(re.findall(r'public\s+\w+\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'private\s+\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'using\s+.*;', code))
        
        complexity = functions * 1.7
        
        comments = len(re.findall(r'//.*|/\*[\s\S]*?\*/', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 15:
            issues.append("High method complexity detected")
        if ratio < 0.12:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_ruby(self, code: str) -> CodeMetrics:
        """Analyze Ruby code"""
        lines = code.split('\n')
        functions = len(re.findall(r'def\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'require\s+.*', code))
        
        complexity = functions * 1.6
        
        comments = len(re.findall(r'#.*', code))
        docstrings = 0
        
        total_lines = len(lines)
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 14:
            issues.append("High method complexity detected")
        if ratio < 0.09:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_go(self, code: str) -> CodeMetrics:
        """Analyze Go code"""
        lines = code.split('\n')
        functions = len(re.findall(r'func\s+\w+\s*\(.*\)\s*\{', code))
        structs = len(re.findall(r'type\s+\w+\s+struct\s*\{', code))
        imports = len(re.findall(r'import\s+\(.*\)', code))
        
        complexity = functions * 1.5
        
        comments = len(re.findall(r'//.*', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 12:
            issues.append("High function complexity detected")
        if ratio < 0.11:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_rust(self, code: str) -> CodeMetrics:
        """Analyze Rust code"""
        lines = code.split('\n')
        functions = len(re.findall(r'fn\s+\w+\s*\(.*\)\s*\{', code))
        structs = len(re.findall(r'struct\s+\w+\s*\{', code))
        imports = len(re.findall(r'use\s+.*;', code))
        
        complexity = functions * 1.4
        
        comments = len(re.findall(r'//.*', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 10:
            issues.append("High function complexity detected")
        if ratio < 0.13:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_php(self, code: str) -> CodeMetrics:
        """Analyze PHP code"""
        lines = code.split('\n')
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'require_once\s+.*|include_once\s+.*', code))
        
        complexity = functions * 1.6
        
        comments = len(re.findall(r'#.*|//.*|/\*[\s\S]*?\*/', code))
        docstrings = 0
        
        total_lines = len(lines)
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 16:
            issues.append("High function complexity detected")
        if ratio < 0.08:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_swift(self, code: str) -> CodeMetrics:
        """Analyze Swift code"""
        lines = code.split('\n')
        functions = len(re.findall(r'func\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = functions * 1.5
        
        comments = len(re.findall(r'//.*', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 14:
            issues.append("High function complexity detected")
        if ratio < 0.12:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_kotlin(self, code: str) -> CodeMetrics:
        """Analyze Kotlin code"""
        lines = code.split('\n')
        functions = len(re.findall(r'fun\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = functions * 1.6
        
        comments = len(re.findall(r'//.*', code))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len(lines)
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 15:
            issues.append("High function complexity detected")
        if ratio < 0.11:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )
    
    def _analyze_typescript(self, code: str) -> CodeMetrics:
        """Analyze TypeScript code"""
        lines = code.split('\n')
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'const\s+\w+\s*=\s*\(.*\)\s*=>\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*\s+from\s+.*;', code))
        
        complexity = functions * 1.5
        
        comments = len(re.findall(r'//.*|/\*[\s\S]*?\*/', code))
        docstrings = 0
        
        total_lines = len(lines)
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        if complexity > 16:
            issues.append("High function complexity detected")
        if ratio < 0.09:
            issues.append("Low code documentation ratio")
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues
        )


# Example usage
if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    
    # Test Python code
    python_code = '''
    def sort_numbers(numbers):
        """Sort a list of numbers"""
        return sorted(numbers)
    
    # Main function
    if __name__ == "__main__":
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        print(sort_numbers(nums))
    '''
    
    metrics = analyzer.analyze_code(python_code, 'python')
    print("Python Code Analysis:")
    print(f"Lines of code: {metrics.lines_of_code}")
    print(f"Complexity score: {metrics.complexity_score}")
    print(f"Functions: {metrics.functions_count}")
    print(f"Potential issues: {metrics.potential_issues}")