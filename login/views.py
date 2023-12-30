from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logIn(request):
    if request.method == "GET":
        return render(request, "Login.html")
    elif request.method == "POST":
        name = request.POST["loginLog"]
        password = request.POST["loginPass"]

        user = authenticate(request, username=name, password=password)
        
        if user is not None:
            login(request, user)
            if user.owner == False:
                return HttpResponseRedirect('/main_menu')
            return HttpResponseRedirect('/owner')
        else:
            return render(request, 'Login.html', {"wrong":1})
    elif request.method == "PUT":
        logout(request)
        return HttpResponse(status = 200)