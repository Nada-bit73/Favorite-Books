from django.db import models
import re
from django.db import models


class ShowManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not postData["first_name"]:
            errors["first_name"] = "Please enter your first name"
        elif len(postData["first_name"]) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        elif not re.match(r'^[a-zA-Z]+$', postData["first_name"]):
            errors["first_name"] = "first name should contain letters only"

        if not postData["last_name"]:
            errors["last_name"] = "Please enter your last name"
        elif len(postData["last_name"]) < 2:
            errors["last_name"] = "last name should be at least 2 characters"
        elif not re.match(r'^[a-zA-Z]+$', postData['last_name']):
            errors["last_name"] = "last name should contain letters only"

        if not postData["email"]:
            errors["email"] = "Please enter your email"
        elif not re.match(EMAIL_REGEX, postData['email']):
            errors["email"] = "email should be in example@example.com formate"
        elif User.objects.filter(email=postData["email"]).exists():
            errors["email"] = "email is already exist"

        if not postData["password"]:
            errors["password"] = "Please enter your password"
            # string like (gr3at@3wdsG)
        elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', postData['password']):
            errors["password"] = "password should be strong"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45,null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    upladed_by = models.ForeignKey(User, related_name="books",on_delete=models.CASCADE,blank=True,null=True)
    user_favs = models.ManyToManyField(User, related_name="fav_book",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    