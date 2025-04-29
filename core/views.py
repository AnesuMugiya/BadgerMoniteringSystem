from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Log in required decorator ensures that only logged in users can access the dashboard
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')