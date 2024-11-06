from django.shortcuts import render
import time
import requests
from django.http import JsonResponse
from django.utils import timezone
from .models import ExchangeRate
from django.core.cache import cache
import os
from dotenv import load_dotenv
from datetime import timedelta

def get_exchange_rate():
    load_dotenv() 
    api_key = os.getenv("API_KEY")
    response = requests.get("https://api.currencyapi.com/v3/latest", params={"base_currency": "USD", "currencies": "RUB", "apikey": api_key})
    data = response.json()
    return data["data"]["RUB"]["value"]

def get_current_usd(request):    
    last_record = ExchangeRate.objects.last()

    if not last_record or timezone.now() - last_record.last_request_time > timedelta(seconds=10):
        rate = get_exchange_rate()
        ExchangeRate.objects.create(rate=rate, last_request_time=timezone.now())
    else:
        rate = last_record.rate
    rate = get_exchange_rate()
    history = ExchangeRate.objects.all().order_by('-timestamp')[:10]
    history_data = [{"rate": record.rate, "timestamp": record.timestamp} for record in history]

    response_data = {
        "current_rate": rate,
        "history": history_data,
    }
    return JsonResponse(response_data)