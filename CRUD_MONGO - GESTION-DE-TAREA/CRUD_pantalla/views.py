from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
from .forms import RegistroForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from datetime import datetime

def Login_usuario (request):
    if request.method == 'GET':
        return render (request, 'Login.html')
    else:
        email=request.POST.get('username')
        contraseña=request.POST.get('password')
        response = requests.get(f'http://localhost:8000/API/usuarios/{email}')
        #print (email)
        usuario = response.json()
        email_recibido=usuario['email']
        contraseña_recibida=usuario['contraseña']
        #print (f'Datos recibidos por peticion: {response.json()}')
        #print (f'Usuario y contraseña recibidos por peticion: {email_recibido} - {contraseña_recibida}')

        if contraseña == contraseña_recibida and contraseña != "":
            # Autentica el usuario
            response = redirect('Inicio')
            response.set_cookie('autenticado', 'true')
            response.set_cookie('email', email_recibido)
            return response
            #return redirect('Inicio')

        else:
            print ("Datos invalidos")
            return redirect ('Login')

def logout(request):
    if request.method == 'POST':
        # Eliminar la cookie de autenticación
        response = redirect('Login')
        response.delete_cookie('autenticado')
        response.delete_cookie('email')
        return response
    else:
        return HttpResponse('Invalid request method')


def Inicio(request):
    if 'autenticado' in request.COOKIES and request.COOKIES['autenticado'] == 'true':
        email=request.COOKIES['email']
        #print (email)
        #http://localhost:8000/API/tareas/?usuario=john.doe@example.com
        #response = requests.get(f'http://localhost:8000/API/tareas/{email}')
        response = requests.get(f'http://localhost:8000/API/tareas/?usuario={email}')
        #print (response.json())
        tareas=response.json()
        lista_tareas=[]
        for data in tareas:
            #convertir fechas a objeto datetime
            fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%dT%H:%M:%SZ')
            fecha_final = datetime.strptime(data['fecha_final'], '%Y-%m-%dT%H:%M:%SZ')
            #cambiar el formato
            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_final_str = fecha_final.strftime('%Y-%m-%d')
            if 'descripcion' in data: 

                tarea={
                    'nombre': data['nombre'],
                    'descripcion':data['descripcion'],
                    'fecha_inicio':fecha_inicio_str,
                    'fecha_final':fecha_final_str,
                    'usuario':data['usuario']
                }
            else:
                tarea={
                    'nombre': data['nombre'],
                    'fecha_inicio':fecha_inicio_str,
                    'fecha_final':fecha_final_str,
                    'usuario':data['usuario']
                }
            lista_tareas.append(tarea)
            
        return render(request, 'Inicio.html', {'tareas': lista_tareas})
    else:
        return redirect('Login')


def Agregar_tarea(request):
    if 'autenticado' in request.COOKIES and request.COOKIES['autenticado'] == 'true':
        if request.method == 'POST':

            email=request.COOKIES['email']
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_final_str = request.POST.get('fecha_final')

            # Convertir las fechas a datetime con el formato correcto
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            fecha_final = datetime.strptime(fecha_final_str, '%Y-%m-%d')
            # Convertir las fechas a formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
            fecha_inicio_iso = fecha_inicio.strftime('%Y-%m-%dT%H:%M:%SZ')
            fecha_final_iso = fecha_final.strftime('%Y-%m-%dT%H:%M:%SZ')
            if request.POST.get('descripcion')!="":
                data={
                'nombre':request.POST.get('nombre'),
                'descripcion':request.POST.get('descripcion'),
                'fecha_inicio': fecha_inicio_iso,
                'fecha_final': fecha_final_iso,
                'usuario':request.COOKIES['email'],
                }
                print (f"Descripcion:{request.POST.get('descripcion')}")
            else:
                data={
                'nombre':request.POST.get('nombre'),
                'fecha_inicio': fecha_inicio_iso,
                'fecha_final': fecha_final_iso,
                'usuario':request.COOKIES['email'],
                }
                print ("No existe")
            #print (data)
            data_json = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(f'http://localhost:8000/API/tareas/', data=data_json, headers=headers)
            print ("Datos agregados")

            return redirect('Inicio')


def Eliminar_tarea(request):
    if 'autenticado' in request.COOKIES and request.COOKIES['autenticado'] == 'true':
        if request.method == 'POST':
            email=request.COOKIES['email']
            nombre=request.POST.get('nombre')
            response= requests.delete(f'http://localhost:8000/API/tareas/{nombre}?usuario={email}')

            return redirect('Inicio')

def Editar_tarea(request):
    if 'autenticado' in request.COOKIES and request.COOKIES['autenticado'] == 'true':
        if request.method == 'POST':
            email=request.COOKIES['email']
            nombre=request.POST.get('nombre')
            #response= requests.delete(f'http://localhost:8000/API/tareas/{nombre}?usuario={email}')
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_final_str = request.POST.get('fecha_final')

            # Convertir las fechas a datetime con el formato correcto
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            fecha_final = datetime.strptime(fecha_final_str, '%Y-%m-%d')
            
            tarea={
                'nombre': request.POST.get('nombre'),
                'descripcion':request.POST.get('descripcion'),
                'fecha_inicio':fecha_inicio,
                'fecha_final':fecha_final,
                'usuario':email
            }
            print (tarea)
            return render(request,'Editar.html', {'tarea':tarea})

def Guardar_modificacion(request):
    if 'autenticado' in request.COOKIES and request.COOKIES['autenticado'] == 'true':
        if request.method == 'POST':
            email=request.COOKIES['email']
            nombre_antiguo=request.POST.get('nombre_antiguo')
            nombre=request.POST.get('nombre')

            print (f'Nombre antiguo:{nombre_antiguo}\nNombre nuevo:{nombre}')
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_final_str = request.POST.get('fecha_final')

            # Convertir las fechas a datetime con el formato correcto
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            fecha_final = datetime.strptime(fecha_final_str, '%Y-%m-%d')
            # Convertir las fechas a formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
            fecha_inicio_iso = fecha_inicio.strftime('%Y-%m-%dT%H:%M:%SZ')
            fecha_final_iso = fecha_final.strftime('%Y-%m-%dT%H:%M:%SZ')

            data={
            'nombre':request.POST.get('nombre'),
            'descripcion':request.POST.get('descripcion'),
            'fecha_inicio': fecha_inicio_iso,
            'fecha_final': fecha_final_iso,
            'usuario':email,
            }
            print (data)
            data_json = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            
            response= requests.put(f'http://localhost:8000/API/tareas/{nombre_antiguo}/?usuario={email}', data=data_json, headers=headers)
            print (response.json)
            print ("Datos agregados")

            return redirect('Inicio')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'email': form.cleaned_data['email'],
                'contraseña': form.cleaned_data['password']
            }
            print (data)
            response = requests.post('http://localhost:8000/API/usuarios/', data=data)
            if response.status_code == 201:
                return redirect('Login')
            else:
                form.add_error(None, "Ocurrió un error al registrar el usuario.")
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

