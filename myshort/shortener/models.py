from django.db import models
from django.contrib.auth.models import User
# stores url for guest user
class GShortURL(models.Model):
    shortcode = models.CharField(max_length=10, unique=True)
    original_url = models.URLField()


    def __str__(self):
        return f"{self.shortcode} → {self.original_url}"

# stores url for login user
class ShortURL(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    shortcode = models.CharField(max_length=10, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shortcode} → {self.original_url}"