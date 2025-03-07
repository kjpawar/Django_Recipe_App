from django.contrib import admin
from django.urls import path
from . import views
from .views import RecipeListCreateView, Recipe_DetailView,PopularRecipeApi


urlpatterns = [
    
    path('api/recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('api/recipes/<int:pk>/', Recipe_DetailView.as_view(), name='recipe-detail'),
    path('api/recipes/popular/',PopularRecipeApi.as_view()),
    path('',views.RecipeListView.as_view(),name="recipes-home"),
    path('recipe/<int:pk>/',views.RecipeDetailView.as_view(),name="recipes-detail"),
    path('recipe/<int:pk>/update/',views.RecipeUpdateView.as_view(),name="recipes-update"),
    path('recipe/<int:pk>/delete/',views.RecipeDeleteView.as_view(),name="recipes-delete"),
    path('recipe/create/',views.RecipeCreateView.as_view(),name="recipes-create"),
    path('about/',views.about,name="recipes-about"),
]
