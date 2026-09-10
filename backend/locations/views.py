from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import WorkerLocation
from .serializers import WorkerLocationSerializer

class UpdateLocationView(views.APIView):
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        heading = request.data.get('heading', 0.0)

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        worker = request.user
        location, created = WorkerLocation.objects.update_or_create(
            worker=worker,
            defaults={
                'latitude': float(latitude),
                'longitude': float(longitude),
                'heading': float(heading)
            }
        )

        serialized_data = WorkerLocationSerializer(location).data

        # Broadcast location to Live Map via Django Channels
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "live_map_group",
                {
                    "type": "location_update",
                    "data": serialized_data
                }
            )
        except Exception as e:
            print("WebSocket location broadcast error:", e)

        return Response({'status': 'success', 'location': serialized_data})

class LiveWorkerLocationsView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WorkerLocationSerializer
    queryset = WorkerLocation.objects.filter(worker__is_online=True)
