from django.urls import path
from .views import get_ai_response 
urlpatterns= [
    path('get-ai-response/', get_ai_response,name='get_ai_response'),
]