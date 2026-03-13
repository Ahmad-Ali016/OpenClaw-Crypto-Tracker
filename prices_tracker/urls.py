from django.urls import path
from prices_tracker.views import get_prices, start_tracker

urlpatterns = [
    path("prices/", get_prices, name="get_prices"),
    path("start-tracker/", start_tracker, name="start_tracker"),
]