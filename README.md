# Shark Coin: A Blockchain Implementation  

## 📌 Introduction  
Since the publication of **Satoshi Nakamoto's 2008 paper**  
[*Bitcoin: A Peer-to-Peer Electronic Cash System*](https://bitcoin.org/bitcoin.pdf),  
the architecture and applications of **blockchain technology** have evolved significantly.  

Inspired by Bitcoin’s blockchain concept, this project implements a blockchain system humorously named **"Shark Coin"**.  
Although it **does not achieve full decentralization**, it incorporates essential blockchain features, including:  

✔ **Digital Signatures**  
✔ **Block Generation**  
✔ **Hashing Algorithms**  
✔ **Mining Rewards**  
✔ **Authentication Mechanisms**  

This makes it a **complex yet rewarding challenge** to explore blockchain principles.  

---

## 🏗️ Overview  
The overall system architecture is illustrated in **Figure 1**.  

### 🔑 1. User Authentication & Registration  
- Users interact with the system through a **GUI interface** (Figure 2).  
- New users complete a **registration process**, where an **RSA key pair (Public & Private Key)** is generated and stored locally.  
- These keys are used for **authentication** and **digital signing** in future transactions.  

### 🔄 2. Client-Server Interaction  
- Upon successful login, the **Client and Server** communicate, with the **Server managing a MySQL database**.  
- The Client retrieves:  
  - ✅ Signatures  
  - ✅ Public keys  
  - ✅ Transaction data  
- The Client verifies the transaction’s authenticity before **initiating mining operations**.  
- **Multiple users can participate in mining simultaneously.**  

### ⛏️ 3. Mining Process  
- Each Client computes a **hash using SHA-256** by iterating through a **random nonce** (Figure 3).  
- Mining continues **until a valid hash is found** that meets the required difficulty level.  

### 🎯 4. Mining Rewards & Blockchain Updates  
- Once a Client **successfully mines a block**, it submits the following to the Server:  
  - ✅ **Signature**  
  - ✅ **Public Key**  
  - ✅ **Transaction Details**  
- Other Clients **pause their mining operations** temporarily.  
- After validation, the successful miner receives a **Shark Coin reward** 🦈💰 (Figure 4).  

### 📜 5. Transaction Processing & Block Generation  
- The mining reward is treated as a **transaction**, which is:  
  1. **Hashed** to generate a digest  
  2. **Signed using the private key**  
  3. **Sent to the Server for inclusion in the next block**  
- The new block is linked to the previous block, forming a **continuous blockchain** (Figure 5).  
- The **Server dynamically adjusts mining difficulty** based on mining speed.  
- Once a new block is created, the Server **broadcasts the transactions, public keys, and signatures** to all miners, allowing them to continue mining.  

### 🔗 6. Blockchain Structure  
- Blocks are **sequentially connected**, forming a **chain**.  
- Each block (except the **genesis block**) contains a **Prehash field**, which stores the hash of the **previous block**.  

---

## 🎉 Conclusion  
After extensive effort, the **Shark Coin blockchain** has been successfully implemented! 🚀  
Although it is **not a fully decentralized blockchain** and lacks **mass mining participation**,  
the fundamental **blockchain structure is fully functional**.  

With this solid foundation, future enhancements such as:  
🔹 **Private Blockchain Deployment**  
🔹 **Smart Contract Integration**  
🔹 **Consensus Algorithm Improvements**  

...can be implemented much more efficiently. 💡  

🔥 **Happy Mining!** 🦈💰  
