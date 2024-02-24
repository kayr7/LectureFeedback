from django.urls import path
from .views import feedback_view, feedback_success, entity_qr_code, entities_overview

urlpatterns = [
    path('feedback/<str:entity_id>/', feedback_view, name='feedback'),
    path('success/', feedback_success, name='feedback_success'),
    path('qr/<str:entity_id>', entity_qr_code, name='entity_qr_code'),
    path('overview/', entities_overview, name='entities_overview'),
]