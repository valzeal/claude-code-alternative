"""
Zeal Code - Enhanced Code Analysis Engine (Phase 3)
Advanced language support with better parsing, complexity calculation, and issue detection
"""

import ast
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CodeMetrics:
    """Enhanced code metrics and analysis results"""
    lines_of_code: int
    complexity_score: float
    functions_count: int
    classes_count: int
    imports_count: int
    docstrings_count: int
    comments_count: int
    code_to_comment_ratio: float
    potential_issues: List[str] = field(default_factory=list)
    code_smells: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    maintainability_index: float = 0.0
    technical_debt_ratio: float = 0.0


class EnhancedCodeAnalyzer:
    """Enhanced code analysis with Phase 3 features"""
    
    def __init__(self):
        """Initialize enhanced code analyzer"""
        self.supported_languages = {
            'python': self._analyze_python_enhanced,
            'javascript': self._analyze_javascript_enhanced,
            'java': self._analyze_java_enhanced,
            'c++': self._analyze_cpp_enhanced,
            'c#': self._analyze_csharp_enhanced,
            'ruby': self._analyze_ruby_enhanced,
            'go': self._analyze_go_enhanced,
            'rust': self._analyze_rust_enhanced,
            'php': self._analyze_php_enhanced,
            'swift': self._analyze_swift_enhanced,
            'kotlin': self._analyze_kotlin_enhanced,
            'typescript': self._analyze_typescript_enhanced
        }
    
    def analyze_code(self, code: str, language: str) -> CodeMetrics:
        """Analyze code and return enhanced metrics"""
        analyzer = self.supported_languages.get(language.lower())
        if not analyzer:
            raise ValueError(f"Unsupported language: {language}")
        
        return analyzer(code)
    
    def _calculate_cyclomatic_complexity(self, code: str, language: str) -> int:
        """Calculate actual cyclomatic complexity based on control flow"""
        complexity = 1  # Base complexity
        
        if language == 'python':
            # Count control flow statements
            complexity += code.count('if ') + code.count('elif ')
            complexity += code.count('for ') + code.count('while ')
            complexity += code.count('except ')
            complexity += code.count(' and ') + code.count(' or ')
        elif language in ['javascript', 'typescript']:
            complexity += code.count('if (') + code.count('else if')
            complexity += code.count('for (') + code.count('while (')
            complexity += code.count('catch (')
            complexity += code.count('&&') + code.count('||')
        elif language == 'java':
            complexity += code.count('if (') + code.count('else if')
            complexity += code.count('for (') + code.count('while (')
            complexity += code.count('catch (')
            complexity += code.count('&&') + code.count('||')
        elif language in ['c++', 'c#']:
            complexity += code.count('if (') + code.count('else if')
            complexity += code.count('for (') + code.count('while (')
            complexity += code.count('catch (')
            complexity += code.count('&&') + code.count('||')
        
        return complexity
    
    def _calculate_maintainability_index(self, metrics: CodeMetrics) -> float:
        """Calculate maintainability index (MI) based on complexity, LOC, and comments"""
        # MI = 171 - 5.2 * ln(aveV) - 0.23 * aveG - 16.2 * ln(aveLOC)
        # Simplified version
        try:
            complexity_factor = 5.2 * (metrics.complexity_score ** 0.5)
            loc_factor = 16.2 * (metrics.lines_of_code ** 0.5)
            comment_factor = 50 * metrics.code_to_comment_ratio
            
            mi = 171 - complexity_factor - loc_factor + comment_factor
            return max(0, min(100, mi))  # Clamp between 0-100
        except:
            return 50.0  # Default if calculation fails
    
    def _analyze_python_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Python code analysis"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return CodeMetrics(
                lines_of_code=0,
                complexity_score=0,
                functions_count=0,
                classes_count=0,
                imports_count=0,
                docstrings_count=0,
                comments_count=0,
                code_to_comment_ratio=0,
                potential_issues=["Syntax error in Python code"]
            )
        
        lines = code.split('\n')
        
        # Enhanced function detection
        functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        
        # Enhanced docstring detection
        docstrings = 0
        comments = 0
        
        # Check module docstring
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
            docstrings += 1
        
        # Check function and class docstrings
        for node in functions + classes:
            if node.body and isinstance(node.body[0], ast.Expr):
                if isinstance(node.body[0].value, ast.Str):
                    docstrings += 1
        
        # Count comments
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('#!'):
                comments += 1
        
        # Calculate actual cyclomatic complexity
        complexity = self._calculate_cyclomatic_complexity(code, 'python')
        
        # Enhanced complexity based on nesting and function count
        for func in functions:
            try:
                # Calculate function-specific complexity
                func_complexity = 1
                for node in ast.walk(func):
                    if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                        func_complexity += 1
                complexity += func_complexity
            except:
                pass
        
        # Code to comment ratio
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        # Detect issues and code smells
        issues = []
        code_smells = []
        security_issues = []
        
        # Complexity issues
        for func in functions:
            try:
                func_lines = func.end_lineno - func.lineno if hasattr(func, 'end_lineno') else 0
                if func_lines > 50:
                    code_smells.append(f"Function '{func.name}' is too long ({func_lines} lines)")
                
                # Check parameter count
                param_count = len(func.args.args) + len(func.args.kwonlyargs)
                if param_count > 5:
                    code_smells.append(f"Function '{func.name}' has too many parameters ({param_count})")
            except:
                pass
        
        if complexity > 15:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.15:
            code_smells.append("Low code documentation ratio")
        
        # Security issues
        if 'eval(' in code:
            security_issues.append("Use of eval() detected - security risk")
        if 'exec(' in code:
            security_issues.append("Use of exec() detected - security risk")
        if re.search(r'from\s+subprocess\s+import\s+.*\n.*shell=True', code):
            security_issues.append("subprocess call with shell=True detected - potential shell injection")
        
        # Calculate maintainability index
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=len(functions),
            classes_count=len(classes),
            imports_count=len(imports),
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=len(functions),
            classes_count=len(classes),
            imports_count=len(imports),
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_javascript_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced JavaScript code analysis"""
        lines = code.split('\n')
        
        # Enhanced function detection
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'const\s+\w+\s*=\s*\(.*\)\s*=>\s*\{', code)) + \
                   len(re.findall(r'\w+\s*:\s*function\s*\(.*\)\s*\{', code))
        
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*\s+from\s+.*;', code)) + \
                 len(re.findall(r'require\s*\(\s*["\'].*["\']\s*\)', code))
        
        # Calculate complexity
        complexity = self._calculate_cyclomatic_complexity(code, 'javascript')
        
        # Comment detection
        single_comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        multi_comments = len(re.findall(r'/\*[\s\S]*?\*/', code))
        comments = single_comments + multi_comments
        docstrings = 0
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        # Enhanced issue detection
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 20:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.1:
            code_smells.append("Low code documentation ratio")
        
        # Detect var usage (code smell)
        var_count = len(re.findall(r'\bvar\s+', code))
        if var_count > 0:
            code_smells.append(f"Use of 'var' detected ({var_count} times) - prefer let/const")
        
        # Security issues
        if 'eval(' in code:
            security_issues.append("Use of eval() detected - security risk")
        if 'innerHTML' in code and 'innerHTML = ' not in code.replace('innerHTML = innerHTML', ''):
            # Only flag if not using with innerHTML to innerHTML assignment (XSS-safe)
            for line in code.split('\n'):
                if 'innerHTML' in line and '=' in line and 'innerHTML = innerHTML' not in line:
                    security_issues.append("Direct innerHTML assignment - potential XSS vulnerability")
                    break
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_java_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Java code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'(public|private|protected)\s+\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        interfaces = len(re.findall(r'interface\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'java')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 25:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.15:
            code_smells.append("Low code documentation ratio")
        
        # Security issues
        if re.search(r'Runtime\.getRuntime\(\)\.exec', code):
            security_issues.append("Direct Runtime.exec() call - potential command injection")
        if re.search(r'Class\.forName', code):
            code_smells.append("Use of Class.forName() - potential classloader injection risk")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_cpp_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced C++ code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        structs = len(re.findall(r'struct\s+\w+\s*\{', code))
        imports = len(re.findall(r'#include\s+<.*>|#include\s+"[^\"]*"', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'c++')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        multi_comments = len(re.findall(r'/\*[\s\S]*?\*/', code))
        docstrings = multi_comments  # C++ uses multi-line comments for docs
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 22:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.1:
            code_smells.append("Low code documentation ratio")
        
        # Security issues
        if re.search(r'scanf\s*\(', code):
            security_issues.append("Use of scanf() detected - potential buffer overflow")
        if re.search(r'gets\s*\(', code):
            security_issues.append("Use of gets() detected - critical buffer overflow risk")
        if re.search(r'strcpy\s*\(', code):
            security_issues.append("Use of strcpy() detected - potential buffer overflow, use strncpy instead")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_csharp_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced C# code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'(public|private|protected|internal)\s+\w+\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        interfaces = len(re.findall(r'interface\s+\w+\s*\{', code))
        imports = len(re.findall(r'using\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'c#')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 20:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.12:
            code_smells.append("Low code documentation ratio")
        
        # Security issues
        if re.search(r'System\.Diagnostics\.Process\.Start', code):
            security_issues.append("Direct Process.Start() call - potential command injection")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    # Stub implementations for other languages (can be enhanced similarly)
    def _analyze_ruby_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Ruby code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'def\s+\w+\s*\(.*\)\s*(\n|\Z)', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        modules = len(re.findall(r'module\s+\w+\s*\{', code))
        imports = len(re.findall(r'require\s+[\'"][^\'"]+[\'"]', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'ruby')
        
        comments = len(re.findall(r'#.*$', code, re.MULTILINE))
        docstrings = 0
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        
        if complexity > 18:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.09:
            code_smells.append("Low code documentation ratio")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + modules,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + modules,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_go_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Go code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'func\s+\w+\s*\(.*\)\s*\{', code))
        structs = len(re.findall(r'type\s+\w+\s+struct\s*\{', code))
        interfaces = len(re.findall(r'type\s+\w+\s+interface\s*\{', code))
        imports = len(re.findall(r'import\s*\([^)]+\)', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'go')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = 0  # Go doesn't have formal docstrings
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        
        if complexity > 15:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.11:
            code_smells.append("Low code documentation ratio")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_rust_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Rust code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'fn\s+\w+\s*\(.*\)\s*\{', code))
        structs = len(re.findall(r'struct\s+\w+\s*\{', code))
        enums = len(re.findall(r'enum\s+\w+\s*\{', code))
        imports = len(re.findall(r'use\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'rust')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        
        if complexity > 12:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.13:
            code_smells.append("Low code documentation ratio")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs + enums,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=structs + enums,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_php_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced PHP code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        interfaces = len(re.findall(r'interface\s+\w+\s*\{', code))
        imports = len(re.findall(r'require_once\s+[\'"][^\'"]+[\'"]|include_once\s+[\'"][^\'"]+[\'"]', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'php')
        
        comments = len(re.findall(r'(#.*$|//.*$)', code, re.MULTILINE))
        multi_comments = len(re.findall(r'/\*[\s\S]*?\*/', code))
        docstrings = multi_comments
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 18:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.08:
            code_smells.append("Low code documentation ratio")
        
        # Security issues
        if re.search(r'mysql_query\s*\(', code):
            security_issues.append("Use of mysql_query() detected - deprecated and vulnerable")
        if re.search(r'\$_GET\[.*\]', code) or re.search(r'\$_POST\[.*\]', code):
            security_issues.append("Direct use of $_GET/$_POST - potential SQL injection if used in queries")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_swift_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Swift code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'func\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        structs = len(re.findall(r'struct\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'swift')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        
        if complexity > 16:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.12:
            code_smells.append("Low code documentation ratio")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + structs,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_kotlin_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced Kotlin code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'fun\s+\w+\s*\(.*\)\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        interfaces = len(re.findall(r'interface\s+\w+\s*\{', code))
        objects = len(re.findall(r'object\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'kotlin')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        docstrings = len(re.findall(r'/\*\*[\s\S]*?\*/', code))
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        
        if complexity > 18:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.11:
            code_smells.append("Low code documentation ratio")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces + objects,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces + objects,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )
    
    def _analyze_typescript_enhanced(self, code: str) -> CodeMetrics:
        """Enhanced TypeScript code analysis"""
        lines = code.split('\n')
        
        functions = len(re.findall(r'function\s+\w+\s*\(.*\)\s*\{', code)) + \
                   len(re.findall(r'const\s+\w+\s*=\s*\(.*\)\s*=>\s*\{', code))
        classes = len(re.findall(r'class\s+\w+\s*\{', code))
        interfaces = len(re.findall(r'interface\s+\w+\s*\{', code))
        imports = len(re.findall(r'import\s+.*\s+from\s+.*;', code))
        
        complexity = self._calculate_cyclomatic_complexity(code, 'typescript')
        
        comments = len(re.findall(r'//.*$', code, re.MULTILINE))
        multi_comments = len(re.findall(r'/\*[\s\S]*?\*/', code))
        docstrings = multi_comments
        
        total_lines = len([l for l in lines if l.strip()])
        comment_lines = comments + docstrings
        ratio = comment_lines / total_lines if total_lines > 0 else 0
        
        issues = []
        code_smells = []
        security_issues = []
        
        if complexity > 20:
            issues.append(f"High cyclomatic complexity detected: {complexity}")
        
        if ratio < 0.09:
            code_smells.append("Low code documentation ratio")
        
        # Detect any type usage (good practice)
        any_types = len(re.findall(r':\s+any\b', code))
        if any_types > 0:
            code_smells.append(f"Use of 'any' type detected ({any_types} times) - prefer specific types")
        
        if 'eval(' in code:
            security_issues.append("Use of eval() detected - security risk")
        
        maintainability = self._calculate_maintainability_index(CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio
        ))
        
        return CodeMetrics(
            lines_of_code=total_lines,
            complexity_score=complexity,
            functions_count=functions,
            classes_count=classes + interfaces,
            imports_count=imports,
            docstrings_count=docstrings,
            comments_count=comments,
            code_to_comment_ratio=ratio,
            potential_issues=issues,
            code_smells=code_smells,
            security_issues=security_issues,
            maintainability_index=maintainability,
            technical_debt_ratio=(1.0 - maintainability/100.0)
        )


# Example usage
if __name__ == "__main__":
    analyzer = EnhancedCodeAnalyzer()
    
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
    
    # Bad practice
    user_input = input("Enter command: ")
    eval(user_input)  # Security risk!
    '''
    
    metrics = analyzer.analyze_code(python_code, 'python')
    print("Enhanced Python Code Analysis:")
    print(f"Lines of code: {metrics.lines_of_code}")
    print(f"Cyclomatic complexity: {metrics.complexity_score}")
    print(f"Functions: {metrics.functions_count}")
    print(f"Maintainability Index: {metrics.maintainability_index:.1f}")
    print(f"Technical Debt Ratio: {metrics.technical_debt_ratio:.2%}")
    print(f"Potential issues: {metrics.potential_issues}")
    print(f"Code smells: {metrics.code_smells}")
    print(f"Security issues: {metrics.security_issues}")
