from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore

# Create your models here.

class CustomUser(AbstractUser):
    pass
    
    def __str__(self) -> str:
        return self.username
    
class GuestUser(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.session_id

class CompressionTask(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    guest_user = models.ForeignKey(GuestUser, null=True, blank=True, on_delete=models.SET_NULL)
    #original_image = models.ImageField(upload_to='original_images/')
    compressed_image = models.ImageField(upload_to='compressed_images/')
    compression_type = models.CharField(max_length=10, choices=[('lossy', 'Lossy'), ('lossless', 'Lossless')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User' if self.user else 'Guest'} - {self.compression_type}"

