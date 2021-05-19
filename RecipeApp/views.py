from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Recipe, Review
import bcrypt
# Create your views here.

def index(request):
    return render(request, 'index.html')

#Create User
def create_user(request):
    if request.method == "POST":
        #validation
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        #validation end
        

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = new_user.id
        return redirect('/user/dashboard')
    return redirect("/")

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/user/dashboard')
        messages.error(request, "email or password are incorrect!")

    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    
    context = { 
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'all_recipes' : Recipe.objects.all
    }
    return render(request, 'dashboard.html', context)

def create_recipe(request):
    if request.method == "POST":
        ##
        errors = Recipe.objects.recipe_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/recipe/recipe_form')
        ##
        user = User.objects.get(id=request.session['logged_user'])
        Newrecipe = Recipe.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            ingredients = request.POST['ingredients'],
            instructions = request.POST['instructions'],
            user_recipe = user
        )
    return redirect(f'/user/dashboard')
    
def recipe_form(request):
    context = { 
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'recipe': Recipe.objects.all()
    }
    return render(request, 'new_recipe.html', context)

def show_recipe(request, recipe_id):
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'recipe' : Recipe.objects.get(id=recipe_id)
    }
    return render(request, 'user_recipe.html', context)

def update(request, recipe_id):
    
    if request.method == "POST":
        ###
        context = { 
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'recipe': Recipe.objects.get(id=recipe_id)
        }
        errors = Recipe.objects.recipe_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return render(request, 'update.html', context)
        ###
        recipe_update = Recipe.objects.get(id=recipe_id)
        user = User.objects.get(id=request.session['logged_user'])
        recipe_update.title = request.POST['title']
        recipe_update.description = request.POST['description']
        recipe_update.ingredients = request.POST['ingredients']
        recipe_update.instructions = request.POST['instructions']
        recipe_update.user_recipe = user
        recipe_update.save()
    return redirect(f'/user/dashboard')

def update_form(request, recipe_id):
    
    context = { 
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'recipe': Recipe.objects.get(id=recipe_id)
    }
    return render(request, 'update.html', context)

def user_page(request, user_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    user = User.objects.get(id=user_id)

    context = {
        'one_user': user
    }
    return render(request, 'user_page.html', context)

def delete(request, recipe_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return redirect(f'/user/dashboard')

def add_review(request):
    # if 'logged_user' not in request.session:
    #     return redirect('/')
    if request.method == "POST":

        recipe = Recipe.objects.get(id=request.POST['recipe_reviewed'])
        errors = Review.objects.review_validator(request.POST)

        if errors:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect(f'/recipe/{recipe.id}')
        
        user = User.objects.get(id=request.session['logged_user'])
        review = Review.objects.create(
            content = request.POST['content'], 
            recipe_reviewed = recipe, user_review = user)

        return redirect(f'/recipe/{recipe.id}')

def delete_review(request, review_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(f'/recipe/{review.recipe_reviewed.id}')


