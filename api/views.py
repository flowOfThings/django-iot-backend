import jwt, datetime
from jwt import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer

# --- Helpers ---
def verify_device_jwt(token):
    """Verify JWT from ESP device using ESP secret."""
    return jwt.decode(token, settings.ESP_SECRET_KEY, algorithms=["HS256"])

def verify_frontend_jwt(token):
    """Verify JWT from frontend user using frontend secret."""
    return jwt.decode(token, settings.FRONTEND_SECRET_KEY, algorithms=["HS256"])

# --- Device ingest ---
@api_view(['POST'])
def ingest(request):
    token = request.data.get("token")
    if not token:
        return Response({"error": "Missing token"}, status=400)

    try:
        payload = verify_device_jwt(token)
    except ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except InvalidTokenError:
        return Response({"error": "Invalid token"}, status=401)

    # Extract fields from payload
    device_id = payload.get("device_id")
    temperature = payload.get("temperature")
    humidity = payload.get("humidity")
    timestamp = payload.get("timestamp")

    # Save to DB
    SensorData.objects.create(
        device_id=device_id,
        temperature=temperature,
        humidity=humidity,
        timestamp=timestamp
    )

    return Response({"status": "stored"})

# --- Frontend login ---
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Demo credentials only
    if username != "demo" or password != "demo":
        return Response({"error": "Invalid credentials"}, status=401)

    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    # Use FRONTEND_SECRET_KEY from settings, fallback if missing
    secret = settings.FRONTEND_SECRET_KEY or "fallbacksecret123"

    token = jwt.encode(payload, secret, algorithm="HS256")

    return Response({"token": token})

# --- Frontend data access ---
@api_view(['GET'])
def list_data(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response({"error": "Missing or invalid Authorization header"}, status=401)

    token = auth_header.split(" ")[1]
    try:
        verify_frontend_jwt(token)
    except ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except InvalidTokenError:
        return Response({"error": "Invalid token"}, status=401)

    # Optional filter by device_id
    device_id = request.query_params.get("device_id")
    if device_id:
        data = SensorData.objects.filter(device_id=device_id).order_by('-timestamp')
    else:
        data = SensorData.objects.all().order_by('-timestamp')

    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)