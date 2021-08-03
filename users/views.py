from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import UsersDetails
from .models import Ser

from .forms import UserDetailForm

# Create your views here.

#List
def create_view(request):

    context = {}

    form = UserDetailForm(request.POST or None)

    if form.is_valid():
        form.save()

    context['form'] = form

    return render(request, "create_view.html", context)

#List
def list_view(request):

    context = {}

    context["dataset"] = UsersDetails.objects.all()

    return render(request, "list_view.html", context)

#Update
def detail_view(request, id):

    context = {}

    context["data"] = UsersDetails.objects.get(id = id)

    return render(request, "detail_view.html", context)

#update
def update_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id=id)

    form = UserDetailForm(request.POST or None, instance = obj)

    if form.is_valid():

        form.save()

        return HttpResponseRedirect("/"+id)

    context["form"] = form

    return render(request, "update_view.html", context)

#Delte
def delete_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id = id)

    if request.method == "POST":

        obj.delete()

        return HttpResponseRedirect("/")

    return render(request, "delete_view.html", context)



