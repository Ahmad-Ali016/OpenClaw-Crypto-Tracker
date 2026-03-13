import subprocess
import json
import time

from django.conf import settings

from prices_tracker.utils import create_price_file, append_price_row


def fetch_crypto_prices():

    # Calls the OpenClaw agent to run the fetch-crypto-prices skill and returns the JSON response as a Python dictionary.

    try:
        # OpenClaw agent command
        result = subprocess.run(
            [
                settings.OPENCLAW_PATH,
                "agent",
                "--agent",
                "main",
                "--message",
                "Use the fetch-crypto-prices skill and return the current crypto prices."
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout

        # Extract JSON block from OpenClaw response/output
        start = output.find("{")
        end = output.rfind("}") + 1
        json_data = output[start:end]

        return json.loads(json_data)

    except Exception as e:
        return {"error": str(e)}

def prices_tracker(interval, duration):

    # Runs the price tracker for a given duration and interval and creates a timestamp CSV file and appends rows to it.

    # Create CSV file for this tracking session
    file_path = create_price_file()

    start_time = time.time()

    while True:

        elapsed = time.time() - start_time

        if elapsed > duration:
            break

        # Fetch prices using OpenClaw
        prices = fetch_crypto_prices()

        # Skip writing if error occurred
        if "error" not in prices:
            append_price_row(file_path, prices)

        # Wait before next fetch
        time.sleep(interval)

    return file_path