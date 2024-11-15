from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.

from . models import Farmer
from . serializers import FarmerSerializers

@api_view(['GET'])
def endpoints(request):
    data = ['/farmers', 'farmers/:username']
    return Response(data)

#add famer


@api_view(['GET','POST'])
def farmer_list(request):
    
    if request.method == 'GET':
            
        
        query = request.GET.get('query')
        
        if query == None:
            query = ""
        farmers = Farmer.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = FarmerSerializers(farmers, many=True)
        #data = ['teddy','kiptoo','lone']
        return Response(serializer.data)
    if request.method == 'POST':
        
        farmer = Farmer.objects.create(
            username = request.data['username'],
            bio = request.data['bio']
        ) 
        serializer = FarmerSerializers(farmer, many=False)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def farmer_detail(request, username):
    
    if request.method == 'GET':
        farmer = Farmer.objects.get(username=username)
        serializer = FarmerSerializers(farmer, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        farmer.username = request.data['username']
        farmer.bio = request.data['bio']
        
        farmer.save()
        serializer = FarmerSerializers(farmer, many=False)
        return Response(serializer.data)


    
    