from django import forms
from .models import UsersDetails
 
 
# creating a form
class UserDetailForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = UsersDetails
 
        # specify fields to be used
        fields = [
            "name",
            "gender",
            "phone",
            "address",
            "date_of_birth",
            "username",
            "email",
        ]