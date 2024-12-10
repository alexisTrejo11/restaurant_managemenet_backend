from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class ApiResponse:

    @staticmethod
    def not_found(message):
        return Response({
            'data': None,
            'message': message,
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def bad_request(message):
        return Response({
            'data': None,
            'message': message,
            'time_stamp': datetime.now(),
        }, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def conflict(message):
        return Response({
            'data': None,
            'message': message,
            'time_stamp': datetime.now(),
        }, status=status.HTTP_409_CONFLICT)


    @staticmethod
    def ok(data, message):
        return Response({
            'data': data,
            'message': message,
            'time_stamp': datetime.now(),
        })
    
    @staticmethod
    def found(data, entity, parameter, value):
        return Response({
            'data': data,
            'message': f'{entity} with {parameter} [{value}] successfully fetched',
            'time_stamp': datetime.now(),
        })

    @staticmethod
    def created(message):
        return Response({
            'data': None,
            'message': message,
            'time_stamp': datetime.now(),
        },status=status.HTTP_201_CREATED)
    
    @staticmethod
    def created(data, message):
        return Response({
            'data': data,
            'message': message,
            'time_stamp': datetime.now(),
        },status=status.HTTP_201_CREATED)
