import subprocess
import json

def fetch_crypto_prices():

    # Calls the OpenClaw agent to run the fetch-crypto-prices skill and returns the JSON response as a Python dictionary.

    try:
        # OpenClaw agent command
        result = subprocess.run(
            [
                r"C:\Users\AL GHANI COMPUTER\AppData\Roaming\npm\openclaw.cmd",
                "agent",
                "--agent",
                "main",
                "--message",
                "Use the fetch-crypto-prices skill and return the current crypto prices."
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout

        # Extract JSON block from output
        start = output.find("{")
        end = output.rfind("}") + 1
        json_data = output[start:end]

        return json.loads(json_data)

    except Exception as e:
        return {"error": str(e)}