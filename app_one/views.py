from turtle import title
from xml.dom import minicompat
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from app_one.models import *
from django.shortcuts import redirect, render
import bcrypt


def index(request):
    return render(request, "Login_Reg.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            conf_pssword = request.POST["conf_pssword"]
            if(password == conf_pssword):

                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password.encode(), salt)
                User.objects.create(
                    first_name=first_name, last_name=last_name, email=email, password=hash.decode())
                messages.success(request, "User registered successfully")
            else:
                messages.error(
                    request, "Password must match the confirmed password")
            return redirect("/")
    return redirect("/register")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["loggedInUser"] = user.id
                return redirect("/books")

            messages.error(
                request, "incorrect Password")

        except User.DoesNotExist:
            messages.error(
                request, "You do not have an account ,Please Register first !")

        return redirect("/")
    return redirect("/")


def books(request):
    if "loggedInUser" in request.session:
        user = User.objects.get(id=request.session["loggedInUser"])
        context = {
            "user": user,
            "books": Book.objects.all(),
        }
        return render(request, "books.html", context)
    return redirect("/")


def addBook(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session["loggedInUser"])
        title = request.POST["title"]
        desc = request.POST["desc"]
        if len(title) < 5:
            messages.error(
                    request, "book title must be at least 5 characters")
            return redirect("/books")
        if len(desc) < 5:
            messages.error(
                    request, "book description must be at least 5 characters")
            return redirect("/books")
        else:            
            book = Book.objects.create(title=title,desc=desc,upladed_by=user)
            user.fav_book.add(book)
            messages.success(
                    request, "book added successfuly")
    return redirect("/books")

def viewFavBook(request,bookId):
        user = User.objects.get(id=request.session["loggedInUser"])
        book = Book.objects.get(id=bookId)
        context = {
            "user": user,
            "book": book,
            "favBook":book.user_favs.all(),
            "userfavBook":user.fav_book.filter(id=bookId)
        }
        return render(request, "viewFavbook.html", context)
    
def updateDesc(request,bookId):
    if request.method == "POST":
        desc = request.POST["newDesc"]
        title = request.POST["newTitle"]
        if len(title) < 5:
            messages.error(
                    request, "book title must be at least 5 characters")
            return redirect(f"/viewFavBook/{bookId}")
        if len(desc) < 5:
            messages.error(
                    request, "book description must be at least 5 characters")
            return redirect(f"/viewFavBook/{bookId}")
        else:            
            Book.objects.filter(id=bookId).update(title=title,desc=desc)
            messages.success(
                    request, "book info updated successfuly")
            return redirect(f"/viewFavBook/{bookId}")
    return redirect("/books")



def deleteBook(request,bookId):
        Book.objects.get(id=bookId).delete()
        return redirect("/books")
    
def unFav(request,bookId):
        user = User.objects.get(id=request.session["loggedInUser"])
        book = Book.objects.get(id=bookId)
        book.user_favs.remove(user)
        print("removed...")
        return redirect("/books")

def addFavBook(request,bookId):
        user = User.objects.get(id=request.session["loggedInUser"])
        book = Book.objects.get(id=bookId)
        book.user_favs.add(user)
        print("added...")
        return redirect("/books")

def logout(request):
    request.session.flush()
    return redirect("/")