from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from pyrebase import pyrebase
from django.contrib import auth
from datetime import datetime
from django.template.context_processors import csrf
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import qrcode
from passlib.hash import pbkdf2_sha256
import cv2

config = {
    'apiKey': "AIzaSyBUZiiqwAD_eThaghVg5MYWIgkmCVXeWas",
    'authDomain': "jpmoney-123.firebaseapp.com",
    'databaseURL': "https://jpmoney-123.firebaseio.com/",
    'projectId': "jpmoney-123",
    'storageBucket': "jpmoney-123.appspot.com",
    'messagingSenderId': "455051452463"
    "serviceAccount": "firebase-adminsdk-qhafg@jpmoney-123.iam.gserviceaccount.com",
  }
firebase = pyrebase.initialize_app(config)
db=firebase.database()

authe = firebase.auth()

def newconductor(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		return render(request,'conductor_details.html',c)
	return HttpResponseRedirect('/login/')

def newbus(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		return render(request,'Bus.html',c) 
	return HttpResponseRedirect('/login/')

def login(request):
    c={}
    c.update(csrf(request))
    if request.session.has_key('username'):
        return HttpResponseRedirect('/home/')
    else:    
        return render(request,'index.html',c)

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect('/login/')

def home(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		info=db.child("ControllerDetails").child(request.session['username']).child('3_city').get().val()
		print(info)
		return render_to_response('home.html',{"id":request.session['username'] ,"city":info},c)
	else:
		return HttpResponseRedirect('/login/')

def addroute(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		return render(request,'addroutes.html',c)

def routeadded(request):
	c={}
	c.update(csrf(request))
	inc=0
	if request.session.has_key('username'):
		source=request.POST.get('src')
		routes=db.child("Route").shallow().get().val()
		for i in routes:
			inc=inc+1

		inc=inc+1	
		rid="R_"+str(inc)
		inc=int(inc)+1
		start=''
		end=''
		temp1=db.child("City").order_by_child("City_Name").equal_to(source).get().val()
		for p,q in temp1.items():
			start=str(p)
		dest=request.POST.get('dest')
		temp2=db.child("City").order_by_child("City_Name").equal_to(dest).get().val()
		for p,q in temp2.items():
			end=str(p)
		number=request.POST.get('station')
		station=[]
		add=''
		for i in range(1,int(number)+1):
			station.append(request.POST.get('station'+str(i)))
		for i in station:
			temp=db.child("City").order_by_child("City_Name").equal_to(i).get().val()
			for k,v in temp.items():
				k=str(k)+'#'
				add=str(add)+str(k)
		ans=str(start)+'#'+str(add)+str(end)
		ans1=str(start)+'#'+str(end)
		data={
				rid:{
					"Path":ans,
					"SortPath":ans1
				}

		}
		db.child("Route").update(data)
		print(ans)
		print(ans1)
	return HttpResponseRedirect('/home/')


def detect_face(request):
	c={}
	c.update(csrf(request))
	return render(request,"face_detect.html",c)


def face_detection(request):
	face_cascade = cv2.CascadeClassifier("C:\\Users\\dell\\Desktop\\abc.xml")
	myimage=request.POST.get('iname')
	if myimage is not None:
		img = cv2.imread(myimage)
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray_img, scaleFactor = 1.045, minNeighbors=5)
		print(type(faces))
		print(faces)
		print('Faces found: ', len(faces))
	
		for x, y, w, h in faces:
			img = cv2.rectangle(img,(x, y),(x + w, y + h),(0, 255, 0),2)
		resized = cv2.resize(img, (int(500),int(500)))
		cv2.imshow("Gray", resized)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return render(request,"face_detect.html",{"count":len(faces)})
	else:
		return HttpResponseRedirect('/detect_face/')


def error_404_view(request,exception):
	data={"name":"ThePythonDjango.com"}
	return render(request,'error.html',data)

@csrf_exempt
def searchbus(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		source=request.POST.get('source')
		destination=request.POST.get('destination')
		cities=db.child("City").shallow().get().val()
		#print(cities)
		start="1"
		end="5"
		try:
			if source is not None:
				route_with_bus=[]
				search_bus_ids=[]
				start=db.child("City").order_by_child("City_Name").equal_to(source).get().val()
				end=db.child("City").order_by_child("City_Name").equal_to(destination).get().val()
				print(start)
				print(end)
				for k,v in start.items():
					mystart=k
				for k,v in end.items():
					myend=k
				print(mystart)
				print(myend)
				myfinalroute=str(mystart)+'#'+str(myend)
				print(myfinalroute)
				routes=db.child("Route").order_by_child("SortPath").equal_to(myfinalroute).get().val()
				print(routes)
				if routes is not None:
					for i,j in routes.items():
						bus_ids=db.child("Bus_Route_time").order_by_child("Route_ID").equal_to(i).get().val()
						#print(bus_ids)
						for k,v in bus_ids.items():
							search_bus_ids.append(k)
							#print(search_bus_ids)
							for p,q in v.items():
								if p=="Departure_time":
									t1=(k,i,q)
									route_with_bus.append(tuple(t1))
									#print(route_with_bus)
					date=datetime.now()
					mydate = date.strftime("%Y-%m-%d")
					return render(request,"search.html",{"routes_with_bus":route_with_bus,"date":mydate,"search_bus_ids":search_bus_ids},c)	
		except Exception as e:
			return render(request,"search.html",{"msg":"bus does not exist"},c)
			
		return render(request,"search.html",{"msg":"bus does not exist"},c)
	else:
		return HttpResponseRedirect('/login/')


def authentication(request):
	c={}
	c.update(csrf(request))
	uname=request.POST.get('uname')
	pwd=request.POST.get('passwd')
	matching = db.child("ControllerDetails").child(uname).get().val()
	if matching is not None and pbkdf2_sha256.verify(pwd,str(db.child("ControllerDetails").child(uname).child("2_password").get().val())):
		request.session['username'] = uname
		return HttpResponseRedirect('/home/')
	else:
		return render(request,'index.html',{"message":"Invalid Username or Password!"},c)

def add_conductor(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		cid=request.POST.get('cid')
		cname=request.POST.get('cname')
		pwd=request.POST.get('passwd')
		email=request.POST.get('email')
		cpwd=request.POST.get('cpasswd')
		add=request.POST.get('address')
		cno=request.POST.get('cno')

		matching = db.child("conductor_details").child(cid).get().val()
		if matching is not None:
			return render(request,'conductor_details.html',{"message":"Already Exist!"},c)
		else:			
			if pwd == cpwd:
				p_hash=pbkdf2_sha256.encrypt(pwd,rounds=12000,salt_size=32)
				data={
					"C_ID":cid,
					"C_Conductor_Name":cname,
					"C_Contact":cno,
					"C_Password" : p_hash,
					"C_Email" : email,
					"C_Address" : add
				}
				try:
					user=authe.create_user_with_email_and_password(email,pwd)
					mydata={"name":cname,"status":"1"}
					db.child("Users").child(cid).child("details").set(mydata)
				except:
					return render(request,'conductor_details.html',{"message":"Unable to add please try again!"},c)
				result=db.child("ConductorDetails").child(cid).update(data)
				return HttpResponseRedirect('/home/')
			else:
				return render(request,'conductor_details.html',{"message":"Invalid details!"},c)
	return HttpResponseRedirect('/login/')

def add_bus(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		bid=request.POST.get('bid')
		bno=request.POST.get('bno')
		seats=request.POST.get('seats')
		matching = db.child("BusDetails").child(bid).get().val()
		if matching is not None:
			return render(request,'Bus.html',{"message":"Already Exist!"},c)
		else:			
			data={
					"Bus_ID":bid,
					"Bus_No":bno,
					"Total_Seats" : seats
				}
			result=db.child("BusDetails").child(bid).update(data)
			info={"busid":bid}
			img = qrcode.make(info)
			img.save(bid+'.jpg')
			return HttpResponseRedirect('/home/')
	return HttpResponseRedirect('/login/')

def fare(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		myfare=[]
		bid=request.GET.get('busid')
		date_today=request.GET.get('Date')
		matching = db.child("Ticket_Log").child(bid).shallow().get().val()
		print("matching"+str (matching))	
		#cid=db.child("bus_conductor").child(bid).child("2_conductor_ID").get().val()
		lat=db.child("Location").child(bid).child("latitude").get().val()
		lon=db.child("Location").child(bid).child("longitude").get().val()
		print(lat)
		#date=request.GET.get('Date')
		total=0
		#cname=db.child("conductor_details").child(cid).child("3_conductor_name").get().val()
		new_list=[]
		#print(lat)
		if matching is not None:
			for i in matching:
				ticket_status=db.child("Fare_Collected_Status").shallow().get().val()
				print(ticket_status)
				for k in ticket_status:
					if str(db.child("Fare_Collected_Status").child(k).child("C_ID").get().val())==i and str(db.child("Fare_Collected_Status").child(k).child("Bus_ID").get().val())==bid and str(db.child("Fare_Collected_Status").child(k).child("Date").get().val())==date_today:
						if (str(db.child("Fare_Collected_Status").child(k).child("Is_Collected").get().val())=="0"):
							myfare=[]
							total=0
							all_tickets=db.child("Ticket_Log").child(bid).child(i).shallow().get().val()
							print("all_tickets"+str(all_tickets))
							for j in all_tickets:
								if str(db.child("Ticket_Log").child(bid).child(i).child(j).child("d_Date").get().val())==date_today:
									tickets=db.child("Ticket_Log").child(bid).child(i).child(j).get().val()
									print("tickets"+str(tickets))
									myfare.append(tickets)
									print("myfare"+ str(myfare))
									total+=int(db.child("Ticket_Log").child(bid).child(i).child(j).child("f_Fare").get().val())
									print("total"+str(total))
									#t1=(i,myfare,total)
									
							t1=(i,myfare,total)
							new_list.append(tuple(t1))
							print(new_list)
			return render(request,'fare.html',{'data':new_list,'lat':lat,'longi':lon})
		return render(request,'fare.html',{"message":"No available Data!"},c)
	return HttpResponseRedirect('/login/')



def UpdateFareStatus(request):
	c={}
	c.update(csrf(request))
	if request.session.has_key('username'):
		b_id=request.POST.get("busid")
		date=request.POST.get("Date")
		c_id=request.POST.get("conducter_id")
		status=db.child("Fare_Collected_Status").shallow().get().val()
		for i in status:
			if str(db.child("Fare_Collected_Status").child(i).child("C_ID").get().val())==c_id and str(db.child("Fare_Collected_Status").child(i).child("Bus_ID").get().val())==b_id and str(db.child("Fare_Collected_Status").child(i).child("Date").get().val())==date:
				data={
						"Bus_ID":b_id,
						"C_ID":c_id,
						"Date" : date,
						"Is_Collected":"1"
					}
				db.child("Fare_Collected_Status").child(i).update(data)
		return HttpResponseRedirect('/fare/?busid='+b_id+'&Date='+date)
	return HttpResponseRedirect('/login')