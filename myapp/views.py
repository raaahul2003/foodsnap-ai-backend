from datetime import datetime
from os import login_tty
from tkinter import Image
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import smtplib


from myapp.models import *

# Create your views here.

def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    print(username)
    print(password)
    check =authenticate(request,username=username,password=password)
    if check is not None:
        
        if check.groups.filter(name='admin').exists():
            login(request,check)
            messages.success(request,'login successful')
            return redirect('/myapp/admin_home/')
        else:
            messages.warning(request,'Invalid user')
            return redirect('/myapp/login_get/')

    else:
        messages.error(request,'Invalid credantials')
        return redirect('/myapp/login_get/')
    
def forget_password(request):
    return render(request,'forgetpassword.html')
# -------------------- a d m i n -------------------
def admin_home(request):
    from django.utils import timezone
    today = timezone.now().date()
    total_users      = Users.objects.count()
    # active_today     = Users.objects.filter(date_joined__date=today).count()
    total_food       = Food_Database.objects.count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='Pending').count() if hasattr(Complaint, 'status') else Complaint.objects.count()
    total_feedback   = Feedback.objects.count()

    # recent_users      = Users.objects.order_by('-date_joined')[:5]
    recent_food       = Food_Database.objects.order_by('-id')[:5]
    recent_complaints = Complaint.objects.order_by('-id')[:5]
    return render(request,'index.html', {
        'total_users':        total_users,
        # 'active_today':       active_today,
        'total_food':         total_food,
        'total_complaints':   total_complaints,
        'pending_complaints': pending_complaints,
        'total_feedback':     total_feedback,
        # 'recent_users':       recent_users,
        'recent_food':        recent_food,
        'recent_complaints':  recent_complaints,
    })

def admin_change_password(request):
    return render(request,'changepassword.html')

def admin_change_password_post(request):
    CurrentPassword = request.POST['Current Password']
    NewPassword = request.POST['New Password']
    ConfirmPassword = request.POST['Confirm Password']
    lid=request.user

    if lid.check_password(CurrentPassword):
        if NewPassword==ConfirmPassword:
            lid.set_password(ConfirmPassword)
            lid.save()
            messages.success(request,'Password Updated Successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.warning(request,'New Password and Confirm Password is Not Matching')
            return redirect('/myapp/admin_change_password/')
    else:
        messages.warning(request,'Invalid Password')
        return redirect('/myapp/admin_change_password/')

def admin_view_user(request):
    data=Users.objects.all()
    return render(request,'viewuser.html',{'data':data})

def admin_add_food(request):
    return render(request,'add_food.html')

def admin_add_food_post(request):
    FoodName = request.POST['Food Name']
    Photo = request.FILES['photo']
    Description = request.POST['Description']

    fs=FileSystemStorage()
    from datetime import datetime
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,Photo)
    path=fs.url(date)

    data=Food_Database()
    data.Food_Name=FoodName
    data.Photo=path
    data.description=Description
    data.save()
    messages.success(request,'Food Added Successfully')
    return redirect('/myapp/admin_view_food_database/')

def admin_view_food_database(request):
    data=Food_Database.objects.all()
    return render(request,'viewfooddatabase.html',{'data':data})

def admin_delete_food_database(request,id):
    Food_Database.objects.get(id=id).delete()
    messages.success(request,'Deleted Successfully')
    return redirect('/myapp/admin_view_food_database/')

def admin_edit_food(request,id):
    data=Food_Database.objects.get(id=id)
    return render(request,'edit_food.html',{'data':data})

def admin_edit_food_post(request):
    FoodName = request.POST['Food Name']
    Description = request.POST['Description']
    id=request.POST['id']

    data=Food_Database.objects.get(id=id)

    if 'photo' in request.FILES:
        Photo = request.FILES['photo']
        fs=FileSystemStorage()
        date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
        fs.save(date,Photo)
        path=fs.url(date)
        data.Photo=path
        data.save()


    data.Food_Name=FoodName
    data.description=Description
    data.save()
    messages.success(request,'Food Edited Successfully')
    return redirect('/myapp/admin_view_food_database/')

def admin_view_complaint(request):
    data=Complaint.objects.all()
    return render(request,'viewcomplaint.html',{'data':data})

def admin_send_reply(request):
    return render(request,'sendreply.html')


def admin_send_reply_post(request):
    Reply = request.POST['Reply']
    return

def admin_view_feedback(request):
    data=Feedback.objects.all()
    return render(request,'viewfeedback.html',{'data':data})


# ---------------------- u s e r --------------------

def app_login(request):
    username=request.POST['Username']
    password=request.POST['Password']
    print(username)
    print(password)
    check =authenticate(request,username=username,password=password)
    print(check)
    if check is not None:
        if check.groups.filter(name='users').exists():
            # login(request,check)
            # messages.success(request,'login successful')
            h="no"
            if Health_Profile.objects.filter(USERS__AUTH_USER=check.id).exists():
                h="yes"
            print(h)
            return JsonResponse({"status":"ok",'lid':str(check.id),"h":h})
        else:
            # messages.warning(request,'Invalid user')
            return JsonResponse({"status":"no"})
    else:
        # messages.error(request,'Invalid credantials')
        return JsonResponse({"status":"no"})
    

def user_signup(request):
    uname=request.POST['uname']
    uemail=request.POST['uemail']
    ugender=request.POST['ugender']
    udob=request.POST['udob']
    uphoto=request.FILES['photo']
    uphone=request.POST['uphone']
    uplace=request.POST['uplace']
    upost=request.POST['upost']
    udistrict=request.POST['udistrict']
    ustate=request.POST['ustate']
    upin=request.POST['upin']
    upassword=request.POST['upassword']
    # uname=request.POST['uconfirmpassword']

    print(uemail)
    print(upassword)
    from datetime import datetime

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,uphoto)
    path=fs.url(date)

    if User.objects.filter(username=uemail).exists():
        return JsonResponse({"status":"ex"})


    user=User.objects.create_user(username=uemail,password=upassword)
    user.groups.add(Group.objects.get(name='users'))
    user.save()

    data=Users()
    data.Name = uname
    data.Dob = udob
    data.Email = uemail
    data.Gender = ugender
    data.Phone = uphone
    data.Photo = path
    data.Place = uplace
    data.Post = upost
    data.District = udistrict
    data.State = ustate
    data.Pin = upin
    data.AUTH_USER = user
    data.save()
    return JsonResponse({"status":"ok"})


def user_change_password_post(request):
    CurrentPassword = request.POST['current']
    NewPassword = request.POST['newpass']
    ConfirmPassword = request.POST['confirm']
    lid=request.POST['lid']
    user=User.objects.get(id=lid)

    if user.check_password(CurrentPassword):
        if NewPassword==ConfirmPassword:
            user.set_password(ConfirmPassword)
            user.save()
            # messages.success(request,'Password Updated Successfully')
            return JsonResponse({"status":"ok"})
        else:
            # messages.warning(request,'New Password and Confirm Password is Not Matching')
            return JsonResponse({"status":"ok"})
    else:
        # messages.warning(request,'Invalid Password')
        return JsonResponse({"status":"ok"})
    
# def user_add_health_profile_post(request):
#     height = request.POST['height']
#     weight = request.POST['weight']
#     bmi = request.POST['bmi']
#     bloodg = request.POST['bloodg']
#     cardiac = request.POST['cardiac']
#     bodytype = request.POST['bodytype']
#     bp = request.POST['bp']
#     cholestrol = request.POST['cholestrol']
#     sugarlevel = request.POST['sugarlevel']
#     thyroid = request.POST['thyroid']
#     waist = request.POST['waist']
#     hip = request.POST['hip']
#     vitamin = request.POST['vitamin']
#     iron = request.POST['iron']
#     smoking = request.POST['smoking']
#     alcohol = request.POST['alcohol']
#     physical = request.POST['physical']
#     bodydensity = request.POST['bodydensity']

#     lid=request.POST['lid']

#     if Health_Profile.objects.filter(USERS__AUTH_USER=lid).exists():
#         return JsonResponse({"status":"ok"})
#     else:
#         data = Health_Profile()
#         data.Height = height
#         data.Weight = weight
#         data.Bmi = bmi
#         data.Blood_Group = bloodg   
#         data.Is_Cardiac = cardiac
#         data.Body_Type = bodytype
#         data.Bp =  bp
#         data.Cholestrol = cholestrol
#         data.Sugar_level = sugarlevel
#         data.Thyroid_Status = thyroid
#         data.Waist_Circumference = waist
#         data.Hip_Circumference = hip   
#         data.Bone_Density_Tscore = bodydensity
#         data.Vitamin_D_Level = vitamin
#         data.Iron_Ferritin =  iron
#         data.Smoking =  smoking
#         data.Alcohol_Consumption = alcohol
#         data.Physical_Activity_Level = physical
#         data.USERS = Users.objects.get(AUTH_USER=lid)
#         data.save()

#         return JsonResponse({"status":"ok"})

from datetime import date

def user_add_health_profile_post(request):

    height = float(request.POST['height'])
    weight = float(request.POST['weight'])
    physical = request.POST['physical']
    bloodg = request.POST['bloodg']
    cardiac = request.POST['cardiac']
    bodytype = request.POST['bodytype']
    bp = request.POST['bp']
    cholestrol = request.POST['cholestrol']
    sugarlevel = request.POST['sugarlevel']
    thyroid = request.POST['thyroid']
    waist = request.POST['waist']
    hip = request.POST['hip']
    vitamin = request.POST['vitamin']
    iron = request.POST['iron']
    smoking = request.POST['smoking']
    alcohol = request.POST['alcohol']
    bodydensity = request.POST['bodydensity']
    lid = request.POST['lid']

    user = Users.objects.get(AUTH_USER=lid)

    today = date.today()
    age = today.year - user.Dob.year

    if user.Gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    activity_multiplier = {
        "low": 1.2,
        "moderate": 1.55,
        "high": 1.9
    }

    multiplier = activity_multiplier.get(physical.lower(), 1.2)

    daily_calories = round(bmr * multiplier)

 

    protein_grams = round(weight * 1.6)

    fat_calories = daily_calories * 0.25
    fat_grams = round(fat_calories / 9)

    remaining_calories = daily_calories - ((protein_grams * 4) + (fat_grams * 9))
    carb_grams = round(remaining_calories / 4)

    if Health_Profile.objects.filter(USERS__AUTH_USER=lid).exists():
        return JsonResponse({
            "status": "ok",
            "calories": daily_calories,
            "protein": protein_grams,
            "fat": fat_grams,
            "carbs": carb_grams
        })

    else:
        data = Health_Profile()
        data.Height = height
        data.Weight = weight
        data.Bmi = request.POST['bmi']
        data.Blood_Group = bloodg
        data.Is_Cardiac = cardiac
        data.Body_Type = bodytype
        data.Bp = bp
        data.Cholestrol = cholestrol
        data.Sugar_level = sugarlevel
        data.Thyroid_Status = thyroid
        data.Waist_Circumference = waist
        data.Hip_Circumference = hip
        data.Bone_Density_Tscore = bodydensity
        data.Vitamin_D_Level = vitamin
        data.Iron_Ferritin = iron
        data.Smoking = smoking
        data.Alcohol_Consumption = alcohol
        data.Physical_Activity_Level = physical

        data.healthprofile = str(daily_calories)
        data.protienvalue = str(protein_grams)
        data.fatvalue = str(fat_grams)
        data.carbvalue = str(carb_grams)

        data.USERS = user
        data.save()

        return JsonResponse({
            "status": "ok",
            "calories": daily_calories,
            "protein": protein_grams,
            "fat": fat_grams,
            "carbs": carb_grams
        })

def user_add_daily_food_log_post(request):
    date = request.POST[' date']
    time = request.POST['time']
    type = request.POST['type']
    food = request.POST['food']
    lid=request.POST['lid']

    data = Daily_Food()
    data.Date = date
    data.Food_Time = time
    data.Type = type
    data.FOOD_DATABASE = food
    data.USERS= Users.objects.get(AUTH_USER=lid)
    data.save()
    
    return JsonResponse({"status":"ok"})

def view_profile(request):
    lid=request.POST['lid']
    data=Users.objects.get(AUTH_USER=lid)
    return JsonResponse({
        "status":"ok",
        "Name":data.Name,
        "Dob":data.Dob,
        "Email":data.Email,
        "Gender":data.Gender,
        "Phone":data.Phone,
        "Photo":data.Photo,
        "Place":data.Place,
        "Post":data.Post,
        "District":data.District,
        "State":data.State,
        "Pin":data.Pin,
        })


def edit_profile(request):
    uname=request.POST['uname']
    uemail=request.POST['uemail']
    ugender=request.POST['ugender']
    udob=request.POST['udob']
    uphone=request.POST['uphone']
    uplace=request.POST['uplace']
    upost=request.POST['upost']
    udistrict=request.POST['udistrict']
    ustate=request.POST['ustate']
    upin=request.POST['upin']
    id=request.POST['id']
    print(id,'abc')
    data=Users.objects.get(AUTH_USER=id)
   

    if 'photo' in request.FILES:
        uphoto=request.FILES['photo']
        fs=FileSystemStorage()
        from datetime import datetime
        date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
        fs.save(date,uphoto)
        path=fs.url(date)
        data.Photo = path
        data.save()
    data.Name = uname
    data.Dob = udob
    data.Email = uemail
    data.Gender = ugender
    data.Phone = uphone
    data.Place = uplace
    data.Post = upost
    data.District = udistrict
    data.State = ustate
    data.Pin = upin
    data.save()

    return JsonResponse({"status":"ok"})

# user=User.objects.get(username='admin@gmail.com')
# user.set_password('123456')
# user.save()
def send_feedback(request):
    feedback = request.POST['feedback']
    lid=request.POST['lid']
    from datetime import datetime
    a=Feedback()
    a.Date=datetime.now().today()
    a.Feedback=feedback
    a.USERS=Users.objects.get(AUTH_USER=lid)
    a.save()
    return JsonResponse({"status":"ok"})

def view_health_profile(request):
    lid=request.POST['lid']
    i=Health_Profile.objects.get(USERS__AUTH_USER=lid)
    
    return JsonResponse({
        'status':'ok',
            'id':i.id,
            'Height':i.Height,
            'Weight':i.Weight,
            'Bmi':i.Bmi,
            'Blood_Group':i.Blood_Group,
            'Is_Cardiac':i.Is_Cardiac,
            'Body_Type':i.Body_Type,
            'Bp':i.Bp,
            'Cholestrol':i.Cholestrol,
            'Sugar_level':i.Sugar_level,
            'Thyroid_Status':i.Thyroid_Status,
            'Waist_Circumference':i.Waist_Circumference,
            'Hip_Circumference':i.Hip_Circumference,
            'Bone_Density_Tscore':i.Bone_Density_Tscore,
            'Vitamin_D_Level':i.Vitamin_D_Level,
            'Iron_Ferritin':i.Iron_Ferritin,
            'Smoking':i.Smoking,
            'Alcohol_Consumption':i.Alcohol_Consumption,
            'Physical_Activity_Level':i.Physical_Activity_Level,
        
        }) 
def edit_health_profile(request):

    height = request.POST['height']
    weight = request.POST['weight']
    bmi = request.POST['bmi']
    bloodg = request.POST['bloodg']
    cardiac = request.POST['cardiac']
    bodytype = request.POST['bodytype']
    bp = request.POST['bp']
    cholestrol = request.POST['cholestrol']
    sugarlevel = request.POST['sugarlevel']
    thyroid = request.POST['thyroid']
    waist = request.POST['waist']
    hip = request.POST['hip']
    vitamin = request.POST['vitamin']
    iron = request.POST['iron']
    smoking = request.POST['smoking']
    alcohol = request.POST['alcohol']
    physical = request.POST['physical']
    bodydensity = request.POST['bodydensity']

    id=request.POST['lid']

    data = Health_Profile.objects.get(USERS__AUTH_USER=id)
    data.Height = height
    data.Weight = weight
    data.Bmi = bmi
    data.Blood_Group = bloodg   
    data.Is_Cardiac = cardiac
    data.Body_Type = bodytype
    data.Bp =  bp
    data.Cholestrol = cholestrol
    data.Sugar_level = sugarlevel
    data.Thyroid_Status = thyroid
    data.Waist_Circumference = waist
    data.Hip_Circumference = hip   
    data.Bone_Density_Tscore = bodydensity
    data.Vitamin_D_Level = vitamin
    data.Iron_Ferritin =  iron
    data.Smoking =  smoking
    data.Alcohol_Consumption = alcohol
    data.Physical_Activity_Level = physical
    data.save()

    return JsonResponse({"status":"ok"})



# import os
# import datetime
# import requests
# import cv2

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import FileSystemStorage

# from ultralytics import YOLO


# # 🔥 Load YOLO model ONCE (important for performance)
# # /Users/rahulrajcp/Riss/web_project/myapp/foodalgo/runs/detect/health_diet_detector4/weights
# MODEL_PATH = YOLO(r'/Users/rahulrajcp/Riss/web_project/myapp/foodalgo/runs/detect/health_diet_detector4/weights/best.pt')  # Use 'yolov8s.pt', 'yolov8m.pt', etc., for larger models

# model = YOLO(MODEL_PATH)


# @csrf_exempt
# def upload_food(request):
#     if request.method != "POST":
#         return JsonResponse({"status": "error", "message": "Invalid request"})

#     if 'photo' not in request.FILES:
#         print('vcvb')
#         return JsonResponse({"status": "error", "message": "No image uploaded"})

#     try:
#         # Save image
#         file = request.FILES['photo']
#         print(file)
#         fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
#         fs = FileSystemStorage()
#         filename = fs.save(fname, file)
#         image_path = fs.path(filename)

#         # Read image
#         image = cv2.imread(image_path)

#         # Run YOLO prediction
#         results = model(image)

#         foodname = ""

#         for result in results:
#             if result.boxes is not None:
#                 for box in result.boxes:
#                     class_id = int(box.cls[0])
#                     confidence = float(box.conf[0])
#                     class_name = model.names[class_id]

#                     if confidence > 0.5:   # Confidence threshold
#                         foodname = class_name
#                         break

#         if foodname == "":
#             return JsonResponse({"status": "no", "message": "No food detected"})

#         # 🔥 USDA API
#         api_key = "wHgCIYjR9w2Y0hoeu2eGplf4n8WM1XWSC3jQdhcv"
#         url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={foodname}&api_key={api_key}"

#         response = requests.get(url)
#         data = response.json()

#         if "foods" not in data or len(data["foods"]) == 0:
#             return JsonResponse({"status": "no", "message": "No nutrition data found"})

#         nutrients_raw = data["foods"][0]["foodNutrients"]

#         nutrients = []

#         for item in nutrients_raw:
#             if item.get("value") is not None:
#                 nutrients.append({
#                     "nutrientName": item.get("nutrientName"),
#                     "value": item.get("value"),
#                     "unitName": item.get("unitName"),
#                 })

#         return JsonResponse({
#             "status": "ok",
#             "foodname": foodname,
#             "nutrients": nutrients
#         })

#     except Exception as e:
#         return JsonResponse({
#             "status": "error",
#             "message": str(e)
#         })


import datetime
import requests
import cv2

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

from ultralytics import YOLO

from .models import Users, Food_Database, Daily_Food


# ✅ Load YOLO model ONCE
MODEL_PATH = r'/Users/rahulrajcp/Riss/web_project/myapp/foodalgo/runs/detect/health_diet_detector4/weights/best.pt'
yolo_model = YOLO(MODEL_PATH)


@csrf_exempt
def upload_food(request):
    print('hello')
    time=datetime.datetime.now().time()

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    if 'photo' not in request.FILES:
        print('no')
        return JsonResponse({"status": "error", "message": "No image uploaded"})
    print('he')
    # try:
        # ✅ Get user id from Flutter
    lid = request.POST.get("lid")
    user_obj = Users.objects.get(AUTH_USER__id=lid)
    print(lid)

    # ✅ Save image
    file = request.FILES['photo']
    fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    fs = FileSystemStorage()
    filename = fs.save(fname, file)
    image_path = fs.path(filename)
    print(image_path)

    # ✅ Run YOLO
    image = cv2.imread(image_path)
    print(image,'vh')
    results = yolo_model(image)

    for r in results:
        print("Boxes:", r.boxes)
        if r.boxes:
            for box in r.boxes:
                print("Class ID:", box.cls)
                print("Confidence:", box.conf)

    foodname = ""

    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = yolo_model.names[class_id]

                if confidence > 0.5:
                    foodname = class_name
                    break

    if foodname == "":
        return JsonResponse({"status": "no", "message": "No food detected"})
    

    kkk=""

    # foodname=f
    ###geneative AI
    genai.configure(api_key='AIzaSyAP6nNbu82Flt2RFY-awuNBakDGQv3icUs')
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            """
You are a nutrition expert.

        Given the food name: """ +foodname +"""

        Return:
        1. List of main ingredients
        2. Approximate nutrition values per 100g:
           - Calories (kcal)
           - Protein (g)
           - Carbohydrates (g)
           - Fat (g)
           - Sugar (g)
           - Fiber (g)

        Return ONLY valid JSON in this format:

        {{
            "food_name": "",
            "ingredients": [],
            "nutrition_per_100g": {{
                "calories": "",
                "protein": "",
                "carbohydrates": "",
                "fat": "",
                "sugar": "",
                "fiber": ""
            }}
        }}
""",
            stream=False
        )

        if not response.text:
            return None

        print(response.text.replace("*", "").strip())

        m=response.text.replace("*", "").strip()
        m=m.replace("`","")
        m=m.replace("json","")

        print("lik",m)


        import json
        kkk=json.loads(m)
        print("=====1233423141234324124332432")

    except Exception as e:
        print("Gemini Error:", e)
        


    print(type(kkk),"lllll")



    ####END GENAI






    # API_KEY = "oq/B1/i8Y6LF6s5ZrG1QAw==Q2iZWUqO2Zqe2rCG"

    # print(foodname)
    # # h='biriyani'

    # api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    # response = requests.get(api_url + foodname, headers={'X-Api-Key': API_KEY})

    # print(response.url)
    # print(response.content,"llllllllllllll")


    # csecret="9088a418c3724e8d87dc88aa70419f3c"
    # cappid="626de7c6ca9641e888437fbdeb509171"

    # # ✅ USDA API
    # # api_key = "wHgCIYjR9w2Y0hoeu2eGplf4n8WM1XWSC3jQdhcv"
    # # url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={foodname}&api_key={api_key}"

    # # response = requests.get(url)
    # data = response.json()
    # print(data)

    # if "foods" not in data or len(data["foods"]) == 0:
    #     print('------')
    #     return JsonResponse({"status": "no", "message": "No nutrition found"})

    # nutrients_raw = data["foods"][0]["foodNutrients"]

    protein = "0"
    carbs = "0"
    fat = "0"

    nutrients = []

    # print(kkk["nutrition_per_100g"],"------------------",type(kkk["nutrition_per_100g"]))

    for item,value in kkk["nutrition_per_100g"].items():

        print(item,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",value)
        name = item
        # value = value
        unit = 'gm'

        print(name,value,"==========AM LIKHIL")

        if value is not None:
            nutrients.append({
                "nutrientName": name,
                "value": value,
                "unitName": unit,
            })

            if name == "protein":
                protein = str(value)

            if name == "carbohydrates":
                carbs = str(value)

            if name == "fat":
                fat = str(value)

    # ✅ Save food to Food_Database (if not exists)
    food_obj, created = Food_Database.objects.get_or_create(
        Food_Name=foodname,
        defaults={
            "Photo": filename,
            "description": foodname
        }
    )

    # ✅ Save to Daily_Food table
    

    Daily_Food.objects.create(
        USERS=user_obj,
        FOOD_DATABASE=food_obj,
        Food_Time=time,
        Protein=protein,
        Carbohydrate=carbs,
        Fat=fat,
        Date=datetime.date.today(),
        Type="Detected"
    )

    print(fat,"lllllllllllllllllllllllllllllllllll")

    return JsonResponse({
        "status": "ok",
        "foodname": foodname,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "nutrients": nutrients
    })

    # except Exception as e:
    #     return JsonResponse({
    #         "status": "error",
    #         "message": str(e)
    #     })

from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime

from .models import Daily_Food, Users


@csrf_exempt
def today_nutrition_summary(request):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    try:
        lid = request.POST.get("lid")

        if not lid:
            return JsonResponse({"status": "error", "message": "User id missing"})

        user_obj = Users.objects.get(AUTH_USER__id=lid)

        today = datetime.date.today()

        foods = Daily_Food.objects.filter(
            USERS=user_obj,
            Date=today
        )

        total_protein = 0
        total_carbs = 0
        total_fat = 0

        for food in foods:
            try:
                total_protein += float(food.Protein)
                total_carbs += float(food.Carbohydrate)
                total_fat += float(food.Fat)
            except:
                pass

        total_calories = (
            (total_protein * 4) +
            (total_carbs * 4) +
            (total_fat * 9)
        )

        return JsonResponse({
            "status": "ok",
            "date": str(today),
            "total_protein": round(total_protein, 2),
            "total_carbs": round(total_carbs, 2),
            "total_fat": round(total_fat, 2),
            "total_calories": round(total_calories, 2),
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
    
# a=User.objects.get(username='admin')
# a.set_password('admin123')
# a.save()


def userviewhishealth(request):
    id=request.POST['lid']
    a=Health_Profile.objects.get(USERS__AUTH_USER_id=id)
    print(a)
    return JsonResponse({
        'status':'ok',
        'healthvalue':a.healthprofile,
        'protienvalue':a.protienvalue,
        'carbvalue':a.carbvalue,
        'fatvalue':a.fatvalue,

    })



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCv2JD3HnV34JJdX47s0lKATVgXl_UZdQ4")
model = genai.GenerativeModel("gemini-2.5-flash")

@csrf_exempt
def analyze_ingredients(request):
    try:
        ingredients = request.POST.get("ingredients", "")
        print(ingredients)

        if not ingredients:
            return JsonResponse({"status": "error", "message": "No ingredients provided"})

        prompt = f"""
        You are a certified nutrition expert.

        Analyze these food ingredients and respond strictly in this format:

        Status: SAFE or HARMFUL
        Risk Level: LOW / MODERATE / HIGH
        Reason: Maximum 3 short lines

        Ingredients:
        {ingredients}
        """

        response = model.generate_content(prompt)
        print(response)
        result = response.text
        print(result)

        return JsonResponse({
            "status": "ok",
            "analysis": result
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
    
@csrf_exempt
def get_food_suggestions(request):
    try:
        lid = request.POST.get("lid")
        print(lid)

        if not lid:
            return JsonResponse({
                "status": "error",
                "message": "User id missing"
            })

        health = Health_Profile.objects.get(USERS__AUTH_USER_id=lid)

        prompt = f"""
You are a certified clinical nutritionist.

Based on the following health profile, suggest a one-day food plan.

Health Profile:
- BMI: {health.Bmi}
- Cardiac: {health.Is_Cardiac}
- BP: {health.Bp}
- Cholesterol: {health.Cholestrol}
- Sugar Level: {health.Sugar_level}
- Thyroid: {health.Thyroid_Status}
- Physical Activity Level: {health.Physical_Activity_Level}
- Body Type: {health.Body_Type}
- Protein Target: {health.protienvalue}
- Carb Target: {health.carbvalue}
- Fat Target: {health.fatvalue}
- Smoking: {health.Smoking}
- Alcohol Consumption: {health.Alcohol_Consumption}

Respond STRICTLY in this format:

Overall Health Advice:
(max 3 short lines)

Breakfast Suggestion:
(food name + short reason)

Lunch Suggestion:
(food name + short reason)

Dinner Suggestion:
(food name + short reason)

Snacks Suggestion:
(food name + short reason)
"""

        response = model.generate_content(prompt)
        result = response.text

        return JsonResponse({
            "status": "ok",
            "suggestion": result
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
    
def and_forget_password_post(request):
    if request.method == 'POST':
        email = request.POST['email']

        user = User.objects.get(username=email)
        print(user)
        if user is None:
            return JsonResponse({"status": "error", "message": "Email does not exist"})
        
        import random
        psw = random.randint(1000, 9999)
        print(psw)

        user.set_password(str(psw))
        user.save()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("eatwise26@gmail.com", "qawg gpgb yfkc aagg")  # App Password

        subject = "Password Reset - EatWise Ai App"
        body = "Your new password is: " + str(psw)
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail("trainingstarted@gmail.com", email, msg)
        server.quit()

        return JsonResponse({"status": "ok", "message": "New password sent to your email"})


    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})



def food_predictions(request):


    file=request.FILES['photo']
    from datetime import datetime

    fname=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"

    fs=FileSystemStorage()
    fs.save(fname,file)


    f = "/Users/rahulrajcp/Riss/web_project/media/" + fname    
    
    import google.generativeai as genai
    from PIL import Image

    genai.configure(api_key="AIzaSyDQ1cNs4Uadhzqv_LLPmx_ENXBOOXq3ilQ")  # Replace with your actual key

    # f=r"C:\Riss\opra\web\opra\media\20260102000746.jpg"
    #######################################

    import google.generativeai as genai
    import json

    def analyze_food_image(image):
        try:
            model = genai.GenerativeModel("gemini-flash-latest")

            # prompt = """
            # Analyze this food image and respond ONLY in valid JSON.

            # Required JSON format:

            # {
            #     "food_name": "",
            #     "estimated_quantity": {
            #         "value": "",
            #         "unit": ""
            #     },
            #     "calories_kcal": "",
            #     "macronutrients": {
            #         "protein_g": "",
            #         "carbohydrates_g": "",
            #         "fat_g": ""
            #     },
            #     "other_nutrients": [],
            #     "health_benefits": ""
            # }

            # Do NOT add explanation.
            # Do NOT add markdown.
            # Do NOT add extra text.
            # Return ONLY valid JSON.
            # """

            prompt = """
Analyze this food image carefully and respond ONLY in valid JSON.

Required JSON format:

{
    "food_name": "",
    "estimated_quantity": {
        "value": "",
        "unit": ""
    },
    "serving_estimation": {
        "approx_servings": "",
        "suitable_for": "",
        "portion_size_per_person": ""
    },
    "calories_kcal": "",
    "macronutrients": {
        "protein_g": "",
        "carbohydrates_g": "",
        "fat_g": "",
        "sugar_g": "",
        "fiber_g": "",

    },
    "other_nutrients": [],
    "health_benefits": ""
}

Instructions:
- Carefully observe the size of the food relative to the plate, bowl, or container.
- Estimate quantity based on visible portion size (small, medium, large).
- If the food fills most of a standard dinner plate, estimate higher grams (400g–800g).
- If the portion is small or occupies only part of the plate, estimate lower grams (100g–250g).
- DO NOT assume a fixed 100g serving.
- Scale calories and macronutrients according to the estimated visible quantity.
- Estimate how many people this portion can serve.
- If exact weight is unclear, make a realistic visual approximation.
- Do NOT add explanation.
- Do NOT add markdown.
- Do NOT add extra text.
- Return ONLY valid JSON.
"""

            response = model.generate_content(
                [prompt, image],
                stream=False
            )

            # Clean response (important if model adds formatting)
            cleaned_text = response.text.strip()

            # Convert to Python dictionary
            data = json.loads(cleaned_text)

            return data
        except Exception as e:
            return {"error": f"Gemini API Error: {str(e)}"}
        
    def load_image(image_path):
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            print("Error loading image:",e)
            return None

    image_path = f  # Change this if needed
    image = load_image(image_path)

    result = analyze_food_image(image)
    # print(result,"================================================================")


    print("Food Name:", result.get("food_name", "N/A"))
    print("Estimated Quantity:", result.get("estimated_quantity", "N/A"))
    estimated_quantity = result.get("estimated_quantity", {})

    print("Estimated value:", estimated_quantity.get("value", "N/A"))
    print("Estimated unit:", estimated_quantity.get("unit", "N/A"))

    print("Calories (kcal):", result.get("calories_kcal", "N/A"))
    print("Macronutrients:", result.get("macronutrients", "N/A"))
    print("Other Nutrients:", result.get("other_nutrients", "N/A"))


    food_name = result.get("food_name", "Unknown")

    estimated_quantity = result.get("estimated_quantity", {})
    quantity_value = estimated_quantity.get("value", "0")

    macros = result.get("macronutrients", {})

    protein = macros.get("protein_g", "0")
    carbs = macros.get("carbohydrates_g", "0")
    fat = macros.get("fat_g", "0")

    uid = request.POST.get("uid")

    print(uid,"gggggggggggggggggggggg")
    user = Users.objects.get(AUTH_USER_id=uid)


    food_obj, created = Food_Database.objects.get_or_create(
    Food_Name=food_name,
        defaults={
            "Photo": fname,
            "description": "AI detected food"
        }
    )

    import datetime

    Daily_Food.objects.create(
        USERS=user,
        FOOD_DATABASE=food_obj,
        Food_Time=datetime.datetime.now().strftime("%H:%M"),
        Protein=protein,
        Carbohydrate=carbs,
        Fat=fat,
        Date=datetime.date.today(),
        Type="AI Scan"
    )



    
    v=float(estimated_quantity.get("value"))/100

    nutrients_list = []
    data=result
        # Macronutrients (grams)
    macros = data.get("macronutrients", {})

    nutrients_list.append({
            "nutrientName": "Calories",
            "value": result.get("calories_kcal", "N/A"),
            "unit": "g"
        })
    
    nutrients_list.append({
            "nutrientName": "Total Quantity",
            "value": estimated_quantity.get("value"),
            "unit": "g"
        })

    for key, value in macros.items():
        nutrient_name = key.replace("_g", "").replace("_", " ").title()
        
        nutrients_list.append({
            "nutrientName": nutrient_name,
            "value": float(value)*v,
            "unit": "g"
        })

    # Other nutrients (unknown quantity → set 0 or None)
    for nutrient in data.get("other_nutrients", []):
        nutrients_list.append({
            "nutrientName": nutrient,
            "value": None,   # since no quantity provided
            "unit": "mg"     # typical micronutrient unit
        })



    print(nutrients_list)
    k={'status':'ok','foodname':data.get("food_name", "Unknown"),
       'cal': result.get("calories_kcal", "N/A"),
       
        'nutrients':nutrients_list}
    print(k)

    return JsonResponse(k)




from django.http import JsonResponse
from django.db.models import Sum
import datetime
from .models import Daily_Food, Users


def find_daily_intake(request):

    lid = request.POST.get('lid')

    try:
        user = Users.objects.get(LOGIN_id=lid)
    except:
        return JsonResponse({"status": "error", "message": "User not found"})

    today = datetime.date.today()
    week_data = []

    for i in range(6, -1, -1):  # last 7 days
        day = today - datetime.timedelta(days=i)

        foods = Daily_Food.objects.filter(
            USERS=user,
            Date=day
        ).aggregate(
            protein=Sum('Protein'),
            carbs=Sum('Carbohydrate'),
            fat=Sum('Fat')
        )

        protein = float(foods['protein'] or 0)
        carbs = float(foods['carbs'] or 0)
        fat = float(foods['fat'] or 0)

        # calorie estimation
        calories = (protein * 4) + (carbs * 4) + (fat * 9)

        week_data.append({
            "date": str(day),
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "calories": calories
        })

    return JsonResponse({
        "status": "ok",
        "week_data": week_data
    })