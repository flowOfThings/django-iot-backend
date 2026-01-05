result = []
for d in qs:
    result.append({
        "device_id": d.device_id,
        "temperature": getattr(d, "temperature", None),
        "humidity": getattr(d, "humidity", None),
        "timestamp": d.timestamp.isoformat() if d.timestamp else None,
    })
return Response(result)