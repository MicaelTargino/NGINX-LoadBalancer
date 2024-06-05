import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render

load_dotenv()

# Create your views here.
def answer_response(request):
    return JsonResponse({'instance': os.getenv("INSTANCE", 'UNKNOWN')})