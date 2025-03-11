from django.shortcuts import render,HttpResponse
from . import models
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe
from django.db.models import Count
from .serializers import RecipeSerializer 
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly


class RecipePagination(PageNumberPagination):
    page_size = 5  # Show 5 recipes per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecipeListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        recipes = Recipe.objects.all()
        paginator = RecipePagination()
        paginated_queryset = paginator.paginate_queryset(recipes, request)
        serializer = RecipeSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
        

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Recipe_DetailView(APIView):
    
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response({"message": "Recipe deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PopularRecipeApi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        popular_recipes = Recipe.objects.values('title').annotate(title_count=Count('title')).order_by('-title_count')
        
        
        recipes = []
        for recipe in popular_recipes:
            recipe_instance = Recipe.objects.filter(title=recipe['title']).first()
            if recipe_instance:
                recipes.append(recipe_instance)

        # Serialize data
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)




# Create your views here.
def home(request):
    recipes=models.Recipe.objects.all()
    context={
        'recipes':recipes
    }
    return render(request,'recipes/home.html',context)

class RecipeListView(ListView):
    model=models.Recipe
    template_name='recipes/home.html'
    context_object_name='recipes'

class RecipeDetailView(DetailView):
    model=models.Recipe  
  

class RecipeCreateView(LoginRequiredMixin,CreateView):
    model=models.Recipe
    fields=['title','description']     

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RecipeUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=models.Recipe
    fields=['title','description']   

    def test_func(self):
        recipe=self.get_object()
        return self.request.user == recipe.author  

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

class RecipeDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=models.Recipe
    success_url=reverse_lazy('recipes-home') 

    def test_func(self):
        recipe=self.get_object()
        return self.request.user == recipe.author  


def about(request):
    return render(request,'recipes/about.html',{'title':'About us page'})