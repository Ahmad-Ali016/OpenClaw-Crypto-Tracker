---
name: fetch-crypto-prices
description: Retrieves current cryptocurrency prices for Bitcoin (BTC), Ethereum (ETH), and Tether (USDT) from the CoinGecko API and returns them in a structured JSON format. Use when a user asks for the current price of BTC, ETH, or USDT.
---

# Fetch Crypto Prices

This skill retrieves current cryptocurrency prices from the CoinGecko API.

## Usage

When a user asks for the price of Bitcoin, Ethereum, or Tether, this skill will fetch the latest USD prices.

## Implementation

The skill uses a Python script to interact with the CoinGecko API.

### `scripts/fetch_prices.py`

```python
import requests
import json

def get_crypto_prices():
    """
    Fetches current prices for BTC, ETH, and USDT from CoinGecko API.
    Returns a dictionary with prices or an error message.
    """
    coins = "bitcoin,ethereum,tether"
    currency = "usd"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies={currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # CoinGecko's simple/price endpoint already returns structured data.
        # Example: {"bitcoin": {"usd": 70000.50}, "ethereum": {"usd": 3500.75}, "tether": {"usd": 1.00}}
        
        return data

    except requests.exceptions.RequestException as e:
        # Return a dictionary with an error key for structured error handling
        return {"error": f"API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode API response."}

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
  "bitcoin": {
    "usd": 70000.50
  }
}
```

**User:** "How much is ETH and USDT?"
**Codex:** (Calls `fetch-crypto-prices` skill)
**Output:**
```json
{
  "ethereum": {
    "usd": 3500.75
  },
  "tether": {
    "usd": 1.00
  }
}
```
