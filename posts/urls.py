from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all'),
    path('new/',views.CreateRegularPost.as_view(),name='create'),
    path('create/', views.CreatePost.as_view(), name='create_post'),
    path('by/(?P<username>[-\w]+)',views.UserPosts.as_view(),name='for_user'),
    path('by/(?P<username>[-\w]+)/(?P<pk>\d+)',views.PostDetail.as_view(),name='single'),
    path('delete/(?P<pk>\d+)',views.DeletePost.as_view(),name='delete'),
]

# path('newpost/',views.CreatePost.as_view(),name='group_post'),