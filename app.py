import tkinter as tk
from urllib.request import urlopen
from urllib.parse import urlencode
import json


# Cryptocurrency API IDs
COINS = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "binancecoin": "Binance Coin (BNB)",
    "solana": "Solana (SOL)",
    "ripple": "XRP (XRP)"
}


def get_prices():
    """Get cryptocurrency prices from CoinGecko."""

    params = urlencode({
        "ids": ",".join(COINS.keys()),
        "vs_currencies": "usd"
    })

    url = f"https://api.coingecko.com/api/v3/simple/price?{params}"

    with urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())

    return data


def update_prices():
    """Update cryptocurrency prices in the GUI."""

    try:
        data = get_prices()

        for coin_id in COINS:
            price = data.get(coin_id, {}).get("usd")

            if price is not None:
                price_labels[coin_id].config(
                    text=f"${price:,.2f}"
                )

        status_label.config(
            text="🟢 Prices updated successfully"
        )

    except Exception:
        status_label.config(
            text="❌ Unable to connect to CoinGecko"
        )


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("CryptoTracker")
root.geometry("600x650")
root.resizable(False, False)


# Title
title_label = tk.Label(
    root,
    text="🪙 CryptoTracker",
    font=("Arial", 28, "bold")
)

title_label.pack(pady=(30, 5))


# Subtitle
subtitle_label = tk.Label(
    root,
    text="Real-Time Cryptocurrency Price Tracker",
    font=("Arial", 12)
)

subtitle_label.pack(pady=(0, 25))


# Price labels
price_labels = {}


for coin_id, coin_name in COINS.items():

    card = tk.Frame(
        root,
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    card.pack(
        fill="x",
        padx=50,
        pady=7
    )

    name_label = tk.Label(
        card,
        text=coin_name,
        font=("Arial", 14, "bold")
    )

    name_label.pack(side="left")

    price_label = tk.Label(
        card,
        text="Loading...",
        font=("Arial", 14, "bold")
    )

    price_label.pack(side="right")

    price_labels[coin_id] = price_label


# Refresh button
refresh_button = tk.Button(
    root,
    text="🔄 Refresh Prices",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    command=update_prices
)

refresh_button.pack(pady=25)


# Status
status_label = tk.Label(
    root,
    text="Connecting to CoinGecko...",
    font=("Arial", 11)
)

status_label.pack()


# Get prices when application starts
root.after(100, update_prices)


# Start application
root.mainloop()