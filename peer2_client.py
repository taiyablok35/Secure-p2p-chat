"""
Peer2 - Secure P2P Chat (connector role)
-----------------------------------------
Connects out to Peer1's IP address. Once connected, both sides are equal
peers: either can send or receive at any time. Every message is encrypted
with AES-128 in CBC mode using a fresh random IV, then Base64 encoded
before it goes on the wire.

Usage: python peer2_client.py <peer1-ip-address>
"""

import socket
import threading
import base64
import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = b"ThisIsA16ByteKey"   # 16 bytes -> AES-128. Must match Peer1's KEY.
PORT = 5000


def encrypt(plaintext: str) -> str:
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt(b64_text: str) -> str:
    raw = base64.b64decode(b64_text)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


def receive_loop(conn: socket.socket) -> None:
    reader = conn.makefile("r")
    for line in reader:
        line = line.strip()
        if not line:
            continue
        try:
            print(f"\n[Peer1]: {decrypt(line)}")
        except Exception as e:
            print(f"\n[Peer2] Could not decrypt incoming message: {e}")
        print("[You]: ", end="", flush=True)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python peer2_client.py <peer1-ip-address>")
        return

    peer1_ip = sys.argv[1]
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((peer1_ip, PORT))
    print(f"[Peer2] Connected to Peer1 at {peer1_ip}")

    threading.Thread(target=receive_loop, args=(conn,), daemon=True).start()

    writer = conn.makefile("w")
    print("Type a message and press Enter. Type /quit to exit.")
    try:
        while True:
            msg = input("[You]: ")
            if msg.strip().lower() == "/quit":
                break
            writer.write(encrypt(msg) + "\n")
            writer.flush()
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    main()
