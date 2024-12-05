from django.urls import path
from .views import home, profile, RegisterView, select_tech_stack

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('select-tech-stack/', select_tech_stack, name='select_tech_stack'),
]
