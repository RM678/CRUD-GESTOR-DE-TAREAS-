from django.db import models
from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://rafaeljesusmolina2004:Test_password123@crudmongo.e2m9i2u.mongodb.net/?retryWrites=true&w=majority&appName=CrudMongo'
client = MongoClient(MONGO_URI)
db = client['Crud_Mongo_2']

class Tarea(models.Model):
    nombre = models.CharField(max_length=255)
    edad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre