

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SimpleDroneTask
from .utils import send_drone_command

@api_view(['POST'])
def initiate_drone_task(request):
    """
    API to initiate a drone task for spraying.
    """
    # Get the coordinates and user from the request
    coordinates = request.data.get('coordinates', {})
    user = request.user
    
    # Create the drone task
    task = SimpleDroneTask.objects.create(
        task_type='spray',
        coordinates=coordinates,
        created_by=user
    )

    # Send the command to the drone
    send_drone_command(coordinates)
    
    # Update task status
    task.status = 'completed'
    task.save()
    
    return Response({
        'status': 'Task Completed',
        'task_id': task.id
    })
