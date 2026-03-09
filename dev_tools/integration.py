"""
Zeal Code - Development Tools Integration (Phase 3)
Integration with VS Code, JetBrains, and other development tools
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import os


@dataclass
class ToolConfig:
    """Configuration for a development tool"""
    tool_name: str
    tool_type: str  # 'ide', 'editor', 'cli'
    supported_languages: List[str]
    config_schema: Dict[str, Any]
    integration_commands: List[str]


class DevelopmentToolsIntegrator:
    """Manage integration with various development tools"""

    def __init__(self):
        """Initialize development tools integrator"""
        self.supported_tools: Dict[str, ToolConfig] = {}
        self.active_integrations: Dict[str, Dict] = {}
        self._initialize_tool_configs()

    def _initialize_tool_configs(self):
        """Initialize supported development tool configurations"""

        # VS Code
        self.supported_tools['vscode'] = ToolConfig(
            tool_name='Visual Studio Code',
            tool_type='ide',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'swift', 'kotlin'],
            config_schema={
                'extension_id': 'zeal-code.extension',
                'api_version': '1.0.0',
                'commands': {
                    'analyze': 'cca.analyze',
                    'generate': 'cca.generate',
                    'review': 'cca.review',
                    'debug': 'cca.debug'
                }
            },
            integration_commands=[
                'code --install-extension',
                'code --list-extensions'
            ]
        )

        # JetBrains (generic)
        self.supported_tools['jetbrains'] = ToolConfig(
            tool_name='JetBrains IDEs',
            tool_type='ide',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'kotlin'],
            config_schema={
                'plugin_id': 'com.zealcode.plugin',
                'plugin_version': '1.0.0',
                'supported_ides': [
                    'PyCharm', 'IntelliJ IDEA', 'WebStorm', 'CLion',
                    'DataGrip', 'RubyMine', 'AppCode', 'GoLand'
                ]
            },
            integration_commands=[
                'plugin install',
                'plugin list'
            ]
        )

        # Vim/Neovim
        self.supported_tools['vim'] = ToolConfig(
            tool_name='Vim/Neovim',
            tool_type='editor',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'kotlin'],
            config_schema={
                'plugin_manager': 'vim-plug',
                'plugin_repository': 'https://github.com/zeal-code/vim-plugin',
                'commands': {
                    'analyze': ':CCAAnalyze',
                    'generate': ':CCAGenerate',
                    'review': ':CCAReview'
                }
            },
            integration_commands=[
                'vim +PluginInstall +qall',
                'nvim +PluginInstall +qall'
            ]
        )

        # Sublime Text
        self.supported_tools['sublime'] = ToolConfig(
            tool_name='Sublime Text',
            tool_type='editor',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'php'],
            config_schema={
                'plugin_path': 'Packages/ZealCode',
                'plugin_repository': 'https://github.com/zeal-code/sublime-plugin',
                'commands': {
                    'analyze': 'ctrl+shift+a',
                    'generate': 'ctrl+shift+g',
                    'review': 'ctrl+shift+r'
                }
            },
            integration_commands=[
                'subl --install-package'
            ]
        )

        # Atom (legacy)
        self.supported_tools['atom'] = ToolConfig(
            tool_name='Atom',
            tool_type='editor',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'php'],
            config_schema={
                'plugin_name': 'zeal-code',
                'plugin_repository': 'https://github.com/zeal-code/atom-plugin',
                'commands': {
                    'analyze': 'ctrl-alt-a',
                    'generate': 'ctrl-alt-g',
                    'review': 'ctrl-alt-r'
                }
            },
            integration_commands=[
                'apm install'
            ]
        )

        # CLI Tools
        self.supported_tools['cli'] = ToolConfig(
            tool_name='Command Line Interface',
            tool_type='cli',
            supported_languages=['python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin'],
            config_schema={
                'command': 'cca',
                'subcommands': {
                    'analyze': 'Analyze code file',
                    'generate': 'Generate code from prompt',
                    'review': 'Review code quality',
                    'debug': 'Debug code issues',
                    'docs': 'Generate documentation',
                    'fix': 'Fix code issues'
                },
                'output_formats': ['json', 'text', 'markdown'],
                'config_file': '~/.cca/config.json'
            },
            integration_commands=[
                'cca --help',
                'cca --version'
            ]
        )

    def get_supported_tools(self) -> Dict[str, ToolConfig]:
        """Get all supported development tools"""
        return self.supported_tools

    def get_tool_config(self, tool_id: str) -> Optional[ToolConfig]:
        """Get configuration for a specific tool"""
        return self.supported_tools.get(tool_id)

    def install_integration(self, tool_id: str, config: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Install integration for a development tool

        Args:
            tool_id: Tool identifier
            config: Optional configuration for the tool

        Returns:
            (success, message)
        """
        tool = self.supported_tools.get(tool_id)
        if not tool:
            return False, f"Tool {tool_id} not supported"

        # In a real implementation, this would execute the installation commands
        self.active_integrations[tool_id] = {
            'tool': tool,
            'config': config or tool.config_schema,
            'installed_at': None,  # Would be timestamp in real implementation
            'status': 'installed'
        }

        return True, f"Integration for {tool.tool_name} installed successfully"

    def uninstall_integration(self, tool_id: str) -> Tuple[bool, str]:
        """
        Uninstall integration for a development tool

        Args:
            tool_id: Tool identifier

        Returns:
            (success, message)
        """
        if tool_id not in self.active_integrations:
            return False, f"Integration for {tool_id} not installed"

        del self.active_integrations[tool_id]
        return True, f"Integration for {tool_id} uninstalled successfully"

    def get_active_integrations(self) -> Dict[str, Dict]:
        """Get all active integrations"""
        return self.active_integrations

    def generate_vscode_extension_manifest(self) -> Dict[str, Any]:
        """Generate VS Code extension manifest"""
        return {
            "name": "zeal-code",
            "displayName": "Zeal Code",
            "description": "AI-powered code analysis, generation, and review",
            "version": "1.0.0",
            "publisher": "valzeal",
            "engines": {
                "vscode": "^1.0.0"
            },
            "categories": [
                "Programming Languages",
                "Snippets",
                "Linters",
                "Formatters"
            ],
            "activationEvents": [
                "onLanguage:python",
                "onLanguage:javascript",
                "onLanguage:typescript",
                "onLanguage:java",
                "onLanguage:cpp",
                "onLanguage:csharp",
                "onLanguage:go",
                "onLanguage:rust",
                "onLanguage:php"
            ],
            "main": "./extension.js",
            "contributes": {
                "commands": [
                    {
                        "command": "cca.analyze",
                        "title": "Zeal Code: Analyze Code"
                    },
                    {
                        "command": "cca.generate",
                        "title": "Zeal Code: Generate Code"
                    },
                    {
                        "command": "cca.review",
                        "title": "Zeal Code: Review Code"
                    },
                    {
                        "command": "cca.debug",
                        "title": "Zeal Code: Debug Code"
                    }
                ],
                "keybindings": [
                    {
                        "command": "cca.analyze",
                        "key": "ctrl+shift+a",
                        "mac": "cmd+shift+a"
                    },
                    {
                        "command": "cca.generate",
                        "key": "ctrl+shift+g",
                        "mac": "cmd+shift+g"
                    }
                ],
                "configuration": {
                    "title": "Zeal Code",
                    "properties": {
                        "cca.apiKey": {
                            "type": "string",
                            "default": "",
                            "description": "API key for authentication"
                        },
                        "cca.serverUrl": {
                            "type": "string",
                            "default": "http://localhost:8000",
                            "description": "Server URL for API calls"
                        },
                        "cca.cacheEnabled": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable caching for better performance"
                        },
                        "cca.autoAnalyze": {
                            "type": "boolean",
                            "default": False,
                            "description": "Automatically analyze code on save"
                        }
                    }
                }
            }
        }

    def generate_cli_help(self) -> str:
        """Generate CLI help text"""
        help_text = """
Zeal Code - Command Line Interface
================================================

Usage: cca [command] [options]

Commands:
  analyze <file>          Analyze code file or directory
  generate <prompt>         Generate code from natural language prompt
  review <file>            Review code quality and suggest improvements
  debug <file>             Debug code and identify issues
  docs <file>              Generate documentation for code
  fix <file>               Automatically fix code issues

Options:
  --language <lang>        Specify programming language
  --output <format>         Output format: json, text, markdown (default: text)
  --cache                  Enable caching
  --no-cache               Disable caching
  --config <file>          Use custom config file
  --verbose                Show detailed output
  --quiet                  Suppress output (errors only)
  --help                   Show this help message
  --version                Show version information

Examples:
  cca analyze script.py
  cca generate "Create a function to sort an array"
  cca review app.js --language javascript --output json
  cca debug server.py --verbose

Configuration:
  Config file: ~/.cca/config.json

  Example config:
  {
    "apiKey": "your_api_key_here",
    "serverUrl": "http://localhost:8000",
    "cacheEnabled": true,
    "defaultLanguage": "python",
    "defaultOutputFormat": "text"
  }

For more information, visit: https://github.com/valzeal/zeal-code
"""
        return help_text

    def generate_plugin_documentation(self, tool_id: str) -> Optional[str]:
        """
        Generate documentation for a plugin

        Args:
            tool_id: Tool identifier

        Returns:
            Documentation string or None
        """
        tool = self.supported_tools.get(tool_id)
        if not tool:
            return None

        doc = f"""
{tool.tool_name} Plugin - Zeal Code
{'=' * (len(tool.tool_name) + 30)}

Supported Languages: {', '.join(tool.supported_languages)}

Installation:
"""
        if tool.tool_type == 'ide':
            doc += f"  1. Install the plugin from your IDE's plugin marketplace\n"
            doc += f"  2. Search for 'Zeal Code'\n"
            doc += f"  3. Click Install and restart your IDE\n"
        elif tool.tool_type == 'editor':
            doc += f"  1. Follow the installation instructions at:\n"
            doc += f"     {tool.config_schema.get('plugin_repository', '')}\n"
            doc += f"  2. Configure your editor settings\n"
        elif tool.tool_type == 'cli':
            doc += f"  1. Download the CLI tool from:\n"
            doc += f"     https://github.com/valzeal/zeal-code/releases\n"
            doc += f"  2. Extract and add to your PATH\n"

        doc += f"""
Configuration:
"""
        for key, value in tool.config_schema.items():
            doc += f"  {key}: {value}\n"

        doc += f"""
Commands:
"""
        for command_name, command_desc in tool.config_schema.get('commands', {}).items():
            doc += f"  {command_name}: {command_desc}\n"

        doc += f"""
For more information and advanced usage, see the documentation at:
https://github.com/valzeal/zeal-code/wiki
"""
        return doc

    def export_integrations_config(self, filepath: str) -> Tuple[bool, str]:
        """
        Export all integration configurations to a file

        Args:
            filepath: Path to output file

        Returns:
            (success, message)
        """
        try:
            config = {
                'supported_tools': {
                    tool_id: {
                        'name': tool.tool_name,
                        'type': tool.tool_type,
                        'supported_languages': tool.supported_languages
                    }
                    for tool_id, tool in self.supported_tools.items()
                },
                'active_integrations': self.active_integrations
            }

            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)

            return True, f"Configuration exported to {filepath}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"


# Example usage
if __name__ == "__main__":
    integrator = DevelopmentToolsIntegrator()

    # List supported tools
    print("Supported Development Tools:")
    for tool_id, tool in integrator.get_supported_tools().items():
        print(f"  {tool_id}: {tool.tool_name} ({tool.tool_type})")
        print(f"    Languages: {', '.join(tool.supported_languages)}")

    # Install VS Code integration
    success, message = integrator.install_integration('vscode')
    print(f"\nInstall VS Code integration: {success}, {message}")

    # Generate VS Code extension manifest
    manifest = integrator.generate_vscode_extension_manifest()
    print(f"\nVS Code Extension Manifest (first 500 chars):")
    print(json.dumps(manifest, indent=2)[:500] + '...')

    # Generate CLI help
    cli_help = integrator.generate_cli_help()
    print(f"\nCLI Help (first 300 chars):")
    print(cli_help[:300] + '...')

    # Generate plugin documentation
    vim_doc = integrator.generate_plugin_documentation('vim')
    print(f"\nVim Plugin Documentation (first 400 chars):")
    print(vim_doc[:400] + '...')

    # Export integrations config
    success, message = integrator.export_integrations_config('/tmp/cca-integrations.json')
    print(f"\nExport config: {success}, {message}")

    # Get active integrations
    active = integrator.get_active_integrations()
    print(f"\nActive integrations: {list(active.keys())}")
