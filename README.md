# Virus Scanning and Secure Document Management System

This project is a backend-based Document Management System (DMS) built using Django and Django REST Framework. It enables users to upload files, scan them for viruses using ClamAV, and securely store them using encryption.

---

## Features

- File upload via API
- Virus scanning using ClamAV
- File encryption using Fernet (cryptography)
- API key-based authentication
- Secure storage of uploaded documents
- REST API implementation using Django REST Framework

---

## Tech Stack

- Python
- Django
- Django REST Framework
- ClamAV
- Cryptography (Fernet)
- Postman (for API testing)

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/rumblybard48/Virus_scanning_and_documentation.git
cd your-repo
### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Install ClamAV

Download ClamAV from:
https://www.clamav.net/downloads

After installation:
- Start `clamd.exe`
- Ensure it is running on port 3310

### 5. Create a .env file

Create a `.env` file in the root directory

API_KEY=your_secret_key

### 6. Apply migrations

python manage.py migrate

### 7. Run the server

python manage.py runserver

## API Endpoint

### Upload and Scan File

Endpoint:

POST /api/upload/

Headers:

X-API-KEY: your_secret_key

Body:
- form-data
- key: file (type: File)

## Workflow

1. File is uploaded via API  
2. File is stored temporarily  
3. File is scanned using ClamAV  
4. If clean, it is stored permanently  
5. File is encrypted using Fernet  
6. Encrypted file is saved securely  

## Testing Virus Detection

You can test virus detection using the EICAR test string:
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
Save this as a `.txt` file and upload it. The system should detect it as infected.

## Notes

- Do not upload ClamAV binaries to GitHub
- Keep `.env` and `secret.key` files secure
- This setup is intended for development purposes

---
## Future Improvements
- Frontend integration (Angular or React)
- JWT-based authentication
- Cloud storage integration
- Secure file download with decryption
- Role-based access control
