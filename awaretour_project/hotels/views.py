from rest_framework.views import APIView  # Добавляем импорт APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Функция для отправки POST-запросов к AwareTour API
def post_request(endpoint, data):
    url = f"https://api.awaretour.com/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response, None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Представление для поиска направления
class SearchDestinationView(APIView):
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "culture": "en-US",
            "query": query
        }
        response, error = post_request("/hotel/search-destination", data)

        if response:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Представление для поиска отелей
class SearchHotelsView(APIView):
    def post(self, request):
        destination_type = request.data.get('destination_type')
        destination = request.data.get('destination')
        check_in = request.data.get('check_in')
        nights = request.data.get('nights')
        nationality = request.data.get('nationality', 'RU')
        adults = request.data.get('adults', 2)
        children = request.data.get('children', [])

        if not destination_type or not destination or not check_in or not nights:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "destination_type": destination_type,
            "destination": destination,
            "roomCriteria": [
                {
                    "adult": adults,
                    "childAges": children
                }
            ],
            "nationality": nationality,
            "check_in": check_in,
            "night": nights,
            "currency": "TRY",
            "culture": "tr-TR"
        }
        response, error = post_request("/hotel/search-hotels", data)

        if response:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({"error": error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
