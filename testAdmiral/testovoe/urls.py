from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'testovoe'

urlpatterns = [
    path('category/', views.CatView.as_view(),name='list'),
    path('category/<int:pk>', views.CatDetailView.as_view(), name="detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
