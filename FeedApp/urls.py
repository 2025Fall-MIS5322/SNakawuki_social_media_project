from django.urls import path
from . import views
# Import the specific class you want to use for the main homepage
from .views import AllPostsHomePageView 



app_name = 'FeedApp'

urlpatterns = [
     # CHANGE 1: Use the class-based view for the main homepage ("/")
    # You use .as_view() when calling a class-based view
    path('', AllPostsHomePageView.as_view(), name='home'), 
    # path('', views.index, name='index'),
    path('index/', views.index, name='index'), 
    path('profile/', views.profile, name='profile'),
    path('myfeed', views.myfeed, name='myfeed'),
    path('new_post', views.new_post, name='new_post'),
    path('friendsfeed', views.friendsfeed, name='friendsfeed'),
    path('comments/<int:post_id>', views.comments,name='comments'),
    path('friends', views.friends, name='friends'),
    ]
   