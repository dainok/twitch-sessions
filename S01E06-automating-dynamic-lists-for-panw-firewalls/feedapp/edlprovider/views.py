
from django.views import View
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound
from . import models

# Create your views here.
class EDL(View):
    def get(self, request, edl_slug=None):
        now = timezone.now()

        try:
            edl_o = models.EDL.objects.get(pk=edl_slug)
        except models.EDL.DoesNotExist:
            return HttpResponseNotFound("EDL not found")
            
        ip_addresses = list(edl_o.ip_addresses.filter(expiration_date__gt=now).values_list("ip_address", flat=True))

        if not ip_addresses:
            ip_addresses.append("0.0.0.0/32")

        return HttpResponse("\n".join(ip_addresses), content_type="text/plain")
