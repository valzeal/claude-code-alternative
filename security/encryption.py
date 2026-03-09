"""
Zeal Code - Simple Encryption Module (Phase 3)
Security implementation without external dependencies
"""

import hashlib
import secrets
import base64
import json
from typing import Optional, Tuple, Any


class SimpleEncryptionManager:
    """Simple encryption manager without external dependencies"""

    def __init__(self, encryption_key: Optional[bytes] = None):
        """
        Initialize encryption manager

        Args:
            encryption_key: Encryption key (generated if not provided)
        """
        self.encryption_key = encryption_key or secrets.token_bytes(32)

    def _xor_encrypt(self, data: bytes, key: bytes) -> bytes:
        """Simple XOR encryption"""
        key_len = len(key)
        return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

    def encrypt(self, data: str) -> Tuple[bool, str, Optional[str]]:
        """
        Encrypt string data using XOR encryption

        Args:
            data: Plain text data

        Returns:
            (success, message, encrypted_data)
        """
        try:
            data_bytes = data.encode()
            encrypted = self._xor_encrypt(data_bytes, self.encryption_key)
            encrypted_b64 = base64.urlsafe_b64encode(encrypted).decode()
            return True, "Data encrypted successfully", encrypted_b64
        except Exception as e:
            return False, f"Encryption failed: {str(e)}", None

    def decrypt(self, encrypted_data: str) -> Tuple[bool, str, Optional[str]]:
        """
        Decrypt encrypted data

        Args:
            encrypted_data: Base64-encoded encrypted data

        Returns:
            (success, message, decrypted_data)
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._xor_encrypt(encrypted_bytes, self.encryption_key)
            return True, "Data decrypted successfully", decrypted.decode()
        except Exception as e:
            return False, f"Decryption failed: {str(e)}", None

    def encrypt_dict(self, data: dict) -> Tuple[bool, str, Optional[str]]:
        """
        Encrypt dictionary data

        Args:
            data: Dictionary to encrypt

        Returns:
            (success, message, encrypted_data)
        """
        try:
            json_str = json.dumps(data)
            return self.encrypt(json_str)
        except Exception as e:
            return False, f"Dictionary encryption failed: {str(e)}", None

    def decrypt_dict(self, encrypted_data: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Decrypt dictionary data

        Args:
            encrypted_data: Base64-encoded encrypted dictionary

        Returns:
            (success, message, decrypted_dict)
        """
        success, message, decrypted_str = self.decrypt(encrypted_data)
        if not success:
            return False, message, None

        try:
            decrypted_dict = json.loads(decrypted_str)
            return True, "Dictionary decrypted successfully", decrypted_dict
        except Exception as e:
            return False, f"Dictionary decryption failed: {str(e)}", None

    def hash_data(self, data: str) -> Tuple[bool, str, Optional[str]]:
        """
        Hash data using SHA-256

        Args:
            data: Data to hash

        Returns:
            (success, message, hash)
        """
        try:
            hash_obj = hashlib.sha256(data.encode())
            return True, "Data hashed successfully", hash_obj.hexdigest()
        except Exception as e:
            return False, f"Hashing failed: {str(e)}", None

    def generate_token(self, length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_hex(length)


class SecureDataStore:
    """Secure data storage with encryption"""

    def __init__(self, encryption_manager: SimpleEncryptionManager):
        """
        Initialize secure data store

        Args:
            encryption_manager: EncryptionManager instance
        """
        self.encryption = encryption_manager
        self.storage: dict = {}

    def store(self, key: str, value: Any, encrypt: bool = True) -> Tuple[bool, str]:
        """
        Store data securely

        Args:
            key: Storage key
            value: Value to store
            encrypt: Whether to encrypt the value

        Returns:
            (success, message)
        """
        try:
            if encrypt:
                success, message, encrypted_value = self.encryption.encrypt_dict(value)
                if not success:
                    return False, message

                self.storage[key] = {
                    'encrypted': True,
                    'data': encrypted_value
                }
            else:
                self.storage[key] = {
                    'encrypted': False,
                    'data': value
                }

            return True, "Data stored successfully"
        except Exception as e:
            return False, f"Storage failed: {str(e)}"

    def retrieve(self, key: str) -> Tuple[bool, str, Optional[Any]]:
        """
        Retrieve data

        Args:
            key: Storage key

        Returns:
            (success, message, value)
        """
        try:
            entry = self.storage.get(key)
            if not entry:
                return False, "Key not found", None

            if entry['encrypted']:
                success, message, decrypted_value = self.encryption.decrypt_dict(entry['data'])
                if not success:
                    return False, message, None

                return True, "Data retrieved successfully", decrypted_value
            else:
                return True, "Data retrieved successfully", entry['data']
        except Exception as e:
            return False, f"Retrieval failed: {str(e)}", None

    def delete(self, key: str) -> Tuple[bool, str]:
        """Delete data"""
        if key not in self.storage:
            return False, "Key not found"

        del self.storage[key]
        return True, "Data deleted successfully"

    def list_keys(self) -> list:
        """List all stored keys"""
        return list(self.storage.keys())


# Example usage
if __name__ == "__main__":
    encryption = SimpleEncryptionManager()

    # Encrypt/decrypt strings
    plain_text = "This is sensitive data"
    success, message, encrypted = encryption.encrypt(plain_text)
    print(f"Encrypt: {success}, {message}")
    print(f"Encrypted: {encrypted[:50]}...")

    success, message, decrypted = encryption.decrypt(encrypted)
    print(f"\nDecrypt: {success}, {message}")
    print(f"Decrypted: {decrypted}")

    # Encrypt/decrypt dictionaries
    test_data = {
        'username': 'john',
        'email': 'john@example.com',
        'api_key': 'secret_key_123'
    }
    success, message, encrypted_dict = encryption.encrypt_dict(test_data)
    print(f"\nEncrypt dict: {success}, {message}")

    success, message, decrypted_dict = encryption.decrypt_dict(encrypted_dict)
    print(f"Decrypt dict: {success}, {message}")
    print(f"Decrypted: {decrypted_dict}")

    # Hash data
    success, message, hash_value = encryption.hash_data(plain_text)
    print(f"\nHash: {success}, {message}")
    print(f"Hash: {hash_value}")

    # Generate token
    token = encryption.generate_token()
    print(f"\nToken: {token}")

    # Secure data store
    secure_store = SecureDataStore(encryption)
    success, message = secure_store.store('user_data', test_data)
    print(f"\nStore: {success}, {message}")

    success, message, retrieved = secure_store.retrieve('user_data')
    print(f"Retrieve: {success}, {message}")
    print(f"Retrieved: {retrieved}")

    success, message = secure_store.delete('user_data')
    print(f"\nDelete: {success}, {message}")
    print(f"Keys: {secure_store.list_keys()}")
