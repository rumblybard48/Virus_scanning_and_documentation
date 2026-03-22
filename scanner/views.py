from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import tempfile
from .utils import run_clamav_scan, encrypt_file, load_key  # Make sure load_key is imported
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "uploaded_documents"
ENCRYPTED_DIR = "encrypted_documents"

@api_view(['POST'])
def scan_file(request):
    api_key = request.headers.get('X-API-KEY')
    VALID_API_KEY = os.getenv("api_key")
    if api_key != VALID_API_KEY:
        return JsonResponse({"error": "Unauthorized access"}, status=401)

    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    # Step 1: Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name

    # Step 2: Run ClamAV scan
    is_clean, result = run_clamav_scan(temp_path)

    if not is_clean:
        os.remove(temp_path)
        return Response({'status': 'Infected', 'details': result}, status=status.HTTP_200_OK)

    # Step 3: Move to permanent folder
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    final_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    if os.path.exists(final_path):
        os.remove(final_path)
    os.rename(temp_path, final_path)

    # Step 4: Encrypt the clean file
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    encrypted_path = os.path.join(ENCRYPTED_DIR, uploaded_file.name + ".enc")

    key = load_key()
    encrypt_file(final_path, encrypted_path, key)

    # (Optional) remove original unencrypted file
    # os.remove(final_path)

    return Response({
        'status': 'Clean and encrypted',
        'file_saved_as': final_path,
        'encrypted_as': encrypted_path
    }, status=200)
