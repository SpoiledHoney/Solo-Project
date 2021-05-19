from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('user/dashboard', views.dashboard),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('recipe/recipe_form', views.recipe_form),
    path('recipe/create', views.create_recipe),
    path('recipe/<int:recipe_id>', views.show_recipe),
    path('recipe/<int:recipe_id>/recipe_update', views.update_form),
    path('recipe/<int:recipe_id>/update', views.update),
    path('recipe/<int:recipe_id>/delete', views.delete),
    path('recipe/add_review', views.add_review),
    path('review/<int:review_id>/delete_review', views.delete_review),
    path('user/<int:user_id>', views.user_page),
    path('user/<int:logged_user>', views.user_page),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)