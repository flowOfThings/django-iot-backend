import logging
import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData

logger = logging.getLogger(__name__)

def _get_secret(env_name: str, fallback: str) -> str:
    return getattr(settings, env_name, None) or fallback

def _ensure_str_token(token):
    if isinstance(token, bytes):
        try:
            return token.decode("utf-8")
        except Exception:
            return token
    return token

@api_view(["POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        if username != "demo" or password != "demo":
            return Response({"error": "Invalid credentials"}, status=401)

        payload = {
            "user": username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        }

        secret = _get_secret("FRONTEND_SECRET_KEY", "fallbacksecret123")
        token = jwt.encode(payload, secret, algorithm="HS256")
        token = _ensure_str_token(token)

        return Response({"token": token})
    except Exception as e:
        logger.exception("Login error")
        return Response({"error": "Internal server error"}, status=500)

@api_view(["GET"])
def list_data(request):
    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()
        if not token:
            return Response({"error": "Authorization token required"}, status=401)

        secret = _get_secret("FRONTEND_SECRET_KEY", "fallbacksecret123")
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError):
            return Response({"error": "Invalid or expired token"}, status=401)

        device_id = request.query_params.get("device_id")
        if device_id:
            qs = SensorData.objects.filter(device_id=device_id).order_by("-timestamp")[:50]
        else:
            qs = SensorData.objects.all().order_by("-timestamp")[:50]

        result = [
            {"device_id": d.device_id, "value": d.value, "timestamp": d.timestamp}
            for d in qs
        ]
        return Response(result)
    except Exception as e:
        logger.exception("list_data error")
        return Response({"error": "Internal server error"}, status=500)

@api_view(["POST"])
def ingest(request):
    try:
        # Accept token either in body or Authorization header for flexibility
        token = request.data.get("token") or request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not token:
            return Response({"error": "Token required"}, status=401)

        secret = _get_secret("ESP_SECRET_KEY", "espfallback123")
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
        except (ExpiredSignatureError, InvalidTokenError, DecodeError):
            return Response({"error": "Invalid or expired token"}, status=401)

        device_id = decoded.get("device_id")
        value = decoded.get("value")
        if device_id is None or value is None:
            return Response({"error": "Token payload missing device_id or value"}, status=400)

        SensorData.objects.create(
            device_id=device_id,
            value=value,
            timestamp=timezone.now()
        )

        return Response({"status": "stored"})
    except Exception as e:
        logger.exception("ingest error")
        return Response({"error": "Internal server error"}, status=500)