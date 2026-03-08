"""
Claude Code Alternative - Web User Interface
Basic web interface for the code assistant
"""

import streamlit as st
from typing import Dict, List, Optional
import json
import textwrap


class WebInterface:
    """Web interface for the code assistant"""
    
    def __init__(self):
        """Initialize web interface"""
        self.setup_page()
    
    def setup_page(self):
        """Setup the Streamlit page"""
        st.set_page_config(
            page_title="Claude Code Alternative",
            page_icon="🚀",
            layout="wide"
        )
        
        # Custom CSS
        st.markdown("""
            <style>
            .main {
                background-color: #f0f2f6;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def render_home_page(self):
        """Render the home page"""
        st.title("🚀 Claude Code Alternative")
        st.subheader("Your AI-powered code assistant")
        
        # Introduction
        st.markdown("""
        Welcome to Claude Code Alternative! This AI-powered assistant helps you:
        - Generate code from natural language
        - Review and improve existing code
        - Debug and test your code
        - Generate documentation automatically
        """)
        
        # Features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📝 Code Generation")
            st.markdown("Generate code from simple English descriptions")
        
        with col2:
            st.markdown("### 🔍 Code Review")
            st.markdown("Automatically analyze and improve your code")
        
        with col3:
            st.markdown("### 🐛 Debugging")
            st.markdown("Find and fix bugs in your code")
        
        # Quick actions
        st.markdown("### Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Generate Code", key="generate_code"):
                self.show_code_generation_interface()
        
        with col2:
            if st.button("Review Code", key="review_code"):
                self.show_code_review_interface()
        
        # Recent activity
        st.markdown("### Recent Activity")
        self.show_recent_activity()
    
    def show_code_generation_interface(self):
        """Show code generation interface"""
        st.header("📝 Generate Code")
        
        # Input form
        with st.form("code_generation_form"):
            language = st.selectbox(
                "Programming Language",
                ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Swift", "Kotlin", "TypeScript"]
            )
            
            request = st.text_area(
                "Describe what you want to generate",
                placeholder="e.g., Write a Python function to sort a list of numbers",
                height=100
            )
            
            submitted = st.form_submit_button("Generate Code")
            
            if submitted and request:
                self.generate_code(language.lower(), request)
    
    def show_code_review_interface(self):
        """Show code review interface"""
        st.header("🔍 Review Code")
        
        # Input form
        with st.form("code_review_form"):
            language = st.selectbox(
                "Programming Language",
                ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "PHP", "Swift", "Kotlin", "TypeScript"]
            )
            
            code = st.text_area(
                "Paste your code here",
                placeholder="Enter or paste your code for review...",
                height=300
            )
            
            submitted = st.form_submit_button("Review Code")
            
            if submitted and code:
                self.review_code(language.lower(), code)
    
    def generate_code(self, language: str, request: str):
        """Generate code based on request"""
        st.info("Generating code... Please wait.")
        
        # Simulate code generation (in real implementation, this would call the code generator)
        generated_code = self._simulate_code_generation(language, request)
        
        # Display results
        st.subheader("Generated Code")
        st.code(generated_code, language=language.lower())
        
        # Download button
        st.download_button(
            label="Download Code",
            data=generated_code,
            file_name=f"generated_{language.lower()}_code.py",
            mime="text/plain"
        )
        
        # Analysis
        st.subheader("Code Analysis")
        analysis = self._analyze_generated_code(generated_code, language)
        st.json(analysis)
    
    def review_code(self, language: str, code: str):
        """Review code and provide analysis"""
        st.info("Analyzing code... Please wait.")
        
        # Simulate code review (in real implementation, this would call the code reviewer)
        review_result = self._simulate_code_review(code, language)
        
        # Display results
        st.subheader("Code Review Results")
        
        # Issues
        if review_result['issues']:
            st.warning("Issues Found:")
            for issue in review_result['issues']:
                st.markdown(f"**{issue['type'].upper()}**: {issue['message']}")
                st.markdown(f"*{issue['suggestion']}*")
        else:
            st.success("No major issues found!")
        
        # Suggestions
        if review_result['suggestions']:
            st.info("Suggestions:")
            for suggestion in review_result['suggestions']:
                st.markdown(f"- {suggestion['message']}")
        
        # Refactored code
        if review_result['refactored_code']:
            st.subheader("Refactored Code")
            st.code(review_result['refactored_code'], language=language.lower())
            
            st.download_button(
                label="Download Refactored Code",
                data=review_result['refactored_code'],
                file_name=f"refactored_{language.lower()}_code.py",
                mime="text/plain"
            )
    
    def _simulate_code_generation(self, language: str, request: str) -> str:
        """Simulate code generation (placeholder)"""
        # In real implementation, this would call the actual code generator
        return f"# Generated {language.capitalize()} Code\n\n# Based on request: {request}\n\ndef example_function():\n    \"\"\"Example function\"\"\"\n    return \"Generated code\"\n"
    
    def _simulate_code_review(self, code: str, language: str) -> Dict:
        """Simulate code review (placeholder)"""
        # In real implementation, this would call the actual code reviewer
        return {
            'issues': [
                {
                    'type': 'complexity',
                    'message': 'Function is too complex',
                    'suggestion': 'Consider breaking into smaller functions'
                }
            ],
            'suggestions': [
                {
                    'type': 'documentation',
                    'message': 'Add docstrings to functions'
                }
            ],
            'refactored_code': code + '\n\n# Added docstring\n\ndef example_function():\n    \"\"\"Example function with docstring\"\"\"\n    return \"Refactored code\"'
        }
    
    def _analyze_generated_code(self, code: str, language: str) -> Dict:
        """Analyze generated code"""
        # Simple analysis (in real implementation, this would be more comprehensive)
        lines = code.split('\n')
        functions = len([line for line in lines if 'def ' in line or 'function ' in line])
        classes = len([line for line in lines if 'class ' in line])
        
        return {
            'language': language,
            'lines_of_code': len(lines),
            'functions_count': functions,
            'classes_count': classes,
            'complexity_score': functions * 2,
            'confidence': 0.85
        }
    
    def show_recent_activity(self):
        """Show recent activity"""
        activities = [
            {"action": "Generated Python code", "time": "2 minutes ago"},
            {"action": "Reviewed JavaScript code", "time": "15 minutes ago"},
            {"action": "Fixed bug in Java code", "time": "1 hour ago"}
        ]
        
        for activity in activities:
            st.markdown(f"- **{activity['action']}** ({activity['time']})")


# Example usage
if __name__ == "__main__":
    interface = WebInterface()
    interface.render_home_page()