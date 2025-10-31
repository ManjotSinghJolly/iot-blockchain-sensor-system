# IoTDataLedger Smart Contract

This smart contract is used to store SHA-256 hashes of IoT sensor readings on the Ethereum blockchain.

## Network

- Ethereum Testnet: Sepolia

## Contract Address

- 0xeAee9E07f6664a996850946C7060ecad063eC8e8

## Functions

| Function           | Description                        |
| ------------------ | ---------------------------------- |
| storeHash(string)  | Saves sensor data hash + timestamp |
| getRecord(uint256) | Gets stored record                 |
| totalRecords()     | Returns number of stored hashes    |

## Purpose

This contract enables immutable verification of IoT data integrity by storing a hash of sensor readings on blockchain.

## Deployment Instructions (Remix)

1. Visit https://remix.ethereum.org
2. Paste `IoTDataLedger.sol`
3. Compiler: Solidity 0.8.x
4. Environment: Injected Provider (MetaMask)
5. Network: Sepolia
6. Deploy + confirm in MetaMask
7. Copy contract address into `.env`
