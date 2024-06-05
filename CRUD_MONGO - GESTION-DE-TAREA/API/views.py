from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TareaSerializer, UsuarioSerializer, db

class UsuarioList(APIView):
    def get(self, request):
        nueva_coleccion = db['usuarios']
        usuarios = nueva_coleccion.find()
        print ("LLegué aqui")
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
        nueva_coleccion = db['usuarios']
        try:
            usuario = nueva_coleccion.find_one({'email': email})
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
        nueva_coleccion = db['usuarios']
        nueva_coleccion.delete_one({'email': usuario['email']})
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
    def get_object(self, nombre, usuario_email):
        nueva_colección = db['tareas']
        try:
            tarea = nueva_colección.find_one({'nombre': nombre, 'usuario.email': usuario_email})
            return tarea
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, nombre):
        tarea = self.get_object(nombre, request.query_params.get('usuario'))
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, nombre):
        usuario_email = request.query_params.get('usuario')
        tarea = self.get_object(nombre, usuario_email)
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, nombre):
        usuario_email = request.query_params.get('usuario')
        if usuario_email:
            tarea = self.get_object(nombre, usuario_email)
            if tarea:
                nueva_colección = db['tareas']
                nueva_colección.delete_one({'nombre': nombre, 'usuario.email': usuario_email})
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

