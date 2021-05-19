from django.db import models
import re
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters"
        if len(postData['first_name']) == 0:
            errors['first_name'] = "You must provide a first name"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "You must provide a last name"    
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 5:
            errors['password'] = "Your password must be at least 5 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class RecipeManager(models.Manager):
    def recipe_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "A title must consist of at least 3 characters!"
        if len(postData['title']) == 0:
            errors['title'] = "A title must be provided!"
        if len(postData['description']) < 3:
            errors['description'] = "A description must consist of at least 3 characters!"
        if len(postData['description']) == 0:
            errors['description'] = "A description must be provided!"
        if len(postData['ingredients']) < 3:
            errors['ingredients'] = "The ingredients list must consist of at least 3 characters!"
        if len(postData['ingredients']) == 0:
            errors['ingredients'] = "Ingredients must be provided!"
        if len(postData['instructions']) < 20:
            errors['instructions'] = "Please provide adequate instructions!"
        if len(postData['instructions']) == 0:
            errors['instructions'] = "Instructions must be provided!"
        return errors

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        if len(postData['content']) < 10:
            errors['content'] = "Please leave review of at least 10 characters"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(null=True, blank=True)
    objects = UserManager()
    #user_reviews = []

class Recipe(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    instructions = models.CharField(max_length=100)
    ingredients = models.TextField()
    user_recipe = models.ForeignKey(User, related_name='user_recipe', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    recipe_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    objects = RecipeManager()

class Review(models.Model):
    content = models.TextField()
    user_review = models.ForeignKey(User, related_name="user_reviews", on_delete=models.CASCADE)
    recipe_reviewed = models.ForeignKey(Recipe, related_name="recipe_reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

class Drink(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    instructions = models.CharField(max_length=100)
    ingredients = models.TextField()
    user_drink = models.ForeignKey(User, related_name='user_drink', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    recipe_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    objects = RecipeManager()

class DrinkReview(models.Model):
    content = models.TextField()
    user_review = models.ForeignKey(User, related_name="user_Drinkreviews", on_delete=models.CASCADE)
    drink_reviewed = models.ForeignKey(Drink, related_name="drink_reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()