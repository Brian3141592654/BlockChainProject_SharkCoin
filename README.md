Shark Coin: A Blockchain Implementation
Introduction
Since the publication of Satoshi Nakamoto's 2008 paper Bitcoin: A Peer-to-Peer Electronic Cash System, the architecture and applications of blockchain technology have gradually evolved and gained significant attention in recent years. Inspired by Bitcoin's blockchain concept, this project implements a blockchain system humorously named "Shark Coin". Although it does not achieve full decentralization, it incorporates key blockchain components such as digital signatures, block generation, hashing algorithms, mining rewards, and authentication mechanisms, making it a complex yet rewarding challenge.

Overview
The overall system architecture is illustrated in Figure 1.

User Authentication & Registration:

Users interact with the system through a GUI interface (Figure 2).
New users complete a registration process, where an RSA key pair (Public Key & Private Key) is generated and stored locally for future authentication and digital signing.
Client-Server Interaction:

Upon successful login, the Client and Server communicate, with the Server managing a MySQL database to store relevant data.
The Client retrieves signatures, public keys, and transaction data from the Server, verifying their authenticity before initiating mining operations.
Multiple users can participate in mining simultaneously.
Mining Process:

Each Client computes a hash using SHA-256 by iterating through a random nonce (Figure 3).
Mining continues until a valid hash is found that meets the required difficulty level.
Mining Rewards & Blockchain Updates:

Once a Client successfully mines a block, it submits its signature, public key, and transaction details to the Server.
Other Clients temporarily pause their mining operations.
After validation, the successful miner receives a Shark Coin reward (Figure 4).
Transaction Processing & Block Generation:

The mining reward is treated as a transaction, which is hashed, signed using the private key, and sent to the Server for inclusion in the next block.
The new block is linked to the previous block, maintaining the blockchain structure (Figure 5).
The Server dynamically adjusts the mining difficulty based on mining speed and broadcasts the new block’s transactions, public keys, and signatures to all miners, allowing them to continue mining.
Blockchain Structure:

Blocks are connected sequentially, forming a chain.
Each block (except the genesis block) contains a Prehash field, which stores the hash of the previous block, ensuring the integrity of the blockchain.
Conclusion
After extensive effort, the Shark Coin blockchain has been successfully implemented. While it is not a fully decentralized blockchain and lacks a large number of participating miners, the fundamental blockchain structure has been established. This achievement is a significant milestone and an exciting accomplishment. With this solid foundation, future enhancements such as private blockchain deployment and smart contract integration can be achieved more efficiently.
