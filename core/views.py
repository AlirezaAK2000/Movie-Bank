from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .serializers import (
    MovieSerializer,
    VoteSerializer,
    CommentSerializer,
    CommentListSerializer
)
from .models import (
    Movie,
    Vote,
    Comment
)
from rest_framework.decorators import (
    action,
    permission_classes
)
from rest_framework import viewsets , status


class MovieViewSet(viewsets.GenericViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    
    @action(methods=['POST'] , detail=False, url_path='admin/movie', permission_classes=[IsAdminUser] , url_name="create-movie")
    def createMovie(self , request):
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'message':'not valid'} , status=status.HTTP_400_BAD_REQUEST)                
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['PUT','DELETE'] , detail=False, url_path=r'admin/movie/(?P<pk>[^/.]+)', permission_classes=[IsAdminUser] , url_name="update-movie")
    def updateMovie(self, request , pk):
        try: 
            if request.method == 'PUT':
                req_data = request.data
                data = Movie.objects.get(pk=pk)
                serialized_data = self.serializer_class(data , data=req_data,partial=True)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({'message':'not valid'} , status=status.HTTP_400_BAD_REQUEST)  
            elif request.method == 'DELETE':
                Movie.objects.get(pk=pk).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)  
            
        except Movie.DoesNotExist:
            return Response({'message' : "movie doesn't exist."} , status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    @action(methods=['GET'] , detail=False, url_path='movies', permission_classes=[AllowAny] ,url_name="list-movie")
    def listMovies(self , request):
        try:
            movies = Movie.objects.all()
            return Response({'movies':self.serializer_class(movies , many=True).data} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=['GET'] , detail=False, url_path=r'movie/(?P<pk>[^/.]+)', permission_classes=[AllowAny] , url_name="get-movie")
    def getMovie(self, request , pk):
        try: 
            return Response(self.serializer_class(Movie.objects.get(pk=pk)).data,status=status.HTTP_200_OK)  
        except Movie.DoesNotExist:
            return Response({'message' : "movie doesn't exist."} , status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    @action(methods=['PUT','DELETE'] , detail=False, url_path=r'admin/comment/(?P<pk>[^/.]+)', permission_classes=[IsAdminUser] , url_name="update-comment")
    def updateDeleteComment(self, request , pk):
        try: 
            if request.method == 'PUT':
                req_data = request.data
                data = Comment.objects.get(pk=pk)
                serialized_data = self.serializer_class(data , data=req_data,partial=True)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({'message':'not valid'} , status=status.HTTP_400_BAD_REQUEST)  
            elif request.method == 'DELETE':
                Comment.objects.get(pk=pk).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)  
        except Comment.DoesNotExist:
            return Response({'message' : "comment doesn't exist."} , status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    @action(methods=['POST'] , detail=False, url_path='user/comment', permission_classes=[IsAuthenticated], url_name="create-comment")
    def createComment(self , request):
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.context["request"] = request
                serialized_data.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'message':'not valid'} , status=status.HTTP_400_BAD_REQUEST)                
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['GET'] , detail=False, url_path='comments', permission_classes=[AllowAny] ,url_name="list-comment")
    def listComments(self , request):
        try:
            movie_pk = int(request.query_params.get('movie'))
            movie = Movie.objects.get(pk=movie_pk)
            comments = Comment.objects.filter(movie_id=movie_pk)
            return Response({"name":movie.name,"comments":CommentListSerializer(comments , many=True).data} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoteViewset(viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    
    @action(methods=['POST'] , detail=False, url_path='user/vote', permission_classes=[IsAuthenticated] , url_name="create-vote")
    def createVote(self , request):
        try:
            data = request.data
            serialized_data = self.serializer_class(data=data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.context['request'] = request
                serialized_data.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'message':'not valid'} , status=status.HTTP_400_BAD_REQUEST)                
        except Exception as e:
            return Response({'message' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
