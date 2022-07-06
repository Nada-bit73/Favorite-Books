from django.urls import path
from . import views
#urlpatterns => static name
urlpatterns = [
# mapping '/' to index function in views file
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),  
    path('books', views.books),  
    path('addBook', views.addBook),  
    path('viewFavBook/<int:bookId>', views.viewFavBook),  
    path('addFavBook/<int:bookId>', views.addFavBook),  
    path('deleteBook/<int:bookId>', views.deleteBook),  
    path('updateDesc/<int:bookId>', views.updateDesc),  
    path('unFav/<int:bookId>', views.unFav),  
]
