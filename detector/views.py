from django.shortcuts import render
from detector.models import Detection
from django.core import serializers
from django.http import JsonResponse

def ai_dashboard(request):
    # Get the latest detection
    latest_detection = Detection.objects.order_by('-input__timestamp').first()
    
    context = {
        'detection': latest_detection,
        'model_version': 'v2.3.1',  # May be fetched from a config file or environment variable
        'model_name': 'Badger Detector',  # May be fetched from a config file or environment variable
    }
    return render(request, 'detector/aip.html', context)