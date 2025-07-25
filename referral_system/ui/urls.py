from django.urls import path
from ui import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('profiles/', views.profiles_view, name='profiles'),
    path('profiles/<int:user_id>/', views.profile_detail_view, name='profile_detail'),
    path('input-referral/', views.input_referral_view, name='input_referral'),
]