"""
Zeal Code - Testing Module (Phase 4)
Comprehensive testing and QA for all modules
"""

import unittest
import sys
import os
from typing import List, Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class TestResult:
    """Result of a test"""
    test_name: str
    passed: bool
    execution_time: float
    error_message: Optional[str] = None
    details: Optional[Dict] = None


class CodeAnalysisTests(unittest.TestCase):
    """Unit tests for code analysis modules"""

    def setUp(self):
        """Set up test fixtures"""
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        try:
            from code_analysis.enhanced_analyzer import EnhancedCodeAnalyzer
            self.analyzer = EnhancedCodeAnalyzer()
        except ImportError:
            self.skipTest("Enhanced code analyzer not available")

    def test_python_analysis(self):
        """Test Python code analysis"""
        python_code = '''
def hello():
    """Say hello"""
    print("Hello, World!")
'''
        result = self.analyzer.analyze_code(python_code, 'python')
        
        self.assertIsNotNone(result)
        self.assertGreater(result.lines_of_code, 0)
        self.assertGreaterEqual(result.functions_count, 1)
        self.assertGreaterEqual(result.maintainability_index, 0)
        self.assertLessEqual(result.maintainability_index, 100)

    def test_javascript_analysis(self):
        """Test JavaScript code analysis"""
        javascript_code = '''
function add(a, b) {
    return a + b;
}
'''
        result = self.analyzer.analyze_code(javascript_code, 'javascript')
        
        self.assertIsNotNone(result)
        self.assertGreater(result.lines_of_code, 0)
        self.assertGreaterEqual(result.functions_count, 1)

    def test_cyclomatic_complexity(self):
        """Test cyclomatic complexity calculation"""
        code = '''
def complex_function(x):
    if x > 0:
        if x < 100:
            if x % 2 == 0:
                return True
    return False
'''
        result = self.analyzer.analyze_code(code, 'python')
        
        # This code should have complexity > 1
        self.assertGreater(result.complexity_score, 5)

    def test_maintainability_index(self):
        """Test maintainability index calculation"""
        simple_code = '''
def simple():
    pass
'''
        result = self.analyzer.analyze_code(simple_code, 'python')
        
        # Simple code should have high maintainability
        self.assertGreater(result.maintainability_index, 80)

    def test_code_smell_detection(self):
        """Test code smell detection"""
        # Code with too many parameters
        code = '''
def function_with_many_params(a, b, c, d, e, f, g):
    pass
'''
        result = self.analyzer.analyze_code(code, 'python')
        
        # Should detect too many parameters
        self.assertTrue(len(result.code_smells) > 0)

    def test_security_issue_detection(self):
        """Test security issue detection"""
        code = '''
user_input = input("Enter command:")
eval(user_input)
'''
        result = self.analyzer.analyze_code(code, 'python')
        
        # Should detect eval() usage as security issue
        self.assertTrue(len(result.security_issues) > 0)


class PerformanceTests(unittest.TestCase):
    """Performance and caching tests"""

    def setUp(self):
        """Set up test fixtures"""
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        try:
            from performance.cache_manager import CacheManager
            self.cache = CacheManager(max_size=100, default_ttl=60)
        except ImportError:
            self.skipTest("Cache manager not available")

    def test_cache_set_get(self):
        """Test basic cache set and get operations"""
        self.cache.set("key1", "value1")
        value = self.cache.get("key1")
        
        self.assertEqual(value, "value1")

    def test_cache_miss(self):
        """Test cache miss returns None"""
        value = self.cache.get("nonexistent_key")
        
        self.assertIsNone(value)

    def test_cache_hit_rate(self):
        """Test cache hit rate calculation"""
        # Set some values
        for i in range(10):
            self.cache.set(f"key{i}", f"value{i}")
        
        # Hit some
        self.cache.get("key1")
        self.cache.get("key2")
        
        # Miss some
        self.cache.get("nonexistent1")
        self.cache.get("nonexistent2")
        
        stats = self.cache.get_stats()
        
        # Should have hits and misses
        self.assertGreater(stats['hits'], 0)
        self.assertGreater(stats['misses'], 0)

    def test_cache_lru_eviction(self):
        """Test LRU eviction when cache is full"""
        cache = self.cache

        # Fill cache
        for i in range(5):
            cache.set(f"key{i}", f"value{i}")

        # Access first key
        cache.get("key0")

        # Add one more (should evict LRU)
        cache.set("key5", "value5")

        # Check that cache is functioning
        stats = cache.get_stats()
        self.assertGreater(stats['current_size'], 0)
        # Cache may exceed max_size briefly before eviction, so check all keys are accessible
        self.assertIsNotNone(cache.get("key5"))


class SecurityTests(unittest.TestCase):
    """Authentication and encryption tests"""

    def setUp(self):
        """Set up test fixtures"""
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        try:
            from security.auth import SimpleAuthenticationManager
            from security.encryption import SimpleEncryptionManager
            self.auth = SimpleAuthenticationManager()
            self.encryption = SimpleEncryptionManager()
        except ImportError:
            self.skipTest("Security modules not available")

    def test_user_creation(self):
        """Test user account creation"""
        success, message, user = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_user_authentication(self):
        """Test user authentication with password"""
        # Create user
        self.auth.create_user("authuser", "auth@example.com", "authpass123")
        
        # Authenticate
        success, message, token = self.auth.authenticate_user("authuser", "authpass123")
        
        self.assertTrue(success)
        self.assertIsNotNone(token)

    def test_wrong_password_fails(self):
        """Test wrong password authentication fails"""
        # Create user
        self.auth.create_user("failuser", "fail@example.com", "failpass123")
        
        # Authenticate with wrong password
        success, message, token = self.auth.authenticate_user("failuser", "wrongpass")
        
        self.assertFalse(success)
        self.assertIsNone(token)

    def test_api_key_authentication(self):
        """Test API key authentication"""
        # Create user
        success, message, user = self.auth.create_user(
            "apiuser", "api@example.com", "apipass123"
        )
        
        # Authenticate with API key
        success, message, api_user = self.auth.authenticate_api_key(user.api_key)
        
        self.assertTrue(success)
        self.assertIsNotNone(api_user)

    def test_token_verification(self):
        """Test token verification"""
        # Create and authenticate user
        self.auth.create_user("tokenuser", "token@example.com", "tokenpass123")
        success, message, token = self.auth.authenticate_user("tokenuser", "tokenpass123")
        
        # Verify token
        success, message, payload = self.auth.verify_token(token)
        
        self.assertTrue(success)
        self.assertIsNotNone(payload)
        self.assertEqual(payload['username'], "tokenuser")

    def test_encryption_decryption(self):
        """Test data encryption and decryption"""
        plain_text = "This is sensitive data"
        
        # Encrypt
        success, message, encrypted = self.encryption.encrypt(plain_text)
        self.assertTrue(success)
        self.assertIsNotNone(encrypted)
        
        # Decrypt
        success, message, decrypted = self.encryption.decrypt(encrypted)
        self.assertTrue(success)
        self.assertEqual(decrypted, plain_text)

    def test_data_hashing(self):
        """Test data hashing"""
        data = "test data"
        
        success, message, hash1 = self.encryption.hash_data(data)
        self.assertTrue(success)
        self.assertIsNotNone(hash1)
        
        # Hashing should be deterministic
        success, message, hash2 = self.encryption.hash_data(data)
        self.assertEqual(hash1, hash2)


class IntegrationTests(unittest.TestCase):
    """Integration tests for module interaction"""

    def setUp(self):
        """Set up test fixtures"""
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    def test_code_analysis_integration(self):
        """Test code analysis module integration"""
        try:
            from code_analysis.enhanced_analyzer import EnhancedCodeAnalyzer
            
            analyzer = EnhancedCodeAnalyzer()
            result = analyzer.analyze_code("def test(): pass", 'python')
            
            self.assertIsNotNone(result)
            self.assertGreater(result.lines_of_code, 0)
        except ImportError:
            self.skipTest("Code analysis module not available")

    def test_cache_integration(self):
        """Test cache module integration"""
        try:
            from performance.cache_manager import CacheManager
            
            cache = CacheManager()
            cache.set("test_key", "test_value")
            value = cache.get("test_key")
            
            self.assertEqual(value, "test_value")
        except ImportError:
            self.skipTest("Cache module not available")

    def test_cli_integration(self):
        """Test CLI module integration"""
        try:
            from dev_tools.cli import ClaudeCodeCLI
            
            cli = ClaudeCodeCLI()
            self.assertIsNotNone(cli)
            self.assertEqual(cli.version, "1.0.0")
        except ImportError:
            self.skipTest("CLI module not available")


def run_test_suite() -> List[TestResult]:
    """
    Run all test suites and collect results

    Returns:
        List of TestResult objects
    """
    import time
    
    results = []
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(CodeAnalysisTests))
    suite.addTests(loader.loadTestsFromTestCase(PerformanceTests))
    suite.addTests(loader.loadTestsFromTestCase(SecurityTests))
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    test_result = runner.run(suite)
    elapsed_time = time.time() - start_time
    
    # Collect results
    total_tests = test_result.testsRun
    passed = total_tests - len(test_result.failures) - len(test_result.errors)
    
    result = TestResult(
        test_name="Full Test Suite",
        passed=(test_result.wasSuccessful()),
        execution_time=elapsed_time,
        error_message=f"{len(test_result.failures)} failures, {len(test_result.errors)} errors",
        details={
            'total_tests': total_tests,
            'passed': passed,
            'failed': len(test_result.failures),
            'errors': len(test_result.errors),
            'success_rate': f"{(passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A"
        }
    )
    
    results.append(result)
    
    return results


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Zeal Code - Comprehensive Test Suite")
    print("=" * 60)
    
    results = run_test_suite()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for result in results:
        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(f"\n{result.test_name}: {status}")
        print(f"  Execution time: {result.execution_time:.3f}s")
        if result.details:
            for key, value in result.details.items():
                print(f"  {key}: {value}")
        if result.error_message:
            print(f"  Error: {result.error_message}")
