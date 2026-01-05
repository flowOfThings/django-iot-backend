import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer

# Shared secret must match the ESP code
ESP_SECRET_KEY = "b218f377b1960218c6ef9463bd29d926"

def verify_jwt(token):
    """
    Decode and verify JWT from ESP node.
    Returns payload dict if valid, else raises.
    """
    return jwt.decode(token, ESP_SECRET_KEY, algorithms=["HS256"])

@api_view(['POST'])
def ingest(request):
    token = request.data.get("token")
    if not token:
        return Response({"error": "Missing token"}, status=400)

    try:
        payload = verify_jwt(token)
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

@api_view(['GET'])
def list_data(request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return Response({"error": "Missing or invalid Authorization header"}, status=401)

    token = token.split(" ")[1]
    try:
        verify_jwt(token)
    except ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except InvalidTokenError:
        return Response({"error": "Invalid token"}, status=401)

    # Optional filter by device_id
    device_id = request.query_params.get("device_id")

    from .models import SensorData
    if device_id:
        data = SensorData.objects.filter(device_id=device_id).order_by('-timestamp')
    else:
        data = SensorData.objects.all().order_by('-timestamp')

    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)

    # Fetch all sensor data, newest first
    data = SensorData.objects.all().order_by('-timestamp')
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)