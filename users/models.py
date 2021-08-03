from django.db import models
#from django import forms

# All the models

class UsersDetails(models.Model):

    #Personal Details
    name = models.CharField(max_length=30, default='YOUR NAME')

    gender = models.CharField(max_length=1, default="")
    
    phone = models.CharField(max_length=11, default="YOUR NUMBER")
    
    address = models.TextField(default="YOUR ADDRESS")
    
    date_of_birth = models.DateTimeField()


    #Account Details
    username = models.CharField(max_length=10, default='YOUR USERNAME')
    
    email = models.EmailField(('email address'), unique = True, default="YOUR EMAIL ADDRESS")
    
    # #password = forms.CharField(widget=forms.PasswordInput)



    def __str__(self):
        return "%the user details are %s" % (self.name, self.gender, self.phone, self.address, self.date_of_birth, self.username, self.email, self.password)



class Ser(models.Model):
    ser = models.OneToOneField(UsersDetails, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "%the serial is" % (self.ser)
