from django.db import models
from django.utils import timezone

class ExchangeRate(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    last_request_time = models.DateTimeField(default=timezone.now)