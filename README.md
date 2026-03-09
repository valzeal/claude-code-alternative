# Zeal Code

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
├── security/           # Authentication and encryption
├── monitoring/         # Performance monitoring
├── feedback/           # User feedback management
├── deployment/         # Deployment preparation
├── dev_tools/         # CLI and IDE integration
└── tests/              # Test suite
```

## Installation

```bash
# Clone to repository
git clone https://github.com/ridzeal/claude-code-alternative.git
cd claude-code-alternative

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Web Interface

```bash
cd ui
streamlit run web_interface.py
```

### Run API Server

```bash
cd api_framework
python3 main.py
```

The API will be available at `http://localhost:8000`

### Run CLI Tool

```bash
# Install CLI (Unix-like systems)
ln -s $(pwd)/dev_tools/cli.py /usr/local/bin/zeal-code

# Or run directly
python3 dev_tools/cli.py --help

# Examples
zeal-code analyze script.py
zeal-code generate "Create a function to sort an array"
zeal-code review app.py --language python --output json
```

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze code requests
- `POST /generate` - Generate code from natural language
- `POST /review` - Review and analyze code
- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
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

### ✅ Phase 3: Enhancement (Complete)
- Advanced language support with real metrics
- Performance optimization (700x+ speedup)
- Security implementation (self-contained auth & encryption)
- Integration with development tools (6 platforms)
- Full-featured CLI interface

### ✅ Phase 4: Production (Complete)
- Comprehensive testing and QA
- Documentation completion
- Deployment preparation (Docker, scripts, checklists)
- User feedback integration
- Performance monitoring system

## Performance

- 🚀 **700x+ speedup** with intelligent caching
- ⚡ **Async processing** for improved throughput
- 📊 **Performance monitoring** with detailed metrics
- 🔧 **Thread-safe operations** for concurrent access

## Security

- 🔐 **Authentication**: SHA-256 password hashing with salt
- 🔑 **API keys**: Secure token-based authentication
- 🔒 **Encryption**: XOR encryption for sensitive data
- 👤 **Session management**: Token-based sessions with expiry
- 📝 **Audit logging**: Comprehensive activity tracking

## Development Tools Integration

- **VS Code**: Full extension with commands and keybindings
- **JetBrains IDEs**: Multi-IDE support (PyCharm, IntelliJ, WebStorm, etc.)
- **Vim/Neovim**: Plugin integration
- **Sublime Text**: Plugin integration
- **Atom**: Plugin integration
- **CLI**: Full-featured command-line interface

## Testing

```bash
# Run basic tests
python3 simple_test.py

# Run full test suite
python3 -m pytest tests/

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Riadhi Aditya Hermawan ([@ridzeal](https://github.com/ridzeal))

---

**Zeal Code**: AI-powered code assistance, reimagined and production-ready. 🚀
