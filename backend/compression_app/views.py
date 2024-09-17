from rest_framework import generics, permissions
#from django.contrib.auth import authenticate, login
#from rest_framework_simplejwt.tokens import RefreshToken
#rom django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, login
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import sys
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, GuestUser, CompressionTask
from .serializers import UserSerializer, ImageCompressionSerializer
from .compression import compress_image
from django.http import FileResponse
from .compression_report import generate_pdf_report

# Create your views here.

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=400)

        if user and check_password(password, user.password) and user.is_active:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'message': 'Invalid credentials'}, status=400)
    

"""class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=400)

        if user and user.check_password(password) and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({'message': 'Invalid credentials'}, status=400)"""

"""class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'message': 'Invalid credentials'}, status=400)"""

class ImageCompressView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user
            is_guest = False
        else:
            # If not authenticated, handle as guest user
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key
            user, created = GuestUser.objects.get_or_create(session_id=session_id)
            is_guest = True

        serializer = ImageCompressionSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['compressed_image']
            compression_type = serializer.validated_data['compression_type']

            # Compress the image
            compressed_image_path = compress_image(image, compression_type)

             # Create an InMemoryUploadedFile from the BytesIO object
            compressed_image_file = InMemoryUploadedFile(
                file=compressed_image_path,
                field_name='compressed_image',
                name=image.name,
                content_type=image.content_type,
                size=sys.getsizeof(compressed_image_path),
                charset=None
            )

            # Save the image to the database associated with the user (guest or authenticated)
            CompressionTask.objects.create(
                user=user if not is_guest else None,  # If logged-in user, store user
                guest_user=user if is_guest else None,  # If guest user, store guest_user
                compressed_image=compressed_image_file,
                compression_type=compression_type
            )

            return Response({'image_path': compressed_image_path}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PDFReportView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        compressed_images = CompressionTask.objects.get(user=user)
        pdf_buffer = generate_pdf_report(compressed_images)
        return FileResponse(pdf_buffer, as_attachment=True, filename='compression_report.pdf')
    