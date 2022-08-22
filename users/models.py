from django.db import models
#from django import forms

# All the models

class UsersDetails(models.Model):

    #Personal Details
    name = models.CharField(max_length=30, default='YOUR NAME')

    # Choose Gender
    gender_options = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    gender = models.CharField(max_length=10, choices=gender_options, default="Male")
    
    phone = models.CharField(max_length=20, default="YOUR NUMBER")
    
    credit_card = models.CharField(max_length=20, default="YOUR CREDIT CARD")


    #Account Details
    username = models.CharField(max_length=10, default='YOUR USERNAME')
    
    email = models.EmailField(('email address'), unique = True, default="YOUR EMAIL ADDRESS")
    
    password = models.CharField(max_length=30, default="YOUR PASSWORD")



    def __str__(self):
        return self.name



class Ser(models.Model):
    ser = models.OneToOneField(UsersDetails, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "the serial is" % (self.ser)
