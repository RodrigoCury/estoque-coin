from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('calendar/', TemplateView.as_view(template_name="app/calendar.html"),
         name='calendar'),
    path('leveduras/', views.YeastListView.as_view(), name="yeast_list"),
    path('leveduras/criar/',
         views.YeastCreateView.as_view(), name="yeast_create"),
    path('leveduras/repicar/<slug:slug>/',
         views.reinnoculate, name='yeast_reinnoculate'),
    path('leveduras/deletar/<slug:slug>/',
         views.delete_yeast_from_bank, name='yeast_delete'),
    path('leveduras/<slug:slug>/',
         views.YeastDetailView.as_view(), name="yeast_detail"),
    path('marcas/', views.BrandListView.as_view(), name="brand_list"),
    path('marcas/criar/', views.BrandCreateView.as_view(), name="brand_create"),
    path('marcas/deletar/<slug:slug>/',
         views.delete_brand_from_bank, name="brand_delete"),
    path('marcas/<slug:slug>/', views.BrandDetailView.as_view(), name="brand_detail"),
    path('perfil/', views.FermentativeProfileListView.as_view(), name="profile_list"),
    path('perfil/criar/', views.FermentativeProfileCreateView.as_view(),
         name="profile_create"),
    path('perfil/deletar/<slug:slug>/',
         views.delete_profile_from_bank, name="profile_delete"),
    path('perfil/<slug:slug>/',
         views.FermentativeProfileDetailView.as_view(), name="profile_detail"),
    path('todo/add', views.todoAdd, name='todo_add'),
    path('todo/complete/<int:id>', views.todoComplete, name='todo_complete'),
    path('todo/delete/<int:id>', views.todoDelete, name='todo_delete'),
]
