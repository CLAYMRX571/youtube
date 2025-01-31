from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChanelSerializer
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from .models import Chanel

class CreateChanel(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        try:
            chanel = request.user.chanel
            if chanel:
                data = {
                    "status": False,
                    "msg": "Kanalingiz mavjud!!!"
                }
                return Response(data=data)
        except Exception as ex:
            pass 

        serializer = ChanelSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        chanel = serializer.save()
        chanel.user = request.user
        chanel.save()
        r_data = {
            "status": True,
            "msg": "Kanal yaratdingiz!!!",
            "data": serializer.data
        }
        return Response(data=r_data)

class DeleteChanel(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, pk):
        chanel = get_object_or_404(Chanel, id=pk)
        if chanel.user == request.user:
            chanel.delete()
            data = {
                'status': True,
                'msg': "Kanalingiz o'chirildi!!!"
            }
            return Response(data)
        else:
            data = {
                'status': False,
                'msg': "Kanal sizniki emas!!!"
            }
            return Response(data)

class GetChanel(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        chanel = request.user.chanel
        serializer = ChanelSerializer(instance=chanel, context={'request': request})
        data = {
            'status': True,
            'data': serializer.data
        }
        return Response(data=data)