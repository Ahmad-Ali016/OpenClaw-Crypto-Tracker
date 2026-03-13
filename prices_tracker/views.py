from prices_tracker.services import fetch_crypto_prices, prices_tracker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def get_prices(request):

    # Simple API endpoint to fetch crypto prices using OpenClaw.
    # Calls the OpenClaw service layer and returns the result as JSON.

    # Call the OpenClaw service
    prices = fetch_crypto_prices()

    # Return JSON response
    return JsonResponse(prices)

@csrf_exempt
def start_tracker(request):

    # Endpoint to start crypto price tracking.

    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)

        interval = int(data.get("interval"))
        duration_minutes  = int(data.get("duration"))

        # convert minutes to seconds for internal processing
        duration = duration_minutes * 60

        if interval <= 0 or duration <= 0:
            return JsonResponse({"error": "Interval and duration must be positive numbers"}, status=400)

        file_path = prices_tracker(interval, duration)

        return JsonResponse({
            "message": "Price tracking completed",
            "file": file_path
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)