from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    """Hello view just return 'Hello.'"""

    def get(self, _request):
        """Just return Hello."""
        return Response({'message': 'Hello.'}, status=status.HTTP_200_OK)
