from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.db.models import Q
from jobapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def studentRegister(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['mobile']
        password = request.POST['password']
        college = request.POST['college']
        department = request.POST['department']
        year = request.POST['year']
        register_number = request.POST['register_number']
        resume = request.FILES['resume']
        if CustomUser.objects.filter(username=email).exists():
            messages.info(request,'Username/email already registred..')
            return redirect("/studentRegister")
        elif Student.objects.filter(Q(phone=phone)).exists() or Company.objects.filter(Q(phone=phone)).exists():
            messages.info(request,'Phone number already registred..')
            return redirect("/studentRegister")
        else:
            usr = CustomUser.objects.create_user(
                username=email, password=password, is_active=0, usertype='Student')
            usr.save()
            par = Student.objects.create(
                name=name, email=email, phone=phone, dept=department, college = college,year = year,reg_no=register_number, resume=resume, user=usr)
            par.save()
            messages.info(request,"Regisgteration Successfull...")
            return redirect('/studentRegister')
    else:
        return render(request, 'studentRegister.html',{'msg': msg})

def companyRegister(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['mobile']
        password = request.POST['password']
        address = request.POST['address']
        proof = request.FILES['proof']
        if CustomUser.objects.filter(username=email).exists():
            messages.info(request,'Username/email already registred..')
            return redirect("/companyRegister")
        elif Student.objects.filter(Q(phone=phone)).exists() or Company.objects.filter(Q(phone=phone)).exists():
            messages.info(request,'Phone number already registred..')
            return redirect("/companyRegister")
        else:
            usr = CustomUser.objects.create_user(
                username=email, password=password, is_active=0, usertype='Company')
            usr.save()
            par = Company.objects.create(
                name=name, email=email, phone=phone, address=address, proof=proof, user=usr)
            par.save()
            messages.info(request,"Regisgteration Successfull...")
            return redirect('/companyRegister')
    else:
        return render(request, 'companyRegister.html',{'msg': msg})

def login(request):
    msg = ""
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        auth = authenticate(username=email, password=password)

        if auth is not None:

            if auth.is_superuser:
                return redirect("/adminHome")
            elif auth.usertype == 'Student':
                st = Student.objects.get(email=email)
                request.session['id'] = st.id
                return redirect("/studentHome")
            elif auth.usertype == 'Company':
                st = Company.objects.get(email=email)
                request.session['id'] = st.id
                return redirect("/companyHome")
        else:
            msg = "Invalid username/password!"
            return render(request, "login.html", {"msg": msg})
    else:
        return render(request, 'login.html',{'msg': msg})

def adminHome(request):
    return render(request, 'adminHome.html')

def adminstudent(request):
    students = Student.objects.filter().order_by('-id')
    return render(request, 'adminstudent.html', {'data': students})


def adm_app_student(request):
    id = request.GET['id']
    status = request.GET['status']
    data = CustomUser.objects.get(id=id)
    if status=='active':
        data.is_active = 1
    else:
        data.is_active = 0
    data.save()
    return redirect("/adminstudent")



def admincompany(request):
    companies = Company.objects.filter().order_by('-id')
    return render(request, 'admincompany.html', {'data': companies})


def adm_app_company(request):
    id = request.GET['id']
    status = request.GET['status']
    data = CustomUser.objects.get(id=id)
    if status=='active':
        data.is_active = 1
    else:
        data.is_active = 0
    data.save()
    return redirect("/admincompany")


def adminJobs(request):
    jobs = Jobs.objects.filter().order_by('-id')
    return render(request, 'adminJobs.html', {'jobs': jobs})

def adminWorkshops(request):
    jobs = Workshop.objects.filter().order_by('-id')
    return render(request, 'adminWorkshops.html', {'data': jobs})


def adminviewApplications(request):
    id=request.GET.get('id')
    job=Jobs.objects.get(id=id)
    applied_jobs = Apply_jobs.objects.filter(jobId=job)  # Get applications for the
    
    if request.method == 'POST':
        date = request.POST.get('date')
        application_id = request.POST.get('application_id')
        application = get_object_or_404(Apply_jobs, id=application_id)
        application.interview_date = date
        application.status = 'Interview Scheduled'
        application.save()
        return redirect('/adminviewApplications?id=' + str(job.id))
    return render(request, 'adminviewApplications.html', {'applied_jobs': applied_jobs})

def admWorkAppView(request):
    id = request.GET.get('id')
    workshop = Workshop.objects.get(id=id)
    appli = Apply_Workshops.objects.filter(workshop=workshop).order_by("-id")
    return render(request, 'admWorkAppView.html', {"data": appli})

def companyHome(request):
    return render(request, 'companyHome.html')


def companyPost(request):
    uid = request.session.get('id')  # Use get() to prevent key errors
    company = Company.objects.get(id=uid)
    
    if request.method == 'POST':
        jobTitle = request.POST.get('jobTitle', '')
        jobcategory = request.POST.get('jobCategory', '')
        jobdesc = request.POST.get('jobdesc', '')
        vacancy = request.POST.get('vacancy', '')
        jobresponsibility = request.POST.get('jobresponsibility', '')
        location = request.POST.get('location', '')
        salary = request.POST.get('salary', '')
        experience = request.POST.get('experience', '')
        qualification = request.POST.get('qualification', '')
        deadline = request.POST.get('deadline', '')

        image = request.FILES.get('image', None)  # Use .get() to prevent errors

        if company:
            job = Jobs.objects.create(
                company=company,
                jobTitle=jobTitle,
                jobcategory=jobcategory,
                jobdesc=jobdesc,
                # jobresponsibility=jobresponsibility,
                location=location,
                salary=salary,
                # experience=experience,
                qualification=qualification,
                deadline=deadline,
                image=image,
                vacancy=vacancy
            )
            messages.info(request, "Job posted successfully.")
            return redirect('/companyPost')
    return render(request, 'companyPost.html')





def companyJobs(request):
    uid = request.session.get('id')  # Use get() to prevent key errors
    company = Company.objects.get(id=uid)
    jobs = Jobs.objects.filter(company=company).order_by('-id')
    return render(request, 'companyJobs.html', {'jobs': jobs})



def companyviewApplications(request):
    uid = request.session.get('id') 
    id=request.GET.get('id')
    company=Company.objects.get(id=uid)
    job=Jobs.objects.get(id=id)
    applied_jobs = Apply_jobs.objects.filter(jobId=job).order_by("-id")  # Get applications for the
    
    if request.method == 'POST':
        date = request.POST.get('date')
        application_id = request.POST.get('application_id')
        application = get_object_or_404(Apply_jobs, id=application_id)
        application.interview_date = date
        application.status = 'Interview Scheduled'
        application.save()
        subject = "Your Application Status Changed!"
        message = f"Hello {application.student.name}, Your application status for {application.jobId.jobTitle} has been updated. Kindly log in to the website to check it."
        send_mail(subject, message, 'futurestainternworkshop2004@gmail.com', [application.student.email])
        return redirect('/companyviewApplications?id=' + str(job.id))
    return render(request, 'companyviewApplications.html', {'applied_jobs': applied_jobs})




def compupdateApplicationStatus(request):
    id = request.GET.get('id')
    status = request.GET.get('status')
    application = get_object_or_404(Apply_jobs, id=id)
    application.status = status
    application.save()
    subject = "Your Application Status Changed!"
    message = f"Hello {application.student.name}, Your application status for {application.jobId.jobTitle} has been updated. Kindly log in to the website to check it."
    send_mail(subject, message, 'futurestainternworkshop2004@gmail.com', [application.student.email])
    return redirect('/companyviewApplications?id=' + str(application.jobId.id))



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Workshop, Company

def companyAddWorkshop(request):
    uid = request.session.get('id')
    company = Company.objects.get(id=uid)

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        seats = int(request.POST.get("seats"))
        fee = int(request.POST.get("fee"))
        location = request.POST.get('location')
        eligibility = request.POST.get('eligibility')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        image = request.FILES.get('image')

        Workshop.objects.create(
            title=title,
            category=category,
            seats=seats,
            fee=fee,
            location=location,
            eligibility=eligibility,
            description=description,
            deadline=deadline,
            image=image,
            organizer=company  # if you added FK, else remove this line
        )

        messages.success(request, "Workshop posted successfully.")
        return redirect('/companyAddWorkshop')

    return render(request, 'companyAddWorkshop.html')



def compWorkshopAppli(request):
    uid = request.session.get('id') 
    id=request.GET.get('id')
    company=Company.objects.get(id=uid)
    workshop=Workshop.objects.filter(organizer=company).order_by("-id")
    # applied_jobs = Apply_jobs.objects.filter(jobId=job).order_by("-id")  # Get applications for the
    
    # if request.method == 'POST':
    #     date = request.POST.get('date')
    #     application_id = request.POST.get('application_id')
    #     application = get_object_or_404(Apply_jobs, id=application_id)
    #     application.interview_date = date
    #     application.status = 'Interview Scheduled'
    #     application.save()
    #     subject = "Your Application Status Changed!"
    #     message = f"Hello {application.student.name}, Your application status for {application.jobId.jobTitle} has been updated. Kindly log in to the website to check it."
    #     send_mail(subject, message, 'futurestainternworkshop2004@gmail.com', [application.student.email])
    #     return redirect('/compWorkshopAppli?id=' + str(job.id))
    return render(request, 'compWorkshopAppli.html',{"data":workshop})

# def compWorkAppView(request):
#     uid = request.session.get('id') 
#     id=request.GET.get('id')
#     company=Company.objects.get(id=uid)
#     workshop=Workshop.objects.get(id=id)
#     appli=Apply_Workshops.objects.filter(workshop=workshop).order_by("-id")
#     # applied_jobs = Apply_jobs.objects.filter(jobId=job).order_by("-id")  # Get applications for the
    
#     if request.method == 'POST':
#         attendance = int(request.POST.get('attendance'))
#         app_id = request.POST.get('app_id')
#         application = Apply_Workshops.objects.get(id=app_id)
#         application.attendence +=int(attendance)
#         application.save()
#         return redirect('/compWorkAppView?id=' + str(id))
#     return render(request, 'compWorkAppView.html',{"data":appli})


def compWorkAppView(request):
    uid = request.session.get('id') 
    id = request.GET.get('id')

    company = Company.objects.get(id=uid)
    workshop = Workshop.objects.get(id=id)
    appli = Apply_Workshops.objects.filter(workshop=workshop).order_by("-id")

    if request.method == 'POST':
        attendance = int(request.POST.get('attendance'))
        app_id = request.POST.get('app_id')

        application = Apply_Workshops.objects.get(id=app_id)

        # FIX: handle None
        if application.attendence is None:
            application.attendence = 0

        application.attendence += attendance
        application.save()

        return redirect('/compWorkAppView?id=' + str(id))

    return render(request, 'compWorkAppView.html', {"data": appli})


def compUploadCertificate(request):
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        certificate = request.FILES.get('certificate')

        application = Apply_Workshops.objects.get(id=app_id)
        workshop_id = application.workshop.id
        application.certificate=certificate
        application.save()
        messages.info(request,"Certificate Uploaded successfully!")
        return redirect('/compWorkAppView?id=' + str(workshop_id))
    return redirect("/compWorkAppView")



def studentHome(request):
    return render(request, 'studentHome.html')

from datetime import date
def studentJobs(request):
    today= date.today()
    print(today,"######################")
    query = request.GET.get('search', '')  # Get the search term from the request
    if query:
        data = Jobs.objects.filter(jobTitle__icontains=query).order_by('-id')  # Filter jobs based on the title
    else:
        data = Jobs.objects.all().order_by('-id')  # Show all jobs if no search query
    return render(request, 'studentJobs.html', {'data': data,"today":today})


def studJobDetails(request):
    job_id = request.GET.get('job_id')
    job = Jobs.objects.get(id=job_id)
    return render(request, 'studJobDetails.html', {'job': job})




def studentapplyjob(request):
    uid = request.session.get('id')  
    jobid = request.GET.get('id')  

    if not uid or not jobid:  
        return redirect('/login')  

    job = Jobs.objects.get(id=jobid)
    jobseeker = Student.objects.get(id=uid)

    if request.method == 'POST':
        resume = request.FILES.get('resume')  
        # expected_salary = request.POST.get('expected_salary')
        cover_letter = request.POST.get('cover_letter')


        # Create job application entry
        Apply_jobs.objects.create(
            jobId=job, 
            student=jobseeker, 
            resume=resume, 
            # expected_salary=expected_salary,
            cover_letter=cover_letter,
           
        )
        messages.info(request, "Job application submitted successfully.")

        return redirect('/studentApplied')  

    return render(request, 'studentapplyjob.html', {'job': job, 'jobseeker': jobseeker})

def studentApplied(request):
    uid = request.session.get('id')  
    jobseeker = Student.objects.get(id=uid)
    applications = Apply_jobs.objects.filter(student=jobseeker).order_by('-id')
    return render(request, 'studentApplied.html', {'applications': applications})




from datetime import date
def studentWorkshop(request):
    today= date.today()
    print(today,"######################")
    query = request.GET.get('search', '')  # Get the search term from the request
    if query:
        data = Workshop.objects.filter(title__icontains=query).order_by('-id')  # Filter jobs based on the title
    else:
        data = Workshop.objects.all().order_by('-id')  # Show all jobs if no search query
    return render(request, 'studentWorkshop.html', {'data': data,"today":today})


def studWorkDetails(request):
    job_id = request.GET.get('job_id')
    job = Workshop.objects.get(id=job_id)
    return render(request, 'studWorkDetails.html', {'job': job})


def studentWorkshopPay(request):
    uid = request.session.get('id')  
    jobid = request.GET.get('id')  

    if not uid or not jobid:  
        return redirect('/login')  

    job = Workshop.objects.get(id=jobid)
    jobseeker = Student.objects.get(id=uid)
    amount=job.fee

    if request.method == 'POST':


        # Create job application entry
        Apply_Workshops.objects.create(
            workshop=job, 
            student=jobseeker, 
           
        )
        messages.info(request, "Applied to Workshop successfully.")

        return redirect('/studentAppliedWork')  

    return render(request, 'studentWorkshopPay.html', {'job': job, 'jobseeker': jobseeker,"amount":amount})


def studentAppliedWork(request):
    uid = request.session.get('id')  
    jobseeker = Student.objects.get(id=uid)
    applications = Apply_Workshops.objects.filter(student=jobseeker).order_by('-id')
    return render(request, 'studentAppliedWork.html', {'applications': applications})