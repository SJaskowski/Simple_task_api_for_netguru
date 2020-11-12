import requests
from django.db.models import Count
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from .models import Car, Rating
from .serializers import CarSerializer, RatingSerializer


class CarService(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def post(self, request, *args, **kwargs):
        try:
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{request.data["make_name"]}?format=json'
            response = requests.get(url).json()
            if response['Count'] == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)

            model_list = [car for car in response['Results'] if car['Model_Name'] == request.data['model_name']]
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(model_list) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().post(request, *args, **kwargs)


class RateService(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        try:
            make_name = request.data['make_name']
            model_name = request.data['model_name']
            if not Car.objects.filter(make_name=make_name, model_name=model_name).first():
                raise MultiValueDictKeyError
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)



class CarPopularity(ListAPIView):
    queryset = Car.objects.all().annotate(Count('ratings')).order_by('ratings__count')
    serializer_class = CarSerializer

    def get(self, request, *args, **kwargs):
        """
            Optional in link parameter "Show" - Describes how many top cars to display
        """
        try:
            nr_to_show = int(request.GET.get('show'))
        except (MultiValueDictKeyError, TypeError):
            nr_to_show = 5
        self.queryset = self.queryset.reverse()[:nr_to_show]
        return super().get(request, *args, **kwargs)




