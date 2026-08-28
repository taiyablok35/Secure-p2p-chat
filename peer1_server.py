"""
Peer1 - Secure P2P Chat (listener role)
-----------------------------------------
Opens a socket and waits for Peer2 to connect. Once connected, both sides
are equal peers: either can send or receive at any time. Every message is
encrypted with AES-128 in CBC mode using a fresh random IV, then Base64
encoded before it goes on the wire.
"""

import socket
import threading
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = b"ThisIsA16ByteKey"   # 16 bytes -> AES-128. Must match Peer2's KEY.
PORT = 5000


def encrypt(plaintext: str) -> str:
    iv = os.urandom(16)                                  # new random IV per message
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt(b64_text: str) -> str:
    raw = base64.b64decode(b64_text)
    iv, ciphertext = raw[:16], raw[16:]                   # pull the IV back off the front
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


def receive_loop(conn: socket.socket) -> None:
    """Runs in the background so incoming messages never block typing."""
    reader = conn.makefile("r")
    for line in reader:
        line = line.strip()
        if not line:
            continue
        try:
            print(f"\n[Peer2]: {decrypt(line)}")
        except Exception as e:
            print(f"\n[Peer1] Could not decrypt incoming message: {e}")
        print("[You]: ", end="", flush=True)


def main() -> None:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", PORT))
    server_sock.listen(1)
    print(f"[Peer1] Waiting for Peer2 to connect on port {PORT} ...")

    conn, addr = server_sock.accept()
    print(f"[Peer1] Connected to {addr}")

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
        server_sock.close()


if __name__ == "__main__":
    main()
