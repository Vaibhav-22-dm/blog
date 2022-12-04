from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('getblog/<int:pk>/', getBlog, name='get-blog'),
    path('addblog/', addBlog, name='add-blog'),
    path('editblog/', editBlog, name='edit-blog'),
    path('listblog/', listBlog, name='list-blog'),
    path('listpopularblog/', listPopularBlog, name='list-popular-blog'),
    path('deleteblog/', deleteBlog, name='delete-blog'),
    path('getcomment/<int:pk>/', getComment, name='get-comment'),
    path('addcomment/', addComment, name='add-comment'),
    path('editcomment/', editComment, name='edit-comment'),
    path('deletecomment/', deleteComment, name='delete-comment'),
    path('listcomment/', listComment, name='list-comment'),
    path('getblogcomment/<int:pk>/', getBlogComment, name='get-blog-comment'),
    path('getreaction/<int:pk>/', getReaction, name='get-reaction'),
    path('addreaction/', addReaction, name='add-reaction'),
    path('editreaction/', editReaction, name='edit-reaction'),
    path('deletereaction/', deleteReaction, name='delete-reaction'),
    path('listreaction/', listReaction, name='list-reaction'),
    path('getblogreaction/<int:pk>/', getBlogReaction, name='get-blog-reaction'),
]
