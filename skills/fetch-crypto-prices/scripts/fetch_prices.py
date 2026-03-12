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
