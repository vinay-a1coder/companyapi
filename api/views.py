import redis
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from companyapi.settings import MAX_STUDENTS
from .models import Company, User, Student
from .serializers import CompanySerializer, StudentSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required
from .permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from .serializers import UserUpdateSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from .signals import company_created_handler, handle_company_created, post_save_student
from django.dispatch import Signal
from .tasks import generate_random_message
from django.views.decorators.csrf import csrf_exempt
from .utils import get_current_count

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)

company_created = Signal()

@csrf_exempt
def send_random_message(request, student_id):
    if request.method == 'POST':
        # Trigger the Celery task with the provided ID
        # breakpoint()
        # generate_random_message(student_id)
        generate_random_message.apply_async(args=(student_id,))
        return JsonResponse({"message": "Random message generation task has been queued."})
    elif request.method == 'GET':
        return HttpResponse("This is a GET request. Use POST to send a message.")
    else:
        return HttpResponse("Unsupported HTTP method.")
    

@csrf_exempt
@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    curr_count = get_current_count()
    if curr_count >= MAX_STUDENTS:
        return HttpResponse("No more seats are available!")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@cache_page(60*60)
@login_required
def company_list(request):
    # Attempt to fetch data from Redis
    companies = cache.get('company_list')

    if not companies:
        # Data not found in Redis, fetch it from the database
        companies = Company.objects.all()
        
        # Store the data in Redis
        cache.set('company_list', companies)

    serializer = CompanySerializer(companies, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@login_required
# @permission_classes([IsAdminUser])
def company_create(request):
    serializer = CompanySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        company_created.send(sender=None, company=serializer)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@login_required
def company_detail(request, pk):
    # Attempt to fetch data from Redis
    company_cache_key = f'company_detail_{pk}'
    company = cache.get(company_cache_key)

    if not company:
        # Data not found in Redis, fetch it from the database
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response(status=404)

        # Store the data in Redis
        cache.set(company_cache_key, company)

    serializer = CompanySerializer(company, context={'request': request})
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@login_required
def company_update(request, pk):
     # Attempt to fetch data from Redis
    company_cache_key = f'company_detail_{pk}'
    company = cache.get(company_cache_key)

    if not company:
        # Data not found in Redis, fetch it from the database
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response(status=404)

    serializer = CompanySerializer(company, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()

        # Update the data in Redis
        cache.set(company_cache_key, serializer.instance)

        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@login_required
def company_delete(request, pk):
    # Attempt to fetch data from Redis
    company_cache_key = f'company_detail_{pk}'
    company = cache.get(company_cache_key)

    if not company:
        # Data not found in Redis, fetch it from the database
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response(status=404)

    company.delete()
    return Response(status=204)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        # Try to fetch access token from Redis
        access_token = fetch_access_token_from_redis(username)

        if access_token:
            return Response({
                'access': access_token,
            }, status=status.HTTP_200_OK)
        else:
            # Access token not found in Redis, fall back to database authentication
            user = authenticate(username=username, password=password)

            if user:
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                # Store access token in Redis
                store_access_token(username, str(refresh.access_token))

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def fetch_access_token_from_redis(username):
    # Fetch access token from Redis
    access_token = redis_instance.get(username)
    if access_token:
        return access_token.decode()  # Decode bytes to string
    else:
        return None
    

@api_view(['POST'])
def registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Store access token in Redis
        store_access_token(user.id, str(refresh.access_token))

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def store_access_token(user_id, access_token):
    # Store the access token in Redis with an expiration time
    redis_instance.set(user_id, access_token, ex=3600)  # Set expiration time as needed


@api_view(['DELETE'])
@login_required
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)

    user.delete()
    return Response(status=204)


@api_view(['PATCH'])
@login_required
def user_update_view(request, id):
    # print("----------update--request_id---",request.id)
    if request.method == 'PATCH':
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        # breakpoint()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  