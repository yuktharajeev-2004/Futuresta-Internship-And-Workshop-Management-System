"""
URL configuration for onlinejob project.

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
from django.urls import path
from jobapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('studentRegister', views.studentRegister, name='studentRegister'),
    path('companyRegister', views.companyRegister, name='companyRegister'),
    path('login', views.login, name='login'),

    path('adminHome', views.adminHome, name='adminHome'),
    path('adminstudent', views.adminstudent, name='adminstudent'),
    path('adm_app_student', views.adm_app_student, name='adm_app_student'),
    path('admincompany', views.admincompany, name='admincompany'),
    path('adm_app_company', views.adm_app_company, name='adm_app_company'),
    path('adminJobs', views.adminJobs, name='adminJobs'),
    path('adminviewApplications', views.adminviewApplications, name='adminviewApplications'),
    path('adminWorkshops', views.adminWorkshops, name='adminWorkshops'),
    path('admWorkAppView', views.admWorkAppView, name='admWorkAppView'),

    path('companyHome', views.companyHome, name='companyHome'),
    path('companyPost', views.companyPost, name='companyPost'),
    path('companyJobs', views.companyJobs, name='companyJobs'),
    path('companyviewApplications', views.companyviewApplications, name='companyviewApplications'),
    path('compupdateApplicationStatus', views.compupdateApplicationStatus, name='compupdateApplicationStatus'),
    path('companyAddWorkshop', views.companyAddWorkshop, name='companyAddWorkshop'),
    path('compWorkshopAppli', views.compWorkshopAppli, name='compWorkshopAppli'),
    path('compWorkAppView', views.compWorkAppView, name='compWorkAppView'),
    path('compUploadCertificate', views.compUploadCertificate, name='compUploadCertificate'),


    path('studentHome', views.studentHome, name='studentHome'),
    path('studentJobs', views.studentJobs, name='studentJobs'),
    path('studJobDetails', views.studJobDetails, name='studJobDetails'),
    path('studentapplyjob', views.studentapplyjob, name='studentapplyjob'),
    path('studentApplied', views.studentApplied, name='studentApplied'),
    path('studentWorkshop', views.studentWorkshop, name='studentWorkshop'),
    path('studWorkDetails', views.studWorkDetails, name='studWorkDetails'),
    path('studentWorkshopPay', views.studentWorkshopPay, name='studentWorkshopPay'),
    path('studentAppliedWork', views.studentAppliedWork, name='studentAppliedWork'),
]
