from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'auth/login.html')

def profiles_view(request):
    return render(request, 'profiles/list.html')

def profile_detail_view(request, user_id):
    return render(request, 'profiles/detail.html', {'user_id': user_id})

def input_referral_view(request):
    return render(request, 'profiles/input_referral.html')