from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SensorDataSerializer

@api_view(['POST'])
def ingest(request):
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "stored"})
    return Response(serializer.errors, status=400)