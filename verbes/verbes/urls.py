"""verbes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.i18n import JavaScriptCatalog
from verbes_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('verbes/', views.verbe_list, name='verbe-list'),
    path('verbes/table/<int:table_id>/', views.table_detail, name='table-detail'),
    path('verbes/table/', views.table_list, name='table-list'),
    path('verbes/table/add/', views.table_create, name='table-create'),
    path('verbes/table/<int:table_id>/exercise/', views.exercise, name='exercise'),
    path('verbes/table/<int:table_id>/exercise/result/', views.exercise_result,
         name='exercise-result')
]
