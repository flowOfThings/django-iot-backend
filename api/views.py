import jwt, datetime
from jwt import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username != "demo" or password != "demo":
        return Response({"error": "Invalid credentials"}, status=401)

    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    secret = settings.FRONTEND_SECRET_KEY or "fallbacksecret123"
    token = jwt.encode(payload, secret, algorithm="HS256")

    return Response({"token": token})


@api_view(['GET'])
def list_data(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    secret = settings.FRONTEND_SECRET_KEY or "fallbacksecret123"

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
    except (ExpiredSignatureError, InvalidTokenError):
        return Response({"error": "Invalid or expired token"}, status=401)

    device_id = request.query_params.get("device_id")
    if device_id:
        data = SensorData.objects.filter(device_id=device_id).order_by("-timestamp")[:50]
    else:
        data = SensorData.objects.all().order_by("-timestamp")[:50]

    return Response([{
        "device_id": d.device_id,
        "value": d.value,
        "timestamp": d.timestamp
    } for d in data])


@api_view(['POST'])
def ingest(request):
    token = request.data.get("token")
    secret = settings.ESP_SECRET_KEY or "espfallback123"

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
    except (ExpiredSignatureError, InvalidTokenError):
        return Response({"error": "Invalid or expired token"}, status=401)

    SensorData.objects.create(
        device_id=decoded["device_id"],
        value=decoded["value"],
        timestamp=datetime.datetime.utcnow()
    )

    return Response({"status": "stored"})