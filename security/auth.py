"""
Zeal Code - Simple Authentication Module (Phase 3)
Security implementation without external dependencies
"""

import hashlib
import secrets
import time
import base64
import json
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class User:
    """User account data"""
    username: str
    email: str
    password_hash: str
    api_key: str
    role: str = 'user'
    created_at: float = field(default_factory=time.time)
    last_login: Optional[float] = None
    is_active: bool = True


class SimpleAuthenticationManager:
    """Simple authentication manager without JWT dependencies"""
    
    def __init__(self, token_expiry_hours: int = 24):
        """
        Initialize authentication manager

        Args:
            token_expiry_hours: Token expiry time in hours
        """
        self.token_expiry = token_expiry_hours * 3600  # Convert to seconds
        self.users: Dict[str, User] = {}  # username -> User
        self.api_keys: Dict[str, User] = {}  # api_key -> User
        self.session_tokens: Dict[str, Dict] = {}  # token -> session data
        self.secret = secrets.token_hex(32)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = password_hash.split('$')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def _generate_api_key(self) -> str:
        """Generate secure API key"""
        return f"cca_{secrets.token_hex(24)}"
    
    def _generate_token(self, user: User) -> str:
        """Generate simple session token"""
        # Create token payload
        payload = {
            'username': user.username,
            'role': user.role,
            'created_at': time.time(),
            'expires_at': time.time() + self.token_expiry
        }
        
        # Sign the payload
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hashlib.sha256((payload_str + self.secret).encode()).hexdigest()
        
        # Combine payload and signature, then base64 encode
        token_data = f"{payload_str}|{signature}"
        token = base64.urlsafe_b64encode(token_data.encode()).decode()
        
        # Store session
        self.session_tokens[token] = {
            'username': user.username,
            'role': user.role,
            'created_at': time.time()
        }
        
        return token
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role: str = 'user'
    ) -> Tuple[bool, str, Optional[User]]:
        """
        Create a new user account

        Args:
            username: Unique username
            email: User email
            password: User password
            role: User role (user, admin, etc.)

        Returns:
            (success, message, user)
        """
        if username in self.users:
            return False, "Username already exists", None
        
        if not self._is_valid_email(email):
            return False, "Invalid email format", None
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters", None
        
        password_hash = self._hash_password(password)
        api_key = self._generate_api_key()
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            api_key=api_key,
            role=role
        )
        
        self.users[username] = user
        self.api_keys[api_key] = user
        
        # Don't return password_hash in user object
        user_info = User(
            username=user.username,
            email=user.email,
            password_hash="***",
            api_key=api_key,
            role=user.role,
            created_at=user.created_at,
            last_login=user.last_login,
            is_active=user.is_active
        )
        
        return True, "User created successfully", user_info
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """
        Authenticate user with username and password

        Args:
            username: Username
            password: Password

        Returns:
            (success, message, token)
        """
        user = self.users.get(username)
        
        if not user:
            return False, "User not found", None
        
        if not user.is_active:
            return False, "Account is inactive", None
        
        if not self._verify_password(password, user.password_hash):
            return False, "Invalid password", None
        
        # Update last login
        user.last_login = time.time()
        
        # Generate token
        token = self._generate_token(user)
        
        return True, "Authentication successful", token
    
    def authenticate_api_key(self, api_key: str) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate user with API key

        Args:
            api_key: API key

        Returns:
            (success, message, user)
        """
        user = self.api_keys.get(api_key)
        
        if not user:
            return False, "Invalid API key", None
        
        if not user.is_active:
            return False, "Account is inactive", None
        
        # Update last login
        user.last_login = time.time()
        
        return True, "API key authentication successful", user
    
    def verify_token(self, token: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Verify session token

        Args:
            token: Session token

        Returns:
            (success, message, payload)
        """
        try:
            # Decode token
            token_data = base64.urlsafe_b64decode(token.encode()).decode()
            parts = token_data.split('|')
            if len(parts) != 2:
                return False, "Invalid token format", None

            payload_str, signature = parts

            # Verify signature
            expected_signature = hashlib.sha256((payload_str + self.secret).encode()).hexdigest()
            if signature != expected_signature:
                return False, "Invalid token signature", None

            # Parse payload
            payload = json.loads(payload_str)

            # Check expiry
            if time.time() > payload['expires_at']:
                # Clean up expired session
                if token in self.session_tokens:
                    del self.session_tokens[token]
                return False, "Token has expired", None

            return True, "Token valid", payload
        except Exception as e:
            return False, f"Invalid token: {str(e)}", None
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user information (without sensitive data)"""
        user = self.users.get(username)
        if not user:
            return None
        
        return {
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'api_key': user.api_key,
            'created_at': user.created_at,
            'last_login': user.last_login,
            'is_active': user.is_active
        }
    
    def regenerate_api_key(self, username: str) -> Tuple[bool, str, Optional[str]]:
        """
        Regenerate API key for user

        Args:
            username: Username

        Returns:
            (success, message, new_api_key)
        """
        user = self.users.get(username)
        if not user:
            return False, "User not found", None
        
        # Remove old API key
        old_key = user.api_key
        if old_key in self.api_keys:
            del self.api_keys[old_key]
        
        # Generate new API key
        new_key = self._generate_api_key()
        user.api_key = new_key
        self.api_keys[new_key] = user
        
        return True, "API key regenerated", new_key
    
    def deactivate_user(self, username: str) -> Tuple[bool, str]:
        """Deactivate user account"""
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        
        user.is_active = False
        return True, "User deactivated"
    
    def activate_user(self, username: str) -> Tuple[bool, str]:
        """Activate user account"""
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        
        user.is_active = True
        return True, "User activated"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get authentication statistics"""
        active_users = sum(1 for user in self.users.values() if user.is_active)
        
        return {
            'total_users': len(self.users),
            'active_users': active_users,
            'inactive_users': len(self.users) - active_users,
            'active_sessions': len(self.session_tokens)
        }


# Example usage
if __name__ == "__main__":
    auth = SimpleAuthenticationManager()
    
    # Create users
    success, message, user = auth.create_user(
        username="john",
        email="john@example.com",
        password="securepassword123",
        role="user"
    )
    print(f"Create user: {success}, {message}")
    print(f"User info: {user}")
    
    # Authenticate with password
    success, message, token = auth.authenticate_user("john", "securepassword123")
    print(f"\nAuth with password: {success}, {message}")
    print(f"Token: {token[:50]}...")
    
    # Verify token
    success, message, payload = auth.verify_token(token)
    print(f"\nVerify token: {success}, {message}")
    print(f"Payload: {payload}")
    
    # Authenticate with API key
    api_key = user.api_key
    success, message, api_user = auth.authenticate_api_key(api_key)
    print(f"\nAuth with API key: {success}, {message}")
    print(f"User: {api_user.username if api_user else None}")
    
    # Get stats
    print(f"\nAuth stats: {auth.get_stats()}")
