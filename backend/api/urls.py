from django.urls import path, re_path, include
from django.conf.urls import url

from .views import index, authorView, postView, authView, commentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# if you are adding a static path, consider put it on top of dynamic paths
# vise versa
urlpatterns = [
    # Index
    path('', index.index, name="index"),
    
    # Auth endpoints [Login/Register] **
    path('author/login/', authView.LoginView.as_view(), name="login"),
    path('author/register/', authView.createSignupRequest, name="register"),

    # Profile Endpoint **
    path('author/<str:authorID>/', authorView.AuthorDetail, name="authorDetail"),
    path('authors/',authorView.AuthorList, name ='authorList'),

    # Post endpoints
    path('author/<str:authorID>/stream/', postView.getStreamPosts, name="streamPosts"),
    path('author/<str:authorID>/posts/', postView.PostByAuthorID, name="authorPosts"),
    path('author/<str:authorID>/posts/<str:postID>', postView.PostByPostID, name="authorPost"),

    # Comment Endpoints
    path('author/<str:author_id>/posts/<str:postID>/comments', commentView.CommentDetail, name='commentDetail'),

    # Token Endpoints
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

