"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('admin_home/',views.admin_home),
    path('app_login/',views.app_login),
    path('admin_change_password/',views.admin_change_password),
    path('admin_change_password_post/',views.admin_change_password_post),
    path('admin_view_user/',views.admin_view_user),
    path('admin_add_food/',views.admin_add_food),
    path('admin_add_food_post/',views.admin_add_food_post),
    path('admin_view_food_database/',views.admin_view_food_database),
    path('admin_view_complaint/',views.admin_view_complaint),
    path('admin_send_reply/',views.admin_send_reply),
    path('admin_send_reply_post/',views.admin_send_reply_post),
    path('admin_view_feedback/',views.admin_view_feedback), 
    path('admin_delete_food_database/<id>',views.admin_delete_food_database),
    path('admin_edit_food/<id>',views.admin_edit_food),
    path('admin_edit_food_post/',views.admin_edit_food_post),
    path('user_signup/',views.user_signup),
    path('user_change_password_post/',views.user_change_password_post),
    path('user_add_health_profile_post/',views.user_add_health_profile_post),
    path('user_add_daily_food_log_post/',views.user_add_health_profile_post),
    path('view_profile/',views.view_profile),
    path('edit_profile/',views.edit_profile),
    path('send_feedback/',views.send_feedback),
    path('view_health_profile/',views.view_health_profile),
    path('upload_food/',views.upload_food),
    path('today_nutrition_summary/',views.today_nutrition_summary),
    path('edit_health_profile/',views.edit_health_profile),
    path('userviewhishealth/',views.userviewhishealth),
    path('analyze_ingredients/',views.analyze_ingredients),
    path("get_food_suggestions/", views.get_food_suggestions),
    path('and_forget_password_post/',views.and_forget_password_post),
    path('food_prediction/',views.food_predictions),



]  

