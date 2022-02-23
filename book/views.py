from contextlib import redirect_stderr
from email import message
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookCreate
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    shelf = Book.objects.all()
    return render(request, 'book/home.html', {'shelf': shelf})

def upload(request):
    upload = BookCreate()
    if request.method == 'POST':
        upload = BookCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('index')
        else:
            return HttpResponse(""" Something went wrong. Please
            reload the webpage by clicking <a href="{{url:'index}}
            Reload</a>" """)

    else: 
        return render(request, 'book/add_form.html', {'add_form':
        upload})

def update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_shelf = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_form = BookCreate(request.POST or None, instance = 
    book_shelf)
    if book_form.is_valid():
        book_form.save()
        return redirect('index')
    return render(request, 'book/add_form.html', {'add_form':
    book_form})

def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_shelf = Book.objects.get(id = book_id)
    except Book.DoesNotExist:
        return redirect('index')
    book_shelf.delete()
    return redirect('index')

def login_page(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Username not Available')
            return redirect('/login/')
        
        user_obj = authenticate(username = username, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        messages.error(request, 'Invalid password')
        return redirect('/login/')


    return render(request, 'book/LoginForm/login.html')

def register_page(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username is taken')
            return redirect('/register/')

        user_obj = User.objects.create(
            username = username,
            first_name = first_name)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'Username Created')
        return redirect('/login/')

    return render(request, 'book/RegisterForm/register.html')

def logout_page(request):
    logout(request)
    return redirect('/login')