"""
Secure TCP Client
"""
import socket
import json
from algorithms.symmetric.aes import AESCipher
from algorithms.asymmetric.rsa import RSACipher
from algorithms.hash.sha256 import SHA256
from utils.crypto_utils import CryptoUtils

class SecureTCPClient:
    def __init__(self, server_host='localhost', server_port=8443):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.rsa = RSACipher(2048)
        self.aes = None
    
    def connect(self):
        """Connect to server and establish secure channel"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        
        print(f"🔐 Connected to server at {self.server_host}:{self.server_port}")
        
        # Step 1: Receive server's RSA public key
        server_public_key = self.socket.recv(4096).decode()
        
        # Step 2: Generate and send client's RSA public key
        self.rsa.generate_keys()
        self.socket.send(self.rsa.public_key.encode())
        
        # Step 3: Receive encrypted AES key
        encrypted_aes_key = self.socket.recv(4096).decode()
        
        # Step 4: Decrypt AES key with client's RSA private key
        aes_key_hex = CryptoUtils.rsa_decrypt(encrypted_aes_key, self.rsa.private_key)
        aes_key = bytes.fromhex(aes_key_hex)
        
        # Step 5: Initialize AES cipher
        self.aes = AESCipher(256)
        self.aes.set_key(aes_key)
        
        print("✅ Secure channel established!")
        return True
    
    def send_message(self, message):
        """Send encrypted message"""
        if not self.aes:
            raise Exception("Not connected. Call connect() first.")
        
        encrypted = self.aes.encrypt_cbc(message)
        self.socket.send(encrypted)
        
        # Wait for response
        response = self.socket.recv(4096)
        decrypted = self.aes.decrypt_cbc(response)
        return decrypted.decode()
    
    def close(self):
        if self.socket:
            self.socket.close()
        print("Connection closed.")

def main():
    client = SecureTCPClient()
    
    try:
        client.connect()
        
        while True:
            message = input("\n📝 Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            
            response = client.send_message(message)
            print(f"📨 Server response: {response}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()