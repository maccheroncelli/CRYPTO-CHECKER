# 🔎 Crypto Checker GUI — OSINT Tool for Blockchain Addresses

A fast, customizable GUI that lets you paste **Bitcoin**, **Ethereum-style Hexadecimal**, or **TRON** addresses (or TXIDs) and instantly open **relevant blockchain explorer tabs**. Built with `customtkinter`, it's lightweight and easily extensible.

---

## ✅ Features

- 🔍 **Auto-detects address type** (Bitcoin, Hex, TRON, or TXID fallback)
- 🌐 Launches selected explorers in a **new browser window**
- ✅ **Checkbox control** over which sites to open
- 🛠️ **Add your own lookups** via the GUI
- 💾 **Remembers last-used selections** with `checked_memory.json`
- 🧠 Puts “Google Search” and “Chainabuse” **last** in the list
- 📂 All config handled via simple editable JSON files

---

## 🖥️ Requirements

- Python 3.10+
- `customtkinter`

```bash
pip install customtkinter
```

---

## 🚀 Usage

```bash
python CRYPTO-CHECKER.py
```

1. Paste a crypto address or transaction ID.
2. Click **Detect Type**.
3. Review the detected address type + site options.
4. Check/uncheck which sites you want to open.
5. Click **Open Selected Sites**.
6. Add new lookups via **Add Site**.
7. Your last selections are remembered next time.

---

## 📁 File Structure

- `CRYPTO-CHECKER.py` — main GUI
- `sites.json` — stores blockchain explorer configurations
- `checked_memory.json` — stores last-used checkboxes per address type

---

## 🧠 Example Use Case

Paste:

```
0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5
```

Crypto Checker detects this as a **Hexadecimal address** and opens:

- ✅ Etherscan  
- ✅ Blockscan  
- ✅ Tokenview  
- ⬜ Chainabuse (optional)  
- ⬜ Google Search (optional)

Perfect for:
- OSINT analysts
- Blockchain forensic investigators
- Law enforcement
- Anyone tracing wallet behavior fast

---

## 🛠️ Customizing

To edit or add site lookups, open `sites.json`:

```json
{
  "Hexadecimal": {
    "validators": ["is_hex_address"],
    "urls": {
      "Etherscan": "https://etherscan.io/address/{value}",
      "Blockscan": "https://blockscan.com/address/{value}"
    }
  }
}
```

Use `{value}` as a placeholder for the address or TXID you input.

---

## 🧼 Notes

- Local-only app. No analytics or outbound data.
- All settings are saved between runs.
- Easily extensible with your own tools or scripts.

---

**Feel free to fork, modify, and improve!**

![2025-05-19_14-55-49](https://github.com/user-attachments/assets/039ccc84-085f-4c8b-aa7a-862605d63436)
