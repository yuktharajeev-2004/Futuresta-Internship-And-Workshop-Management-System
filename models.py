from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    usertype=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.username
    
    
class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.BigIntegerField()
    college=models.CharField(max_length=100,null=True)
    dept=models.CharField(max_length=100)
    year=models.IntegerField()
    reg_no = models.CharField(max_length=100)
    resume=models.FileField(upload_to='resume/')
    # address=models.TextField()
    reg_date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Company(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.BigIntegerField()
    address=models.TextField()
    proof=models.FileField(upload_to='company_proof/')
    reg_date=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Jobs(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    jobTitle=models.CharField(max_length=50,null=True)
    jobcategory=models.CharField(max_length=50,null=True)
    jobdesc=models.CharField(max_length=50,null=True)
    # jobresponsibility=models.CharField(max_length=50,null=True)
    location=models.CharField(max_length=50,null=True)
    vacancy=models.CharField(max_length=50,null=True)
    salary=models.CharField(max_length=50,null=True)
    # experience=models.CharField(max_length=50,null=True)
    qualification=models.CharField(max_length=50,null=True)
    deadline=models.DateField()
    image=models.FileField(upload_to='profile/',null=True)


class Apply_jobs(models.Model):
    jobId = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, default='Applied')
    applyDate = models.DateField(auto_now=True)
    resume=models.FileField(upload_to='resumeApplied/',null=True)
    # expected_salary = models.CharField(max_length=50, null=True)
    cover_letter = models.TextField(null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)




class Workshop(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=150)
    seats = models.PositiveIntegerField()
    fee = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='workshops/')
    eligibility = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Apply_Workshops(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, default='Applied')
    attendence = models.IntegerField( null=True)
    certificate = models.FileField(upload_to="certificates/",null=True)
    applyDate = models.DateField(auto_now=True)