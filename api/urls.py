from django.urls import path
from .views import health_check, process_urls_view, ask_view

urlpatterns = [
    path('health/', health_check),
path('process-urls/', process_urls_view),
path('ask/', ask_view),
]