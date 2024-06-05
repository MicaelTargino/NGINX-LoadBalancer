from django.urls import path
from .views import answer_response

urlpatterns = [
    path('', answer_response)
]