from django.db import models
import uuid

# Create your models here.

class EDL(models.Model):
    name = models.CharField(max_length=100, help_text="EDL name")
    slug = models.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        db_table = "edls"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/edlprovider/edl/{str(self.slug)}"


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(help_text="IP Address of the device")
    name = models.CharField(max_length=100, help_text="Hostname")
    edl = models.ForeignKey(EDL, on_delete=models.CASCADE, related_name="ip_addresses")
    expiration_date = models.DateTimeField(help_text="Expires at")

    class Meta:
        db_table = "ip_addresses"

    def __str__(self):
        return f"{self.name} ({str(self.ip_address)})"


