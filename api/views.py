from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.rag_service import process_urls
from .services.qa_service import ask_question

@api_view(['GET'])
def health_check(request):
    return Response({"status": "Backend running 🚀"})

@api_view(['POST'])
def process_urls_view(request):
    urls = request.data.get("urls", [])

    if not urls or not isinstance(urls, list):
        return Response(
            {"error": "Invalid URLs"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        index_id = process_urls(urls)
        return Response({"index_id": index_id})
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from .services.qa_service import ask_question

@api_view(['POST'])
def ask_view(request):
    question = request.data.get("question")
    index_id = request.data.get("index_id")

    if not question or not index_id:
        return Response(
            {"error": "Missing question or index_id"},
            status=400
        )

    # TEMP DEBUG (remove try-except)
    result = ask_question(question, index_id)

    return Response(result)