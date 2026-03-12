from django.urls import path
from prices_tracker.views import get_prices

urlpatterns = [
    path("prices/", get_prices, name="get_prices"),
]