from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
def mainMenu(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'MainMenu.html')
    return HttpResponseRedirect('../login')
    
def orderManagement(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'OrderManagement.html')
    return HttpResponseRedirect('../login')