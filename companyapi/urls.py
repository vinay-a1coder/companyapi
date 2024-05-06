"""
URL configuration for companyapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('api.urls'))
    # path('accounts/login/', login, name='account-login'),
    path('login/', login, name='login'),
    path('register/', registration, name='registration'),
    path('update_user/<int:id>/', user_update_view, name='user-update'),
    path('delete/<int:pk>', delete_user, name='delete-user'),
    path('companies/', company_list, name='company-list'),
    path('companies/create/', company_create, name='company-create'),
    path('companies/<int:pk>/', company_detail, name='company-detail'),
    path('companies/<int:pk>/update/', company_update, name='company-update'),
    path('companies/<int:pk>/delete/', company_delete, name='company-delete'),
    path('send_message/<int:student_id>/', send_random_message, name='send-message'),
    path('add_student/', add_student, name='add-student')
]
