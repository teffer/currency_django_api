from django.shortcuts import render
import time
import requests
from django.http import JsonResponse
from django.utils import timezone
from .models import ExchangeRate
from django.core.cache import cache
import os
from dotenv import load_dotenv

def get_exchange_rate():
    api_key = os.getenv("API_KEY")
    response = requests.get("https://api.currencyapi.com/v3/latest", params={"base_currency": "USD", "currencies": "RUB", "apikey": api_key})
    data = response.json()
    return data["data"]["RUB"]["value"]

def get_current_usd(request):
    rate = get_exchange_rate()
    ExchangeRate.objects.create(rate=rate)
    history = ExchangeRate.objects.all().order_by('-timestamp')[:10]
    history_data = [{"rate": record.rate, "timestamp": record.timestamp} for record in history]

    response_data = {
        "current_rate": rate,
        "history": history_data,
    }
    return JsonResponse(response_data)