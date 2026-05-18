"""
Secure UDP Chat Application
"""
import socket
import threading
import hashlib
import hmac
from algorithms.symmetric.aes import AESCipher
from algorithms.asymmetric.ecc import ECCCipher
from algorithms.hash.sha256 import SHA256
import base64

class SecureUDPChat:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)
        self.aes = None
        self.ecc = ECCCipher()
        self.running = False
        self.peers = {}
    
    def start_server(self):
        """Start UDP server for receiving messages"""
        self.socket.bind((self.host, self.port))
        self.running = True
        print(f"📡 UDP Chat listening on {self.host}:{self.port}")
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(65536)
                self.handle_message(data, addr)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_message(self, data, addr):
        """Handle incoming encrypted message"""
        try:
            if addr not in self.peers:
                # First message - key exchange
                self.handle_key_exchange(data, addr)
                return
            
            # Decrypt message
            decrypted = self.peers[addr].decrypt_cbc(data)
            message = decrypted.decode()
            
            # Verify HMAC
            msg_parts = message.split('||')
            if len(msg_parts) == 3:
                content, hmac_val, timestamp = msg_parts
                expected_hmac = hmac.new(
                    self.peers[addr].key,
                    f"{content}{timestamp}".encode(),
                    hashlib.sha256
                ).hexdigest()
                
                if hmac_val == expected_hmac:
                    print(f"\n💬 [{addr[0]}:{addr[1]}]: {content}")
                else:
                    print(f"\n⚠️ HMAC verification failed - message tampered!")
        except Exception as e:
            print(f"Error handling message: {e}")
    
    def handle_key_exchange(self, data, addr):
        """Perform ECDH key exchange"""
        try:
            # Receive peer's public key
            peer_public = data.decode()
            
            # Generate own key pair
            self.ecc.generate_keys()
            
            # Compute shared secret
            shared_secret = self.ecc.compute_shared_secret(peer_public)
            
            # Derive AES key from shared secret
            aes_key = hashlib.sha256(str(shared_secret).encode()).digest()[:32]
            
            # Initialize AES cipher
            cipher = AESCipher(256)
            cipher.set_key(aes_key)
            
            self.peers[addr] = cipher
            
            # Send own public key
            self.socket.sendto(self.ecc.public_key.encode(), addr)
            
            print(f"🔐 Secure channel established with {addr}")
        except Exception as e:
            print(f"Key exchange failed: {e}")
    
    def send_message(self, message, target_addr):
        """Send encrypted message to peer"""
        if target_addr not in self.peers:
            # Initiate key exchange
            self.ecc.generate_keys()
            self.socket.sendto(self.ecc.public_key.encode(), target_addr)
            print("Waiting for key exchange...")
            return
        
        # Prepare message with HMAC
        timestamp = str(hashlib.sha256(message.encode()).hexdigest()[:8])
        hmac_val = hmac.new(
            self.peers[target_addr].key,
            f"{message}{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        full_message = f"{message}||{hmac_val}||{timestamp}"
        encrypted = self.peers[target_addr].encrypt_cbc(full_message)
        self.socket.sendto(encrypted, target_addr)
        print(f"📤 Sent to {target_addr}: {message}")

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        chat = SecureUDPChat()
        print("Starting UDP Chat Server...")
        chat.start_server()
    else:
        chat = SecureUDPChat()
        target = input("Enter target address (host:port): ")
        host, port = target.split(':')
        target_addr = (host, int(port))
        
        # Start receiver thread
        receiver_thread = threading.Thread(target=chat.start_server, daemon=True)
        receiver_thread.start()
        
        print("UDP Chat Client started. Type messages to send.")
        while True:
            msg = input("> ")
            if msg.lower() == 'quit':
                break
            chat.send_message(msg, target_addr)

if __name__ == "__main__":
    main()