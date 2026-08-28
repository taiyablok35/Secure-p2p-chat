# Secure P2P Chat (AES-CBC)

A pure peer-to-peer encrypted chat: no central server, no third party.
One peer briefly acts as a "listener" just to open the socket; after that,
both sides are equal and can send/receive independently and simultaneously.

## Files
- `Peer1Server.java` — run this first, on the machine that will be listening
- `Peer2Client.java` — run this second, on the machine that will connect in

## How it works
- AES-128 in CBC mode (`AES/CBC/PKCS5Padding`)
- A fresh random 16-byte IV is generated for **every** message and sent
  along with the ciphertext (Base64-encoded together) — this avoids the
  pattern-leakage problem of AES-ECB
- A background thread handles incoming messages so you can type and receive
  at the same time, instead of taking strict turns

## Running on two different devices

Both devices must be able to reach each other over the network — same
Wi-Fi/LAN is simplest. If you're on separate networks, see "Running over
the internet" below.

1. Compile on both machines:
   ```
   javac Peer1Server.java
   javac Peer2Client.java
   ```

2. On Device A (the listener), find its local IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`

3. On Device A, start Peer1:
   ```
   java Peer1Server
   ```

4. On Device B, connect in using Device A's IP:
   ```
   java Peer2Client 192.168.1.23
   ```
   (replace with Device A's actual IP)

5. Chat! Type a message and hit Enter on either machine. Type `/quit` to
   exit.

## Firewall note
Device A's OS firewall must allow inbound connections on port `5000`
(the port is set as a constant, `PORT = 5000`, in both files — change it
in both if you need a different one).

## Running over the internet (not just LAN)
This requires port forwarding on Device A's router (forward external
port 5000 to Device A's local IP and port 5000) and connecting to
Device A's public IP instead of its local IP. Exposing a port publicly
carries risk — only do this on a network you control, and turn off
forwarding when you're done.

## Security note on the key
The AES key is currently hardcoded (`ThisIsA16ByteKey`) so both peers
agree on it out of the box, matching the lab's teaching goal. In a real
deployment this key would instead be negotiated per-session via a key
exchange protocol (e.g. Diffie-Hellman), never hardcoded in source.
