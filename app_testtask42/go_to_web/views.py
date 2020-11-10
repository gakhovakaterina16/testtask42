from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'go_to_web/men_20_25_vk.html')
