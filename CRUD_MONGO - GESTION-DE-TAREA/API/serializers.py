from rest_framework import serializers
from rest_framework.views import APIView
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = 'mongodb+srv://rafaeljesusmolina2004:Test_password123@crudmongo.e2m9i2u.mongodb.net/?retryWrites=true&w=majority&appName=CrudMongo'
client = MongoClient(MONGO_URI)
db = client['CrudMongo']

class UsuarioSerializer(serializers.Serializer):
    #Datos que queremos almacentar
    nombre = serializers.CharField(max_length=255)
    contraseña = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    
    #Validar si ya existe el email
    def validate_email(self, value):
        nueva_coleccion = db['usuarios']
        usuario = nueva_coleccion.find_one({'email': value})
        if usuario:
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

    #Crear un nuevo usuario
    def create(self, validated_data):
        nueva_colección = db['usuarios']
        nueva_colección.insert_one(validated_data)
        return validated_data

    #Actualizar el usuario
    def update(self, instance, validated_data):
        nueva_colección = db['usuarios']
        nueva_colección.update_one({'email': instance['email']}, {'$set': validated_data})
        instance.update(validated_data)
        return instance


class TareaSerializer(serializers.Serializer):
    #Datos de las Tareas
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, required=False)
    fecha_inicio = serializers.DateTimeField()
    fecha_final = serializers.DateTimeField()
    usuario = serializers.CharField(max_length=255)

    #Validar si este usuario existe
    def validate_usuario(self, value):
        nueva_colección = db['usuarios']
        usuario = nueva_colección.find_one({'email': value})
        if not usuario:
            raise serializers.ValidationError("El usuario no existe.")
        return value

    #Validar si este usuario tiene ya una tarea con ese nombre
    def validate_nombre(self, value):
        nueva_colección = db['tareas']
        tarea = nueva_colección.find_one({'nombre': value, 'usuario.email': self.initial_data['usuario']})
        if tarea:
            raise serializers.ValidationError("La tarea ya existe registrada por este usuario.")
        return value

    #Crear una nueva tarea
    def create(self, validated_data):
        nueva_colección = db['tareas']
        usuario_email = validated_data.pop('usuario')
        validated_data['usuario'] = {'email': usuario_email}
        nueva_colección.insert_one(validated_data)
        return validated_data

    #Actualizar tarea
    def update(self, instance, validated_data):
        nueva_colección = db['tareas']
        usuario_email = validated_data.pop('usuario', None)
        if usuario_email:
            validated_data['usuario'] = {'email': usuario_email}
        nueva_colección.update_one({'nombre': instance['nombre']}, {'$set': validated_data})
        instance.update(validated_data)
        return instance



class UsuarioList(APIView):
    def get(self, request):
        nueva_colección = db['usuarios']
        usuarios = nueva_colección.find()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioDetail(APIView):
    def get_object(self, email):
        nueva_colección = db['usuarios']
        try:
            usuario = nueva_colección.find_one({'email': email})
            return usuario
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, email):
        usuario = self.get_object(email)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    def put(self, request, email):
        usuario = self.get_object(email)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email):
        usuario = self.get_object(email)
        nueva_colección = db['usuarios']
        nueva_colección.delete_one({'email': usuario['email']})
        return Response(status=status.HTTP_204_NO_CONTENT)

class TareaList(APIView):
    def get(self, request):
        usuario_email = request.query_params.get('usuario')
        if usuario_email:
            nueva_colección = db['tareas']
            tareas = nueva_colección.find({'usuario.email': usuario_email})
            serializer = TareaSerializer(tareas, many=True)
            return Response(serializer.data)
        else:
            nueva_colección = db['tareas']
            tareas = nueva_colección.find()
            serializer = TareaSerializer(tareas, many=True)
            return Response(serializer.data)


    def post(self, request):
        serializer = TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TareaDetail(APIView):
    def get_object(self, nombre):
        nueva_colección = db['tareas']
        try:
            tarea = nueva_colección.find_one({'nombre': nombre})
            return tarea
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, nombre):
        tarea = self.get_object(nombre)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, nombre):
        tarea = self.get_object(nombre)
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, nombre):
        tarea = self.get_object(nombre)
        nueva_colección = db['tareas']
        nueva_colección.delete_one({'nombre': tarea['nombre']})
        return Response(status=status_HTTP_204_NO_CONTENT)
