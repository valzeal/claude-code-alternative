# Claude Code Alternative

An AI-powered code assistant for generating, reviewing, and debugging code across multiple programming languages.

## Features

- 🚀 **Code Generation**: Generate code from natural language prompts
- 🔍 **Code Review**: Analyze code quality and suggest improvements
- 🐛 **Debugging**: Identify bugs and generate test cases
- 📝 **Documentation**: Auto-generate documentation from code
- 🌐 **Multi-language Support**: 12+ programming languages
- 🖥️ **Web Interface**: Streamlit-based UI for easy interaction
- 🔌 **REST API**: FastAPI backend for integration

## Supported Languages

- Python
- JavaScript
- TypeScript
- Java
- C++
- C#
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin

## Project Structure

```
claude-code-alternative/
├── api_framework/      # FastAPI REST API
├── code_analysis/      # Code analysis engine
├── code_generation/    # Multi-language code generator
├── code_review/        # Code review module
├── debugging/          # Debugging assistant
├── documentation/      # Documentation generator
├── nlp_module/         # Natural language processing
├── ui/                 # Streamlit web interface
└── tests/              # Test suite
```

## Installation

```bash
# Clone the repository
git clone https://github.com/ridzeal/claude-code-alternative.git
cd claude-code-alternative

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Web Interface

```bash
cd ui
streamlit run web_interface.py
```

### Run the API Server

```bash
cd api_framework
python3 main.py
```

The API will be available at `http://localhost:8000`

### Test Code Generation

```bash
python3 simple_test.py
```

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze code requests
- `POST /generate` - Generate code from natural language
- `POST /review` - Review and analyze code
- `GET /health` - Service health check

## Development Status

### ✅ Phase 1: Foundation (Complete)
- Requirements analysis
- Modular architecture design
- Technical stack selection

### ✅ Phase 2: Core Functionality (Complete)
- Code generation engine
- Code review module
- Debugging module
- Documentation module
- Basic user interface
- API integration

### 🚧 Phase 3: Enhancement (In Progress)
- Advanced language support
- Performance optimization
- Security implementation
- Integration with development tools

### 📋 Phase 4: Production (Planned)
- Comprehensive testing and QA
- Documentation completion
- Deployment preparation
- User feedback integration

## Testing

```bash
# Run basic tests
python3 simple_test.py

# Run full test suite
python3 -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Riadhi Aditya Hermawan ([@ridzeal](https://github.com/ridzeal))

## Acknowledgments

Built as an alternative to Claude Code with focus on open-source accessibility and multi-language support.
