---
name: fetch-crypto-prices
description: Retrieves current cryptocurrency prices for Bitcoin (BTC), Ethereum (ETH), and Tether (USDT) against USD and USDT from the CoinGecko API. Returns prices in a structured JSON format: BTC_USD, BTC_USDT, ETH_USD, ETH_USDT, USDT_USD. Use when a user asks for the current price of BTC, ETH, or USDT against USD or USDT.
---

# Fetch Crypto Prices

This skill retrieves current cryptocurrency prices from the CoinGecko API, specifically focusing on BTC, ETH, and USDT against both USD and USDT.

## Usage

When a user asks for the price of Bitcoin, Ethereum, or Tether, this skill will fetch the latest prices against USD and USDT and return them in a specific JSON format.

## Implementation

The skill uses a Python script to interact with the CoinGecko API. It includes error handling and request timeouts for robustness.

### `scripts/fetch_prices.py`

```python
import requests
import json

def get_crypto_prices():
    """
    Fetches current prices for BTC, ETH, and USDT against USD and USDT from CoinGecko API.
    Returns a dictionary with structured prices or an error message.
    """
    coins = "bitcoin,ethereum,tether"
    currencies = "usd,usdt" # Fetch against both USD and USDT
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies={currencies}"
    timeout_seconds = 10 # Added timeout

    try:
        response = requests.get(url, timeout=timeout_seconds)
        response.raise_for_status()  # Raise an exception for bad status codes
        raw_data = response.json()

        # Transform raw_data into the desired structured JSON
        transformed_data = {}
        
        # Process Bitcoin
        if "bitcoin" in raw_data:
            if "usd" in raw_data["bitcoin"]:
                transformed_data["BTC_USD"] = raw_data["bitcoin"]["usd"]
            if "usdt" in raw_data["bitcoin"]:
                transformed_data["BTC_USDT"] = raw_data["bitcoin"]["usdt"]

        # Process Ethereum
        if "ethereum" in raw_data:
            if "usd" in raw_data["ethereum"]:
                transformed_data["ETH_USD"] = raw_data["ethereum"]["usd"]
            if "usdt" in raw_data["ethereum"]:
                transformed_data["ETH_USDT"] = raw_data["ethereum"]["usdt"]
                
        # Process Tether (only USDT_USD is requested)
        if "tether" in raw_data:
            if "usd" in raw_data["tether"]:
                transformed_data["USDT_USD"] = raw_data["tether"]["usd"]

        # Check if any data was actually transformed. If not, it means the API response was empty or malformed for our needs.
        if not transformed_data:
             return {"error": "No price data could be extracted in the expected format from the API response."}
             
        return transformed_data

    except requests.exceptions.Timeout:
        return {"error": f"API request timed out after {timeout_seconds} seconds."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode API response."}
    except Exception as e: # Catch any other unexpected errors during transformation
        return {"error": f"An unexpected error occurred during data transformation: {e}"}


if __name__ == "__main__":
    prices = get_crypto_prices()
    print(json.dumps(prices, indent=2))

```

## Examples

**User:** "What's the current price of Bitcoin?"
**Codex:** (Calls `fetch-crypto-prices` skill)
**Output:**
```json
{
  "BTC_USD": 70000.50,
  "BTC_USDT": 70001.20
}
```

**User:** "How much is ETH and USDT?"
**Codex:** (Calls `fetch-crypto-prices` skill)
**Output:**
```json
{
  "ETH_USD": 3500.75,
  "ETH_USDT": 3501.00,
  "USDT_USD": 1.00
}
```
