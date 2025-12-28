from django.urls import path
from . import views

app_name = 'poll_analytics'

urlpatterns = [
    # Микросервис 1: Статистика
    path('statistics/<int:question_id>/', views.poll_statistics, name='poll_statistics'),
    path('statistics/overall/', views.overall_statistics, name='overall_statistics'),
    
    # Микросервис 2: Диаграммы
    path('charts/<int:question_id>/', views.poll_chart, name='poll_chart'),
    path('charts/<int:question_id>/percentage/', views.poll_chart_percentage, name='poll_chart_percentage'),
    
    # Микросервис 3: Экспорт
    path('export/<int:question_id>/json/', views.export_poll_json, name='export_poll_json'),
    path('export/<int:question_id>/csv/', views.export_poll_csv, name='export_poll_csv'),
    
    # Микросервис 4: Поиск и фильтрация
    path('search/', views.poll_search, name='poll_search'),
]

