from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, GuestUser, CompressionTask
from .serializers import UserSerializer, GuestUserSerializers, ImageCompressionSerializer
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
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'message': 'Invalid credentials'}, status=400)
    
class ImageUploadView(generics.CreateAPIView):
    queryset = CompressionTask.objects.all()
    serializer_class = ImageCompressionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def peform_create(self, serializer):
        # Add compression logic here
        uploaded_image = self.request.FILES.get('image')
        compressed_image = compress_image(uploaded_image)
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None, compressed_image=compressed_image)


class PDFReportView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        compressed_images = CompressionTask.objects.filter(user=user)
        pdf_buffer = generate_pdf_report(compressed_images)
        return FileResponse(pdf_buffer, as_attachment=True, filename='compression_report.pdf')
    