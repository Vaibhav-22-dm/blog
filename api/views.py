from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
import socket

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def getBlog(request, pk):
    try:
        post = Post.objects.get(id=pk)
        ip = visitor_ip_address(request)
        try:
            socket.inet_aton(ip)
            visitor = VisitedIPs.objects.filter(post=post).filter(ip=ip)
            if not visitor:
                print('New Visitor')
                post.count += 1
                post.save()
                visitor = VisitedIPs.objects.create(ip=ip, post=post)
                visitor.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
        except socket.error:
            return Response({'message':'No such ip address exists!'}, status=403)
    except Post.DoesNotExist:
        return Response({'message':'No such post exists!'}, status=403)

@api_view(['GET'])
def listBlog(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    if request.GET.get('page_size'):
        paginator.page_size = int(request.GET.get('page_size'))
    post_objects = Post.objects.all()
    result_page = paginator.paginate_queryset(post_objects, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def listPopularBlog(request):
    posts = Post.objects.all().order_by('-count')[:5]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBlog(request):
    try:
        if request.user.has_perm('api.add_post'):
            post = PostSerializer(data=request.data)
            if post.is_valid():
                post.save()
        else:
            return Response({'message':'Your are not an author'}, status=403)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editBlog(request):
    try:
        if request.user.has_perm('api.add_post'):
            if 'id' in request.data:
                post = Post.objects.get(id=request.data['id'])
                if not post.owner == request.user or not request.user.is_superuser: 
                    return Response({'message':'This post doesn\'t belong to you!'}, status=403)
                if 'title' in request.data:
                    post.title = request.data['title']
                if 'body' in request.data:
                    post.body = request.data['body']
                post.save()
                return Response({'message':'Your post has been edited succesfully!'}, status=200)
        else:
            return Response({'message':'Your are not an author'}, status=403)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request):
    try:
        post = Post.objects.get(id=request.data['id'])
        if post.owner != request.user or not request.user.is_superuser:
            return Response({'message':'This blog doesn\'t belong to you!'}, status=403)
        post.delete()
        return Response({'message':'Your post has beedn deleted succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getComment(request, pk):
    try:
        post = Comment.objects.get(id=pk)
        serializer = CommentSerializer(post)
        return Response(serializer.data, status=200)
    except Comment.DoesNotExist:
        return Response({'message':'No such comment exist!'}, status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listComment(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    if request.GET.get('page_size'):
        paginator.page_size = int(request.GET.get('page_size'))
    comment_objects = Comment.objects.all()
    result_page = paginator.paginate_queryset(comment_objects, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):
    try:
        post = Post.objects.get(id=request.data['post'])
        comment = Comment.objects.create(owner=request.user, post=post, body=request.data['body'])
        comment.save()
        return Response({'message':'Your comment has been added succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editComment(request):
    try:
        comment = Comment.objects.get(id=request.data['id'])
        if comment.owner != request.user or not request.user.is_superuser:
            return Response({'message':'This comment doesn\'t belong to you!'}, status=403)
        comment.body = request.data['body']
        comment.save()
        return Response({'message':'Your comment has been edited succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComment(request):
    try:
        comment = Comment.objects.get(id=request.data['id'])
        if comment.owner != request.user or not request.user.is_superuser:
            return Response({'message':'This comment doesn\'t belong to you!'}, status=403)
        comment.delete()
        return Response({'message':'Your comment has been deleted succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['GET'])
def getBlogComment(request, pk):
    try:
        post = Post.objects.get(id=pk)
        print(post)
        comments = Comment.objects.filter(post=post)
        print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReaction(request, pk):
    print(request.user)
    if request.user.is_superuser == False:
        return Response({'message':'Your are not allowed to get reaction.'}, status=403)
    try:
        post = Reaction.objects.get(id=pk)
        serializer = ReactionSerializer(post)
        return Response(serializer.data, status=200)
    except Comment.DoesNotExist:
        return Response({'message':'No such reaction exist!'}, status=403)

@api_view(['GET'])
def getBlogReaction(request, pk):
    try:
        reactions = Reaction.objects.filter(id=pk)
        likes = reactions.filter(emotion='Like').count()
        dislikes = reactions.filter(emotion='Dislikes').count()
        return Response({'likes':likes, 'dislikes':dislikes}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listReaction(request):
    print(request.user)
    if request.user.is_superuser == False:
        return Response({'message':'Your are not allowed to list reactions.'}, status=403)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    if request.GET.get('page_size'):
        paginator.page_size = int(request.GET.get('page_size'))
    reaction_objects = Reaction.objects.all()
    result_page = paginator.paginate_queryset(reaction_objects, request)
    serializer = ReactionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addReaction(request):
    try:
        post = Post.objects.get(id=request.data['post'])
        try:
            reaction = Reaction.objects.get(post=post, owner=request.user)
            return Response({'message':'Your reaction has been recorded already!'}, status=403)
        except:
            pass
        reaction = Reaction.objects.create(owner=request.user, post=post, emotion=request.data['emotion'])
        reaction.save()
        return Response({'message':'Your reaction has been added succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editReaction(request):
    try:
        post = Post.objects.get(id=request.data['post'])
        reaction = Reaction.objects.filter(owner=request.user).filter(post=post)
        if reaction.owner != request.user or not request.user.is_superuser:
            return Response({'message':'This reaction doesn\'t belong to you!'}, status=403)
        reaction.emotion = request.data['emotion']
        reaction.save()
        return Response({'message':'Your reaction has been edited succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)
 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteReaction(request):
    try:
        post = Post.objects.get(id=request.data['post'])
        reaction = Reaction.objects.filter(owner=request.user).filter(post=post)
        if reaction.owner != request.user or not request.user.is_superuser:
            return Response({'message':'This reaction doesn\'t belong to you!'}, status=403)
        reaction.delete()
        return Response({'message':'Your reaction has been deleted succesfully!'}, status=200)
    except Exception as e:
        return Response({'message':str(e)}, status=500)


