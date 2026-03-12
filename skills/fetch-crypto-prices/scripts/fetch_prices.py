import requests
import json

def safe_get(data, *keys):
    """Safely get a nested value from a dictionary."""
    if not isinstance(data, dict):
        return None
    
    current_data = data
    for key in keys:
        if isinstance(current_data, dict) and key in current_data:
            current_data = current_data[key]
        else:
            return None
    return current_data

def get_crypto_prices():
    """
    Fetches current prices for BTC, ETH, and USDT against USD and USDT from CoinGecko API.
    Ensures all required fields (BTC_USD, BTC_USDT, ETH_USD, ETH_USDT, USDT_USD) are present.
    Calculates USDT pairs if missing.
    Returns a dictionary with structured prices or an error message.
    """
    coins = "bitcoin,ethereum,tether"
    currencies = "usd,usdt" # Fetch against both USD and USDT
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies={currencies}"
    timeout_seconds = 10 # Added timeout

    # Initialize all required fields to None. This ensures they are always present.
    transformed_data = {
        "BTC_USD": None,
        "BTC_USDT": None,
        "ETH_USD": None,
        "ETH_USDT": None,
        "USDT_USD": None
    }

    try:
        response = requests.get(url, timeout=timeout_seconds)
        response.raise_for_status()  # Raise an exception for bad status codes
        raw_data = response.json()

        # Populate direct prices from API response
        transformed_data["BTC_USD"] = safe_get(raw_data, "bitcoin", "usd")
        transformed_data["BTC_USDT"] = safe_get(raw_data, "bitcoin", "usdt")
        transformed_data["ETH_USD"] = safe_get(raw_data, "ethereum", "usd")
        transformed_data["ETH_USDT"] = safe_get(raw_data, "ethereum", "usdt")
        transformed_data["USDT_USD"] = safe_get(raw_data, "tether", "usd")

        # Perform calculations if necessary and if USDT_USD is available and not zero
        usdt_usd_price = transformed_data["USDT_USD"]
        if usdt_usd_price is not None and usdt_usd_price != 0:
            # Calculate BTC_USDT if missing
            if transformed_data["BTC_USDT"] is None and transformed_data["BTC_USD"] is not None:
                transformed_data["BTC_USDT"] = transformed_data["BTC_USD"] / usdt_usd_price
            
            # Calculate ETH_USDT if missing
            if transformed_data["ETH_USDT"] is None and transformed_data["ETH_USD"] is not None:
                transformed_data["ETH_USDT"] = transformed_data["ETH_USD"] / usdt_usd_price
        else:
            # If USDT_USD is missing or zero, USDT pair calculations are impossible
            # We can leave BTC_USDT and ETH_USDT as None (which they are initialized to)
            # or explicitly set them to None here for clarity if they were somehow populated earlier.
            # Since they are initialized to None, no action needed here for this case.
            pass
            
        # Final check: if all values are None, it means API call might have succeeded but returned no usable data.
        all_none = all(v is None for v in transformed_data.values())
        if all_none:
            return {"error": "API returned data, but no usable price information could be extracted."} # More specific error

        return transformed_data

    except requests.exceptions.Timeout:
        return {"error": f"API request timed out after {timeout_seconds} seconds."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode API response."}
    except Exception as e:
        # Catch any other unexpected errors during transformation or calculation
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == "__main__":
    prices = get_crypto_prices()
    print(json.dumps(prices, indent=2))
