from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html', 
                  { 'message': 'Bienvienido a la tienda', 
                   'title': 'Listado de Productos', 
                   'products': [
                       {'title': 'remera', 'price': 5000, 'stock': True},
                       {'title': 'campera', 'price': 15000, 'stock': True},
                       {'title': 'pantalon', 'price': 4000, 'stock': False}                                              
                   ]})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'usuarios/login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente')
    return redirect('login')
