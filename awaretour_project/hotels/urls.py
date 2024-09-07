from django.urls import path
from .views import SearchDestinationView, SearchHotelsView

urlpatterns = [
    path('api/search-destination/', SearchDestinationView.as_view(), name='search_destination'),
    path('api/search-hotels/', SearchHotelsView.as_view(), name='search_hotels'),
]
