from django.db import models

# Create your models here.

class Coin(models.Model):
    """Coin model."""
    id = models.CharField(max_length=32, null=False, blank=False, index=True)
    name = models.CharField(max_length=32, null=False, blank=False, index=True)
    symbol = models.CharField(max_length=8, null=False, blank=False)

    def __str__(self):
        return f"{self.name}-{self.symbol}"


class MarketCap(models.Model):
    """Market Cap model."""
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    date = models.DateField(_("Date"), null=False, blank=False)
    value = models.DecimalField(max_digits=19, decimal_places=5)
    currency = models.CharField(max_length=4, null=False, blank=False)

    def __str__(self):
        return f"{self.value}"