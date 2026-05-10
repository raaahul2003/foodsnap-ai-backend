from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    Name = models.CharField(max_length=50)
    Dob = models.DateField()
    Email = models.CharField(max_length=100)
    Gender = models.CharField(max_length=30)
    Phone = models.CharField(max_length=30)
    Photo = models.CharField(max_length=500)
    Place = models.CharField(max_length=100)
    Post = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pin = models.CharField(max_length=100)
    AUTH_USER=models.OneToOneField(User,on_delete=models.CASCADE)

class Food_Database(models.Model):
    Food_Name = models.CharField(max_length=50)
    Photo = models.CharField(max_length=500)
    description = models.CharField(max_length=300)

class Complaint(models.Model):
    Date = models.DateField()
    Complaint = models.CharField(max_length=300)
    Status = models.CharField(max_length=50)
    Reply = models.CharField(max_length=50)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)

class Feedback(models.Model):
     Date = models.DateField()
     Feedback = models.CharField(max_length=300)
     USERS=models.ForeignKey(Users,on_delete=models.CASCADE)

class Daily_Food(models.Model):
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)
    FOOD_DATABASE=models.ForeignKey(Food_Database,on_delete=models.CASCADE)
    Food_Time = models.CharField(max_length=50)
    Protein = models.CharField(max_length=100)
    Carbohydrate = models.CharField(max_length=100)
    Fat = models.CharField(max_length=100)
    Date = models.DateField()
    Type = models.CharField(max_length=100)
    
class Health_Profile(models.Model):
    Height = models.CharField(max_length=50)
    Weight = models.CharField(max_length=50)
    Bmi = models.CharField(max_length=50)
    Blood_Group = models.CharField(max_length=50)
    Is_Cardiac = models.CharField(max_length=50)
    Body_Type = models.CharField(max_length=50)
    Bp = models.CharField(max_length=50)
    Cholestrol = models.CharField(max_length=50)
    Sugar_level = models.CharField(max_length=50)
    Thyroid_Status = models.CharField(max_length=50)
    Waist_Circumference = models.CharField(max_length=50)
    Hip_Circumference = models.CharField(max_length=50)
    Bone_Density_Tscore = models.CharField(max_length=50)
    Vitamin_D_Level = models.CharField(max_length=50)
    Iron_Ferritin = models.CharField(max_length=50)
    Smoking = models.CharField(max_length=50)
    Alcohol_Consumption = models.CharField(max_length=50)
    Physical_Activity_Level = models.CharField(max_length=50)
    healthprofile=models.CharField(max_length=100)
    protienvalue=models.CharField(max_length=100)
    fatvalue=models.CharField(max_length=100)
    carbvalue=models.CharField(max_length=100)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)


 