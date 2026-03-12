import csv
import os
from datetime import datetime

DATA_DIR = "crypto_data"

def create_price_file():

    # Create a new CSV file with timestamp in filename. Returns the file path.

    # Ensure directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    file_path = os.path.join(DATA_DIR, f"prices_{timestamp}.csv")

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "timestamp",
            "BTC_USD",
            "BTC_USDT",
            "ETH_USD",
            "ETH_USDT",
            "USDT_USD"
        ])

    return file_path


def append_price_row(file_path, prices):

    # Append a row of price data to an existing CSV file.

    with open(file_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prices.get("BTC_USD"),
            prices.get("BTC_USDT"),
            prices.get("ETH_USD"),
            prices.get("ETH_USDT"),
            prices.get("USDT_USD")
        ])