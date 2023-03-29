from django.shortcuts import render
from django.http.response import Http404
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response




# Create your views here.
class TodoAPIView(APIView):
    #READ a single TOdo


    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk) 
        except Todo.DoesNotExist:
            raise Http404


#Get list of Todos
    def get(self, request, pk = None, format = None):
        if pk:
            data = self.get_object(pk)
            serializer = TodoSerializer(data)
        else:
            data = Todo.objects.all()
            serializer = TodoSerializer(data, many= True)


            return Response(serializer.data)   


    def post(self, request, format = None):
        data = request.data
        serializer = TodoSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
                
        response = Response()

        response.data = {
            'message': "Todo Created successfully",
            "data": serializer.data
        }
        return response


    def put(self, request, format = None, pk= None):
        #Get the todo we want to update
        todo_update = Todo.objects.get(pk)
        serializer = TodoSerializer(instance = todo_update, data = request.data, partial = True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
                
        response = Response()

        response.data = {
            'message': "Todo Updated successfully",
            "data": serializer.data
        }
        return response


    def delete(self, request, pk = None, format = None):
        #Get todoobject to delete
        todo_to_del = Todo.objects.get(pk = pk)

        todo_to_del.delete()

        return Response({
            'message': "Todo deleted successfully"
        })


    