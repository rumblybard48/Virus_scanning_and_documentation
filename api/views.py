import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .utils import scan_file_with_clamd

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=400)

        # Save temporarily
        temp_path = f"temp_uploads/{file_obj.name}"
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        with open(temp_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        # Scan file
        is_clean, result = scan_file_with_clamd(temp_path)

        if not is_clean:
            os.remove(temp_path)
            return Response({'error': f'Virus detected: {result}'}, status=400)

        # If clean: Move or save permanently
        final_path = f"uploaded_documents/{file_obj.name}"
        os.rename(temp_path, final_path)

        return Response({'message': 'File uploaded and scanned successfully'})
