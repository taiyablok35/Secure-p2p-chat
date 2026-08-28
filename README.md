# Secure Peer-to-Peer Chat Application

A secure peer-to-peer chat application implemented in Python using TCP socket programming and AES-128-CBC encryption.

## Aim

To demonstrate a secure peer-to-peer chat application using the AES algorithm for encrypted communication between two peers.

## Objectives

- To understand peer-to-peer communication using TCP sockets.
- To implement message encryption and decryption using AES-128-CBC.
- To use a random Initialization Vector (IV) for each message.
- To enable simultaneous message exchange between two peers.

## Introduction

Chat applications are commonly used for exchanging messages over a network. However, messages transmitted without encryption can be intercepted and read by unauthorized parties. Cryptography can be used to protect communication by converting readable information into an encrypted form.

In a peer-to-peer (P2P) chat application, two systems can exchange information directly without depending on a permanent centralized server. In this implementation, one peer initially acts as a listener while the second peer connects to it. After the connection is established, both peers can send and receive messages.

To provide confidentiality, the application uses the Advanced Encryption Standard (AES). AES-128 in CBC (Cipher Block Chaining) mode is used for encryption. A fresh random 16-byte Initialization Vector (IV) is generated for every message. The IV and ciphertext are then Base64 encoded before transmission.

The application is implemented in Python using socket programming, multithreading, and the PyCryptodome library.

## Features

- Peer-to-peer chat communication
- AES-128-CBC message encryption
- Random IV generated for every message
- TCP socket communication
- Simultaneous sending and receiving
- Base64 encoding of encrypted data
- Python implementation

## Technologies Used

- Python
- TCP/IP Socket Programming
- AES-128-CBC
- PyCryptodome
- Multithreading
- Base64 Encoding

## Project Structure

secure-p2p-chat-aes/
|
|-- peer1_server.py
|-- peer2_client.py
|-- README.md
|-- requirements.txt
|-- .gitignore

## How the Application Works

The application consists of two Python programs.

### Peer 1 - Server / Listener

peer1_server.py acts as the listener. It creates a TCP socket and waits for Peer 2 to connect on port 5000.

### Peer 2 - Client / Connector

peer2_client.py acts as the connector. It connects to Peer 1 using the IP address of Peer 1 and port 5000.

Once the connection is established, both peers can send and receive messages independently.

## Encryption Process

When a message is sent, it follows this process:

Plaintext
↓
UTF-8 Encoding
↓
Padding
↓
Random 16-byte IV Generation
↓
AES-128-CBC Encryption
↓
IV + Ciphertext
↓
Base64 Encoding
↓
TCP Transmission

## Decryption Process

At the receiving peer, the following process takes place:

Base64 Data
↓
Base64 Decoding
↓
Separate IV and Ciphertext
↓
AES-128-CBC Decryption
↓
Remove Padding
↓
UTF-8 Decoding
↓
Original Message

## Cryptography Used

### AES-128

Advanced Encryption Standard (AES) is a symmetric-key encryption algorithm. The same secret key is used for both encryption and decryption.

This implementation uses:

- Algorithm: AES
- Key Size: 128 bits
- Key Length: 16 bytes
- Mode: CBC (Cipher Block Chaining)
- Block Size: 16 bytes
- Padding: PKCS5
- Initialization Vector: Random 16 bytes for every message

A new random IV is generated for every message to prevent identical plaintext messages from producing the same ciphertext pattern.

## Installation

### Prerequisites

Make sure Python is installed on your system.

Check the Python version using:

python --version

### Install Required Library

Install PyCryptodome using:

python -m pip install pycryptodome

Alternatively, install the project dependency using:

python -m pip install -r requirements.txt

## Running the Application

### Step 1 - Start Peer 1

Open a terminal in the project directory and run:

python peer1_server.py

Peer 1 will display:

[Peer1] Waiting for Peer2 to connect on port 5000 ...

Peer 1 now waits for Peer 2 to establish a connection.

### Step 2 - Start Peer 2

Open a second terminal and run:

python peer2_client.py 127.0.0.1

For testing both peers on the same computer, 127.0.0.1 can be used.

Peer 2 will display:

[Peer2] Connected to Peer1 at 127.0.0.1

Type a message and press Enter. Type /quit to exit.

### Step 3 - Exchange Messages

After the connection is established, messages can be entered from either peer.

Example:

Peer 1: Hello from Peer 1

Peer 2: Hello from Peer 2

Messages are encrypted before being transmitted and decrypted at the receiving peer.

### Step 4 - Exit the Chat

To terminate the chat session, type:

/quit

## Running on Two Different Computers

The application can also be tested on two computers connected to the same Wi-Fi or LAN.

### On Computer A

Start Peer 1:

python peer1_server.py

Find the IPv4 address of Computer A using:

ipconfig

For example:

192.168.1.23

### On Computer B

Run Peer 2 using the IP address of Computer A:

python peer2_client.py 192.168.1.23

Replace 192.168.1.23 with the actual IPv4 address of Computer A.

Both computers must be able to communicate over the network, and the firewall on Computer A must allow TCP connections on port 5000.

## Example Communication

PEER 1

[Peer1] Waiting for Peer2 to connect on port 5000 ...

[Peer1] Connected to ('127.0.0.1', XXXXX)

Type a message and press Enter. Type /quit to exit.

[You]: Hello Peer 2

[Peer2]: Hello Peer 1


PEER 2

[Peer2] Connected to Peer1 at 127.0.0.1

Type a message and press Enter. Type /quit to exit.

[You]: Hello Peer 1

[Peer1]: Hello Peer 2

## Security Considerations

The application demonstrates encrypted peer-to-peer communication using AES-128-CBC.

A fresh random IV is generated for every message, which helps prevent repeated plaintext messages from producing the same ciphertext pattern.

The current implementation uses a hardcoded AES key for demonstration purposes. In a real-world application, the encryption key should be securely exchanged or negotiated rather than stored directly in the source code.

AES-CBC by itself does not provide message authentication or integrity protection. A production implementation should use an authenticated encryption method such as AES-GCM.

## Files

### peer1_server.py

Contains the Peer 1 listener implementation, AES encryption and decryption functions, TCP socket handling, and message receiving thread.

### peer2_client.py

Contains the Peer 2 connector implementation, AES encryption and decryption functions, TCP connection handling, and message receiving thread.

### requirements.txt

Contains the Python dependency required for AES encryption:

pycryptodome

### .gitignore

Contains files and folders that should not be uploaded to the repository, such as Python cache files and virtual environments.

## Conclusion

The project demonstrates a secure peer-to-peer chat system using Python, TCP socket programming, and AES-128-CBC encryption. Messages are encrypted before transmission and decrypted at the receiving peer, while a new random IV is generated for every message.

The application successfully demonstrates secure message exchange between two peers and provides an understanding of socket programming, symmetric encryption, initialization vectors, Base64 encoding, and multithreading.

## Author

**Taiyab Lokhandwala**

M.Tech Computer Science & Engineering - Cybersecurity
