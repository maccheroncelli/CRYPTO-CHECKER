import subprocess
import tkinter as tk
import re

def is_valid_bitcoin_address(value):
    # Bitcoin address pattern
    address_pattern = re.compile(r'^(bc1[0-9a-z]{8,87}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$', re.IGNORECASE)
    return bool(address_pattern.match(value))

def is_valid_ethereum_address(value):
    # Ethereum address pattern
    ethereum_address_pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
    return bool(ethereum_address_pattern.match(value))

def is_valid_tron_address(value):
    # TRON address pattern
    tron_address_pattern = re.compile(r'^T[0-9a-zA-Z]{33}$')
    return bool(tron_address_pattern.match(value))

def open_chrome_tabs(search_query, blockchain):
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    if is_valid_bitcoin_address(search_query):
        print(f"Opening Bitcoin-related websites for address: {search_query}")
        # Bitcoin-related websites
        bitcoin_websites = [
            f'https://tokenview.io/en/search/{search_query}',
            f'https://oxt.me/address/{search_query}',
            f'https://blockchair.com/bitcoin/address/{search_query}',
            f'https://www.walletexplorer.com/address/{search_query}',
            f'https://www.blockchain.com/btc/address/{search_query}',
            f'https://www.oklink.com/btc/address/{search_query}',
            f'https://www.google.com/search?q={search_query}%20-block',
            f'https://www.chainabuse.com/address/{search_query}',
            # Add more Bitcoin-related websites as needed
        ]
        subprocess.Popen([chrome_path, '--new-window'] + bitcoin_websites)
    elif is_valid_ethereum_address(search_query):
        print(f"Opening Ethereum-related websites for address: {search_query}")
        # Ethereum-related websites
        ethereum_websites = [
            f'https://tokenview.io/en/search/{search_query}',
            f'https://etherscan.io/address/{search_query}',
            f'https://www.chainabuse.com/address/{search_query}',
            f'https://www.google.com/search?q={search_query}%20-block'
            # Add more Ethereum-related websites as needed
        ]
        subprocess.Popen([chrome_path, '--new-window'] + ethereum_websites)
    elif is_valid_tron_address(search_query):
        print(f"Opening TRON-related websites for address: {search_query}")
        # TRON-related websites
        tron_websites = [
            f'https://tokenview.io/en/search/{search_query}',
            f'https://tronscan.org/#/address/{search_query}',
            f'https://www.chainabuse.com/address/{search_query}',
            f'https://www.google.com/search?q={search_query}%20-block'
            # Add more TRON-related websites as needed
        ]
        subprocess.Popen([chrome_path, '--new-window'] + tron_websites)
    else:
        print(f"Opening Bitcoin transaction websites for ID: {search_query}")
        # Bitcoin transaction websites
        transaction_websites = [
            f'https://www.blockchain.com/explorer/transactions/btc/{search_query}',
            f'https://oxt.me/transaction/{search_query}',
            f'https://www.oklink.com/btc/tx/{search_query}',
            f'https://blockchair.com/bitcoin/transaction/{search_query}'
            # Add more Bitcoin transaction-related websites as needed
        ]
        subprocess.Popen([chrome_path, '--new-window'] + transaction_websites)

def on_button_click(entry, blockchain):
    search_query = entry.get().strip()  # Trim excess whitespace
    open_chrome_tabs(search_query, blockchain)

def on_enter_key(event, entry, blockchain):
    on_button_click(entry, blockchain)

def main():
    root = tk.Tk()
    root.title("Crypto Checker")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    entry_label = tk.Label(frame, text="Enter cryptocurrency address or transaction ID:")
    entry_label.pack(pady=10)

    entry = tk.Entry(frame, width=50)
    entry.pack(pady=10)
    entry.focus_set()
    entry.bind("<Return>", lambda event: on_enter_key(event, entry, "cryptocurrency"))  # Bind Enter key to trigger the search

    button = tk.Button(frame, text="Open Websites", command=lambda: on_button_click(entry, "cryptocurrency"))
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
