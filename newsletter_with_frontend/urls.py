from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.get_user_profile, name="get_user_profile"),
    path('profiles/', views.profile_list, name="profiles"),
    path('editor/<int:pk>/', views.editor, name="Editor"),
    path('snippets/', views.snippets),
]