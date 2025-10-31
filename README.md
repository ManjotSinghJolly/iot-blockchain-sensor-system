# IoT + Blockchain Sensor System

### Decentralized Environmental Monitoring using ESP32, Flask & Ethereum (Sepolia)

![Project Badge](https://img.shields.io/badge/IoT-ESP32-blue)
![Project Badge](https://img.shields.io/badge/Backend-Flask-green)
![Project Badge](https://img.shields.io/badge/Blockchain-Ethereum-purple)
![Project Badge](https://img.shields.io/badge/Web3-web3.py-orange)
![Project Badge](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Project Badge](https://img.shields.io/badge/Network-Infura-red)

This project demonstrates a **tamper-proof IoT data logging system** using:

- ESP32 + DHT22 temperature & humidity sensor
- Flask backend server
- SHA-256 hashing for data integrity
- Ethereum smart contract (Sepolia testnet) to store data hashes on-chain
- Real-time dashboard with charts & Etherscan verification

Sensor readings are stored **locally AND on Ethereum blockchain**, ensuring trust, transparency, and immutability.

---

## System Architecture

```
 ┌────────┐       Wi-Fi        ┌────────────┐      SHA-256       ┌──────────────┐
 | DHT22  | ─────────────────▶ |   ESP32    | ────────────────▶ | Flask Server |
 └────────┘                    └────────────┘                    └─────┬────────┘
                                                                      │
                                                                      ▼
                                                              ┌──────────────┐
                                                              |  SQLite DB   |
                                                              └──────────────┘
                                                                      │
                                                                      ▼
                                                         ┌────────────────────────┐
                                                         | Ethereum (Sepolia)     |
                                                         | Smart Contract stores  |
                                                         | hash + timestamp       |
                                                         └────────────────────────┘
```

---

### Hardware Wiring (ESP32 → DHT22)

| DHT22 Pin | ESP32 Pin |
| --------- | --------- |
| VCC (+)   | 3.3V      |
| GND (-)   | GND       |
| DATA      | GPIO 26   |

> Note: DHT22 Data pin connected to GPIO26 (D26)

![Wiring Diagram](screenshots/wiring_diagram.png)

---

## Screenshots

### Live IoT Dashboard

![Dashboard](screenshots/dashboard.png)

### ESP32 + DHT22 Hardware Setup

![ESP32 Setup](screenshots/esp32_setup.jpeg)

### Flask Server Logs (showing blockchain TX hash)

![Server Logs](screenshots/server_console.png)

### Ethereum Transaction Verified on Etherscan

![Etherscan](screenshots/etherscan.png)

### ESP32 Serial Monitor Output

![Serial Monitor](screenshots/serial_monitor.png)

---

## Tech Stack

| Layer      | Technology                    |
| ---------- | ----------------------------- |
| Hardware   | ESP32 + DHT22                 |
| Comm       | Wi-Fi HTTP                    |
| Backend    | Flask (Python)                |
| Database   | SQLite                        |
| Blockchain | Solidity + Ethereum (Sepolia) |
| Web3       | web3.py + Infura              |
| Frontend   | Bootstrap + Chart.js          |
| Security   | SHA-256 hashing               |

---

## Project Structure

```
iot-blockchain-sensor-system/
├── server.py                 # Flask API + Dashboard backend
├── blockchain_client.py      # Ethereum Web3 client
├── templates/
│   └── dashboard.html        # Frontend UI
├── static/
│   └── style.css             # CSS styles
├── .gitignore                # Prevents secret leakage
└── README.md
```

---

## Requirements

- Python 3.8+
- ESP32 board
- Arduino IDE
- MetaMask wallet
- Infura account (Sepolia RPC)

---

## Setup Instructions

### 1. Clone repo

```bash
git clone https://github.com/ManjotSinghJolly/iot-blockchain-sensor-system
cd iot-blockchain-sensor-system
```

### 2. Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install flask flask_sqlalchemy web3 python-dotenv
```

### 4. Create `.env`

```
SEPOLIA_RPC_URL=your_infura_url
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=your_contract
ACCOUNT_ADDRESS=your_wallet_address
```

### 5. Run Backend

```bash
python server.py
```

Go to:

```
http://127.0.0.1:5000/dashboard
```

---

## How the System Works

| Step | Action                                              |
| ---- | --------------------------------------------------- |
| 1    | ESP32 reads Temp & Humidity from DHT22              |
| 2    | Sends readings via Wi-Fi → Flask API                |
| 3    | Flask hashes data using SHA-256                     |
| 4    | Data stored locally in SQLite                       |
| 5    | Hash sent to Ethereum smart contract                |
| 6    | Dashboard updates live with graphs + Etherscan link |

Result: Sensor data becomes **proven and verifiable**.

---

## Features

| Feature                         | Status |
| ------------------------------- | ------ |
| Real-time IoT sensor readings   | ✅     |
| Local database storage          | ✅     |
| SHA-256 data integrity          | ✅     |
| Hash on Ethereum                | ✅     |
| Etherscan verification buttons  | ✅     |
| Live chart updates              | ✅     |
| Pending vs confirmed TX display | ✅     |

---

## Author

**Manjot Singh Jolly**

If you found this useful, consider ⭐ starring this repo!

---

## 🪪 License

MIT License _(to be added)_
