from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


@login_required(login_url="/login/")
def recipe(request):
    if request.method == "POST":
        data = request.POST

        receipe_name = data.get("receipe_name")
        receipe_desc = data.get("receipe_desc")
        receipe_image = request.FILES.get("receipe_image")

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_desc=receipe_desc,
            receipe_image=receipe_image
        )

        return redirect("/recipes/")

    allRecipes = Receipe.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        allRecipes = allRecipes.filter(
            receipe_name__icontains=request.GET.get('search'))

    context = {'recipes': allRecipes}
    return render(request, "recipes.html", context)


@login_required(login_url="/login/")
def update_recipe(request, id):
    queryset = Receipe.objects.get(id=id)
    allRecipes = Receipe.objects.all()

    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_desc = data.get("receipe_desc")
        receipe_image = request.FILES.get("receipe_image")

        queryset.receipe_name = receipe_name
        queryset.receipe_desc = receipe_desc

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()

        return redirect('/recipes/')

    context = {'recipe': queryset, 'recipes': allRecipes}
    return render(request, 'recipes.html', context)


@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect("/recipes/")


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect('/login/')

        else:
            login(request, user)
            return redirect('/recipes/')

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already exits.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()
        messages.success(request, "User created successfully!")

        return redirect('/login/')

    return render(request, "register.html")


def get_student(request):
    queryset = Student.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(student_name__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(department__department__icontains=search) |
            Q(student_email__icontains=search) |
            Q(student_age__icontains=search)
        )

    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "reports/students.html", {'students': page_obj})
