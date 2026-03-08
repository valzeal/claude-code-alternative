"""
Claude Code Alternative - Code Generation Engine
Generates code from natural language prompts and requirements
"""

import ast
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import textwrap


@dataclass
class CodeGenerationResult:
    """Code generation result with metadata"""
    code: str
    language: str
    confidence: float
    generated_functions: List[str]
    complexity_score: float
    suggestions: List[str]


class CodeGenerator:
    """Core code generation functionality"""
    
    def __init__(self):
        """Initialize code generator"""
        self.language_templates = {
            'python': self._generate_python,
            'javascript': self._generate_javascript,
            'java': self._generate_java,
            'c++': self._generate_cpp,
            'c#': self._generate_csharp,
            'ruby': self._generate_ruby,
            'go': self._generate_go,
            'rust': self._generate_rust,
            'php': self._generate_php,
            'swift': self._generate_swift,
            'kotlin': self._generate_kotlin,
            'typescript': self._generate_typescript
        }
    
    def generate_code(self, request: str, language: str = 'python') -> CodeGenerationResult:
        """Generate code based on natural language request"""
        generator = self.language_templates.get(language.lower())
        if not generator:
            raise ValueError(f"Unsupported language: {language}")
        
        try:
            result = generator(request)
            return CodeGenerationResult(
                code=result['code'],
                language=language,
                confidence=result['confidence'],
                generated_functions=result['functions'],
                complexity_score=result['complexity'],
                suggestions=result.get('suggestions', [])
            )
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")
    
    def _analyze_request(self, request: str) -> Dict:
        """Analyze natural language request for code generation"""
        # Extract function name and parameters
        function_pattern = r'(function|class|def|func)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(?(.*?)\)?'
        matches = re.findall(function_pattern, request, re.IGNORECASE)
        
        # Extract language if specified
        language = None
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
            if re.search(pattern, request, re.IGNORECASE):
                language = lang
                break
        
        # Extract requirements and functionality
        requirements = []
        functionality_words = ['sort', 'calculate', 'find', 'search', 'filter', 'process', 'transform', 
                             'validate', 'parse', 'serialize', 'deserialize', 'connect', 'query',
                             'update', 'delete', 'create', 'read', 'write', 'append', 'remove']
        
        for word in functionality_words:
            if word in request.lower():
                requirements.append(word)
        
        return {
            'language': language,
            'functions': [match[1] for match in matches],
            'parameters': [match[2] for match in matches],
            'requirements': requirements,
            'confidence': 0.8  # Default confidence
        }
    
    def _generate_python(self, request: str) -> Dict:
        """Generate Python code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        # Generate function definitions
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            # Determine function body based on requirements
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return sorted({params})
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    # Calculate result based on input parameters
                    result = 0
                    for item in {params}:
                        result += item
                    return result
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    # Find items matching criteria
                    results = []
                    for item in {params}:
                        if item == target:
                            results.append(item)
                    return results
                ''')
            else:
                body = textwrap.dedent(f'''\
                    # Function implementation
                    result = None
                    return result
                ''')
            
            # Create function definition
            func_code = textwrap.dedent(f'''\
                def {func_name}({params}):
                    {body}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        # Add main execution block if requested
        if 'main' in request.lower() or 'test' in request.lower():
            code_lines.append(textwrap.dedent('''
                if __name__ == "__main__":
                    # Test the generated functions
                    print("Testing generated code...")
            '''))
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 2,
            'suggestions': ['Consider adding type hints', 'Add error handling']
        }
    
    def _generate_javascript(self, request: str) -> Dict:
        """Generate JavaScript code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.sort();
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    let result = 0;
                    for (const item of {params}) {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    const results = [];
                    for (const item of {params}) {{
                        if (item === target) {{
                            results.push(item);
                        }}
                    }}
                    return results;
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    const result = null;
                    return result;
                ''')
            
            func_code = textwrap.dedent(f'''\
                function {func_name}({params}) {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.5,
            'suggestions': ['Consider using arrow functions', 'Add input validation']
        }
    
    def _generate_java(self, request: str) -> Dict:
        """Generate Java code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return Arrays.stream({params}).sorted().toArray();
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    int result = 0;
                    for (int item : {params}) {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    List<Integer> results = new ArrayList<>();
                    for (int item : {params}) {{
                        if (item == target) {{
                            results.add(item);
                        }}
                    }}
                    return results;
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return null;
                ''')
            
            func_code = textwrap.dedent(f'''\
                public {self._get_java_return_type(requirements)} {func_name}({params}) {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 2,
            'suggestions': ['Add proper error handling', 'Consider generics']
        }
    
    def _get_java_return_type(self, requirements: List[str]) -> str:
        """Determine appropriate Java return type based on requirements"""
        if 'sort' in requirements or 'calculate' in requirements:
            return 'int[]'
        elif 'find' in requirements or 'search' in requirements:
            return 'List<Integer>'
        else:
            return 'Object'
    
    def _generate_cpp(self, request: str) -> Dict:
        """Generate C++ code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    std::sort({params}.begin(), {params}.end());
                    return {params};
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    int result = 0;
                    for (int item : {params}) {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    std::vector<int> results;
                    for (int item : {params}) {{
                        if (item == target) {{
                            results.push_back(item);
                        }}
                    }}
                    return results;
                ''')
            else:
                body = textwrap.dedent('''\
                    // Function implementation
                    return {};
                ''')
            
            func_code = textwrap.dedent(f'''\
                std::vector<int> {func_name}({params}) {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.8,
            'suggestions': ['Add proper error handling', 'Consider using templates']
        }
    
    def _generate_csharp(self, request: str) -> Dict:
        """Generate C# code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.OrderBy(x => x).ToArray();
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    int result = 0;
                    foreach (var item in {params}) {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    var results = new List<int>();
                    foreach (var item in {params}) {{
                        if (item == target) {{
                            results.Add(item);
                        }}
                    }}
                    return results.ToArray();
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return null;
                ''')
            
            func_code = textwrap.dedent(f'''\
                public {self._get_csharp_return_type(requirements)} {func_name}({params}) {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.7,
            'suggestions': ['Add proper error handling', 'Consider using LINQ']
        }
    
    def _get_csharp_return_type(self, requirements: List[str]) -> str:
        """Determine appropriate C# return type based on requirements"""
        if 'sort' in requirements or 'calculate' in requirements:
            return 'int[]'
        elif 'find' in requirements or 'search' in requirements:
            return 'int[]'
        else:
            return 'object'
    
    def _generate_ruby(self, request: str) -> Dict:
        """Generate Ruby code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.sort
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    result = 0
                    {params}.each do |item|
                        result += item
                    end
                    return result
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    results = []
                    {params}.each do |item|
                        if item == target
                            results << item
                        end
                    end
                    return results
                ''')
            else:
                body = textwrap.dedent(f'''\
                    # Function implementation
                    result = nil
                    return result
                ''')
            
            func_code = textwrap.dedent(f'''\
                def {func_name}({params})
                    {body}
                end
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.6,
            'suggestions': ['Add proper error handling', 'Consider using blocks']
        }
    
    def _generate_go(self, request: str) -> Dict:
        """Generate Go code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    sort.Ints({params})
                    return {params}
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    result := 0
                    for _, item := range {params} {{
                        result += item
                    }}
                    return result
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    var results []int
                    for _, item := range {params} {{
                        if item == target {{
                            results = append(results, item)
                        }}
                    }}
                    return results
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return nil
                ''')
            
            func_code = textwrap.dedent(f'''\
                func {func_name}({params}) []int {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.5,
            'suggestions': ['Add proper error handling', 'Consider using interfaces']
        }
    
    def _generate_rust(self, request: str) -> Dict:
        """Generate Rust code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    {params}.sort();
                    return {params};
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    let mut result = 0;
                    for item in {params}.iter() {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    let mut results = Vec::new();
                    for item in {params}.iter() {{
                        if *item == target {{
                            results.push(*item);
                        }}
                    }}
                    return results;
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return None;
                ''')
            
            func_code = textwrap.dedent(f'''\
                fn {func_name}({params}) -> Vec<i32> {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.4,
            'suggestions': ['Add proper error handling', 'Consider using Result type']
        }
    
    def _generate_php(self, request: str) -> Dict:
        """Generate PHP code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params};
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    $result = 0;
                    foreach ($params as $item) {{
                        $result += $item;
                    }}
                    return $result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    $results = [];
                    foreach ($params as $item) {{
                        if ($item == $target) {{
                            $results[] = $item;
                        }}
                    }}
                    return $results;
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return null;
                ''')
            
            func_code = textwrap.dedent(f'''\
                function {func_name}({params}) {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.6,
            'suggestions': ['Add proper error handling', 'Consider type hints']
        }
    
    def _generate_swift(self, request: str) -> Dict:
        """Generate Swift code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.sorted()
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    var result = 0
                    for item in {params} {{
                        result += item
                    }}
                    return result
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    var results: [Int] = []
                    for item in {params} {{
                        if item == target {{
                            results.append(item)
                        }}
                    }}
                    return results
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return nil
                ''')
            
            func_code = textwrap.dedent(f'''\
                func {func_name}({params}) -> [Int] {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.5,
            'suggestions': ['Add proper error handling', 'Consider using optionals']
        }
    
    def _generate_kotlin(self, request: str) -> Dict:
        """Generate Kotlin code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.sorted()
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    var result = 0
                    for (item in {params}) {{
                        result += item
                    }}
                    return result
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    val results = mutableListOf<Int>()
                    for (item in {params}) {{
                        if (item == target) {{
                            results.add(item)
                        }}
                    }}
                    return results
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return null
                ''')
            
            func_code = textwrap.dedent(f'''\
                fun {func_name}({params}): List<Int> {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.6,
            'suggestions': ['Add proper error handling', 'Consider using nullable types']
        }
    
    def _generate_typescript(self, request: str) -> Dict:
        """Generate TypeScript code"""
        analysis = self._analyze_request(request)
        functions = analysis['functions']
        parameters = analysis['parameters']
        requirements = analysis['requirements']
        
        code_lines = []
        generated_functions = []
        
        for i, func_name in enumerate(functions):
            params = parameters[i] if i < len(parameters) else ''
            
            if 'sort' in requirements:
                body = textwrap.dedent(f'''\
                    return {params}.sort();
                ''')
            elif 'calculate' in requirements:
                body = textwrap.dedent(f'''\
                    let result = 0;
                    for (const item of {params}) {{
                        result += item;
                    }}
                    return result;
                ''')
            elif 'find' in requirements or 'search' in requirements:
                body = textwrap.dedent(f'''\
                    const results: number[] = [];
                    for (const item of {params}) {{
                        if (item === target) {{
                            results.push(item);
                        }}
                    }}
                    return results;
                ''')
            else:
                body = textwrap.dedent(f'''\
                    // Function implementation
                    return null;
                ''')
            
            func_code = textwrap.dedent(f'''\
                function {func_name}({params}): number[] {{
                    {body}
                }}
            ''')
            
            code_lines.append(func_code)
            generated_functions.append(func_name)
        
        code = '\n\n'.join(code_lines)
        
        return {
            'code': code,
            'functions': generated_functions,
            'confidence': analysis['confidence'],
            'complexity': len(generated_functions) * 1.5,
            'suggestions': ['Add proper error handling', 'Consider using type annotations']
        }


# Example usage
if __name__ == "__main__":
    generator = CodeGenerator()
    
    # Test Python code generation
    request = "Write a Python function to sort a list of numbers"
    result = generator.generate_code(request, 'python')
    
    print("Generated Python Code:")
    print(result.code)
    print(f"\nGenerated Functions: {result.generated_functions}")
    print(f"Confidence: {result.confidence}")
    print(f"Complexity: {result.complexity_score}")
    print(f"Suggestions: {result.suggestions}")