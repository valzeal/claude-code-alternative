"""
Zeal Code - Documentation Generation Module
Automatically generates documentation from code
"""

import ast
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
import textwrap
from datetime import datetime


@dataclass
class DocumentationResult:
    """Documentation generation result"""
    documentation: str
    api_docs: Dict
    user_guide: str
    confidence: float = 0.0


class DocumentationGenerator:
    """Core documentation generation functionality"""
    
    def __init__(self):
        """Initialize documentation generator"""
        self.code_analyzer = CodeAnalyzer()  # Assuming CodeAnalyzer exists from previous module
        self.doc_templates = self._load_doc_templates()
    
    def generate_documentation(self, code: str, language: str, doc_type: str = 'comprehensive') -> DocumentationResult:
        """Generate documentation for the given code"""
        try:
            # Analyze code structure
            metrics = self.code_analyzer.analyze_code(code, language)
            
            # Generate different types of documentation
            if doc_type == 'api':
                docs = self._generate_api_docs(code, language, metrics)
            elif doc_type == 'user':
                docs = self._generate_user_guide(code, language, metrics)
            else:
                docs = self._generate_comprehensive_docs(code, language, metrics)
            
            return DocumentationResult(
                documentation=docs['full'],
                api_docs=docs['api'],
                user_guide=docs['user'],
                confidence=0.9
            )
        except Exception as e:
            raise RuntimeError(f"Documentation generation failed: {str(e)}")
    
    def _generate_comprehensive_docs(self, code: str, language: str, metrics: CodeMetrics) -> Dict:
        """Generate comprehensive documentation including API and user guides"""
        docs = {
            'full': '',
            'api': {},
            'user': ''
        }
        
        # Generate API documentation
        api_docs = self._generate_api_docs(code, language, metrics)
        docs['api'] = api_docs
        
        # Generate user guide
        user_guide = self._generate_user_guide(code, language, metrics)
        docs['user'] = user_guide
        
        # Combine into full documentation
        docs['full'] = f"""# Code Documentation

## Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{api_docs['full']}

## User Guide

{user_guide}

## Code Analysis Summary

- Lines of code: {metrics.lines_of_code}
- Functions: {metrics.functions_count}
- Classes: {metrics.classes_count}
- Complexity score: {metrics.complexity_score:.2f}
- Documentation ratio: {metrics.code_to_comment_ratio:.2%}
"""
        
        return docs
    
    def _generate_api_docs(self, code: str, language: str, metrics: CodeMetrics) -> Dict:
        """Generate API documentation"""
        api_docs = {
            'full': '',
            'functions': {},
            'classes': {},
            'modules': {}
        }
        
        try:
            if language.lower() == 'python':
                tree = ast.parse(code)
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                
                # Generate function documentation
                for func in functions:
                    func_docs = self._generate_python_function_docs(func)
                    api_docs['functions'][func.name] = func_docs
                
                # Generate class documentation
                for cls in classes:
                    class_docs = self._generate_python_class_docs(cls)
                    api_docs['classes'][cls.name] = class_docs
                
                # Generate full API documentation
                api_docs['full'] = self._format_api_docs(api_docs, language)
                
            elif language.lower() == 'javascript':
                api_docs = self._generate_javascript_api_docs(code, metrics)
            
            elif language.lower() == 'java':
                api_docs = self._generate_java_api_docs(code, metrics)
            
        except Exception as e:
            api_docs['full'] = f"Error generating API docs: {str(e)}"
        
        return api_docs
    
    def _generate_python_function_docs(self, func: ast.FunctionDef) -> Dict:
        """Generate documentation for Python function"""
        # Extract function name and parameters
        func_name = func.name
        params = [arg.arg for arg in func.args.args]
        
        # Extract docstring if exists
        docstring = ast.get_docstring(func) or "No documentation available"
        
        # Extract return type if annotated
        return_type = "Any"
        if func.returns:
            return_type = ast.unparse(func.returns)
        
        return {
            'name': func_name,
            'parameters': params,
            'return_type': return_type,
            'docstring': docstring,
            'line_number': func.lineno
        }
    
    def _generate_python_class_docs(self, cls: ast.ClassDef) -> Dict:
        """Generate documentation for Python class"""
        class_name = cls.name
        docstring = ast.get_docstring(cls) or "No documentation available"
        
        # Extract methods
        methods = []
        for node in ast.walk(cls):
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
        
        return {
            'name': class_name,
            'docstring': docstring,
            'methods': methods,
            'line_number': cls.lineno
        }
    
    def _format_api_docs(self, api_docs: Dict, language: str) -> str:
        """Format API documentation for display"""
        lines = [f"# {language.capitalize()} API Documentation"]
        lines.append("")
        
        # Add functions section
        if api_docs['functions']:
            lines.append("## Functions")
            lines.append("")
            for func_name, func_docs in api_docs['functions'].items():
                lines.append(f"### {func_name}()")
                lines.append(f"**Parameters:** {', '.join(func_docs['parameters'])}")
                lines.append(f"**Return type:** {func_docs['return_type']}")
                lines.append(f"**Description:** {func_docs['docstring']}")
                lines.append("")
        
        # Add classes section
        if api_docs['classes']:
            lines.append("## Classes")
            lines.append("")
            for class_name, class_docs in api_docs['classes'].items():
                lines.append(f"### {class_name}")
                lines.append(f"**Description:** {class_docs['docstring']}")
                lines.append(f"**Methods:** {', '.join(class_docs['methods'])}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _generate_javascript_api_docs(self, code: str, metrics: CodeMetrics) -> Dict:
        """Generate JavaScript API documentation"""
        api_docs = {
            'full': '# JavaScript API Documentation\n\n',
            'functions': {},
            'classes': {},
            'modules': {}
        }
        
        # Extract function definitions
        function_pattern = r'function\s+(\w+)\s*\((.*?)\)\s*\{'
        functions = re.findall(function_pattern, code)
        
        for func_name, params in functions:
            api_docs['functions'][func_name] = {
                'name': func_name,
                'parameters': [p.strip() for p in params.split(',')],
                'return_type': 'Any',
                'docstring': 'No documentation available',
                'line_number': 'N/A'
            }
        
        # Format full documentation
        if api_docs['functions']:
            api_docs['full'] += "## Functions\n\n"
            for func_name, func_docs in api_docs['functions'].items():
                api_docs['full'] += f"### {func_name}()\n"
                api_docs['full'] += f"**Parameters:** {', '.join(func_docs['parameters'])}\n"
                api_docs['full'] += f"**Return type:** {func_docs['return_type']}\n"
                api_docs['full'] += f"**Description:** {func_docs['docstring']}\n\n"
        
        return api_docs
    
    def _generate_java_api_docs(self, code: str, metrics: CodeMetrics) -> Dict:
        """Generate Java API documentation"""
        api_docs = {
            'full': '# Java API Documentation\n\n',
            'functions': {},
            'classes': {},
            'modules': {}
        }
        
        # Extract method definitions
        method_pattern = r'public\s+\w+\s+(\w+)\s*\((.*?)\)\s*\{'
        methods = re.findall(method_pattern, code)
        
        for method_name, params in methods:
            api_docs['functions'][method_name] = {
                'name': method_name,
                'parameters': [p.strip() for p in params.split(',')],
                'return_type': 'void',
                'docstring': 'No documentation available',
                'line_number': 'N/A'
            }
        
        # Format full documentation
        if api_docs['functions']:
            api_docs['full'] += "## Methods\n\n"
            for method_name, method_docs in api_docs['functions'].items():
                api_docs['full'] += f"### {method_name}()\n"
                api_docs['full'] += f"**Parameters:** {', '.join(method_docs['parameters'])}\n"
                api_docs['full'] += f"**Return type:** {method_docs['return_type']}\n"
                api_docs['full'] += f"**Description:** {method_docs['docstring']}\n\n"
        
        return api_docs
    
    def _generate_user_guide(self, code: str, language: str, metrics: CodeMetrics) -> str:
        """Generate user guide documentation"""
        guide = f"""# User Guide

## Overview

This code provides functionality for [describe purpose based on code analysis].

## Getting Started

### Prerequisites

- [List prerequisites based on code analysis]
- [Additional requirements]

### Installation

{self._generate_installation_instructions(language)}

### Usage

{self._generate_usage_examples(code, language)}

## API Reference

{self._generate_api_reference(code, language)}

## Examples

{self._generate_code_examples(code, language)}

## Troubleshooting

{self._generate_troubleshooting(code, language)}

## Contributing

[Contribution guidelines]
"""
        return guide
    
    def _generate_installation_instructions(self, language: str) -> str:
        """Generate installation instructions for the given language"""
        instructions = {
            'python': 'pip install -r requirements.txt',
            'javascript': 'npm install',
            'java': 'mvn clean install',
            'c++': 'cmake . && make',
            'c#': 'dotnet restore',
            'ruby': 'bundle install',
            'go': 'go mod tidy',
            'rust': 'cargo build',
            'php': 'composer install',
            'swift': 'swift package update',
            'kotlin': 'gradle build'
        }
        return instructions.get(language.lower(), 'Follow standard installation procedures')
    
    def _generate_usage_examples(self, code: str, language: str) -> str:
        """Generate usage examples"""
        examples = {
            'python': 'from module import function\nresult = function(input_data)',
            'javascript': 'const result = function(inputData);',
            'java': 'Result result = ClassName.method(inputData);'
        }
        return examples.get(language.lower(), 'See API reference for usage examples')
    
    def _generate_api_reference(self, code: str, language: str) -> str:
        """Generate API reference section"""
        return "Refer to the API documentation section for detailed method and class information."
    
    def _generate_code_examples(self, code: str, language: str) -> str:
        """Generate code examples"""
        return "See the examples directory for usage examples."
    
    def _generate_troubleshooting(self, code: str, language: str) -> str:
        """Generate troubleshooting section"""
        return "Common issues and their solutions are documented here."
    
    def _load_doc_templates(self) -> Dict:
        """Load documentation templates"""
        return {
            'python': {
                'function': '''def {name}({params}):
    """{docstring}
    
    Args:
        {args}
    
    Returns:
        {return_type}
    """
    {body}
''',
                'class': '''class {name}:
    """{docstring}"""
    
    def __init__(self, {init_params}):
        """Initialize {name}"""
        {init_body}
''',
                'module': '''"""
{module_name}

{description}
"""

{imports}

{functions}

{classes}
'''
            },
            'javascript': {
                'function': '''/**
 * {docstring}
 * 
 * @param {params}
 * @returns {return_type}
 */
function {name}({params}) {{
    {body}
}}
''',
                'class': '''/**
 * {docstring}
 */
class {name} {{
    /**
     * Constructor
     * @param {init_params}
     */
    constructor({init_params}) {{
        {init_body}
    }}
    
    {methods}
}}
''',
                'module': '''/**
 * {module_name}
 * 
 * {description}
 */

{imports}

{functions}

{classes}
'''
            },
            'java': {
                'method': '''/**
 * {docstring}
 * 
 * @param {params}
 * @return {return_type}
 */
public {return_type} {name}({params}) {{
    {body}
}}
''',
                'class': '''/**
 * {docstring}
 */
public class {name} {{
    /**
     * Constructor
     * @param {init_params}
     */
    public {name}({init_params}) {{
        {init_body}
    }}
    
    {methods}
}}
''',
                'interface': '''/**
 * {docstring}
 */
public interface {name} {{
    {methods}
}}
'''
            }
        }


# Example usage
if __name__ == "__main__":
    doc_generator = DocumentationGenerator()
    
    # Test Python code documentation
    python_code = '''
    def sort_numbers(numbers):
        """Sort a list of numbers in ascending order"""
        return sorted(numbers)
    
    def calculate_sum(numbers):
        """Calculate the sum of a list of numbers"""
        result = 0
        for num in numbers:
            result += num
        return result
    '''
    
    result = doc_generator.generate_documentation(python_code, 'python')
    print("Documentation Generation Results:")
    print("Full Documentation:")
    print(result.documentation)
    print("\nAPI Docs:")
    print(result.api_docs)
    print("\nUser Guide:")
    print(result.user_guide)