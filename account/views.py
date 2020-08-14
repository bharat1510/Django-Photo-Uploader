from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . import models
import psycopg2
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import upload

connection = psycopg2.connect(user="postgres",password="1510",host="localhost",port="5432",database="task_user")
cursor = connection.cursor()

# Create your views here.
def index(request):
	val = upload.objects.all().filter(email='b@gmail.com')
	return render(request, 'index.html',{'val':val})

def signup(request):
	if request.method == 'GET':
		return render(request,'signup.html')
	else:
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['pass']
		password1 = request.POST['pass1']
		if password==password1:
			if User.objects.filter(username=username).exists():
				messages.info(request,"Username is taken")
				return redirect('signup')
			elif User.objects.filter(email=email).exists():
				messages.error(request,"Email id is already registered")
				return redirect('signup')
			else:
				user = User.objects.create_user(password=password,username=username,email=email)
				user.save()
				return redirect('login')
		else:
			messages.warning(request,"Password not match")
			return redirect('signup')
		return redirect('/')
				
	#return render(request, 'signup.html')

def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	else:
		username = request.POST['username']
		password = request.POST['pass']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.warning(request,"Check your Username or Password.")
			return redirect('login')
			
	#return render(request, 'login.html')
	
def logout(request):
	auth.logout(request)
	return redirect('/')
	
def iupload(request):
	if request.method == 'POST' and request.FILES['image']:
		myfile = request.FILES['image']
		username = request.POST['user']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		print("URL:",uploaded_file_url)
		img_name = myfile.name
		
		postgres_insert_query = """ INSERT INTO account_upload (email,image) VALUES (%s,%s)"""
		record_to_insert = (username,img_name)
		cursor.execute(postgres_insert_query, record_to_insert)
		connection.commit()
		
		return redirect('/')
	return render(request, 'index.html')