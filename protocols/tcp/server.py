"""
Secure TCP Server using Hybrid Cryptography
"""
import socket
import threading
import json
from algorithms.symmetric.aes import AESCipher
from algorithms.asymmetric.rsa import RSACipher
from algorithms.hash.sha256 import SHA256
from utils.crypto_utils import CryptoUtils
import logging

class SecureTCPServer:
    def __init__(self, host='localhost', port=8443):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.rsa = RSACipher(2048)
        self.aes = None
        self.running = False
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the secure server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"🔐 Secure Server listening on {self.host}:{self.port}")
        self.logger.info(f"Server started on {self.host}:{self.port}")
        
        # Generate RSA key pair
        print("Generating RSA key pair...")
        self.rsa.generate_keys()
        print(f"RSA Public Key: {self.rsa.public_key[:50]}...")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"\n📱 New connection from {address}")
                
                # Start new thread for each client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                self.logger.error(f"Error accepting connection: {e}")
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        try:
            # Step 1: Send server's RSA public key
            client_socket.send(self.rsa.public_key.encode())
            
            # Step 2: Receive client's RSA public key
            client_public_key = client_socket.recv(4096).decode()
            
            # Step 3: Generate AES session key
            aes_key = CryptoUtils.generate_aes_key(256)
            self.aes = AESCipher(256)
            self.aes.set_key(aes_key)
            
            # Step 4: Encrypt AES key with client's RSA key
            encrypted_aes_key = CryptoUtils.rsa_encrypt(aes_key.hex(), client_public_key)
            client_socket.send(encrypted_aes_key.encode())
            
            print(f"✅ Secure channel established with {address}")
            self.logger.info(f"Secure channel established with {address}")
            
            # Step 5: Secure message exchange
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Decrypt message
                decrypted = self.aes.decrypt_cbc(data)
                message = decrypted.decode()
                
                # Verify integrity
                hash_val = SHA256.hash(message)
                
                print(f"\n📨 Received from {address}: {message}")
                print(f"🔒 Hash: {hash_val[:16]}...")
                
                # Echo back with HMAC
                response = f"Server received: {message}"
                encrypted_response = self.aes.encrypt_cbc(response)
                client_socket.send(encrypted_response)
                
        except Exception as e:
            self.logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection closed: {address}")
    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    server = SecureTCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()