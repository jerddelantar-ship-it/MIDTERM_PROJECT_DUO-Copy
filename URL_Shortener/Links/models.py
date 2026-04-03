from django.db import models
import string
import random
from django.utils import timezone
from django.core.validators import URLValidator

class URLMap(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    custom_alias = models.CharField(max_length=50, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    created_by = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    def save(self, *args, **kwargs):
        if not self.short_code and not self.custom_alias:
            self.short_code = self.generate_short_code()
        if self.custom_alias and not self.short_code:
            self.short_code = self.custom_alias
        super().save(*args, **kwargs)
    
    def generate_short_code(self, length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=length))
            if not URLMap.objects.filter(short_code=short_code).exists():
                return short_code
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def increment_click_count(self):
        self.click_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['click_count', 'last_accessed'])

class ClickStats(models.Model):
    link = models.ForeignKey(URLMap, on_delete=models.CASCADE, related_name='click_stats')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Click on {self.link.short_code} at {self.clicked_at}"

# Remove Category, Tag, LinkTag for now to simplify