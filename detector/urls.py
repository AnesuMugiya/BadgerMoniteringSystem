from django.urls import path
from . import views

urlpatterns = [
    path('ai-dashboard/', views.ai_dashboard, name='ai_dashboard'),
    # path('api/latest-detection/', views.get_latest_detection, name='get_latest_detection'),
]