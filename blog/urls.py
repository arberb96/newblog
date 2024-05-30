from django.urls import path
from .views import HomeView, PostDetailView, DeletePostView
from django.conf import settings
from django.conf.urls.static import static
from .views import create_post
from .views import edit_post_and_paragraphs, test_post_view, your_view, user_login, user_logout,register

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home", your_view, name="test-pagination"),
    # path("news/create", PostCreateView.as_view(), name="add-post"),
    path("news/create", create_post, name="add-post"),
    path("news/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    # path("news/update/<int:pk>/", UpdatePostView.as_view(), name="update-post"),
    path("news/update/<int:pk>/", edit_post_and_paragraphs, name='update-post'),
    path("news/delete/<int:pk>/", DeletePostView.as_view(), name="delete-post"),
    
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    path("test/", test_post_view, name="test-post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)