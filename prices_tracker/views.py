from prices_tracker.services import fetch_crypto_prices
from django.http import JsonResponse

# Create your views here.

def get_prices(request):

    # Simple API endpoint to fetch crypto prices using OpenClaw.
    # Calls the OpenClaw service layer and returns the result as JSON.

    # Call the OpenClaw service
    prices = fetch_crypto_prices()

    # Return JSON response
    return JsonResponse(prices)