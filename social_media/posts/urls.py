from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('detail/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name="post_detail"),
    path('detail/delete/<int:post_id>/', views.PostDeleteView.as_view(), name="post_delete"),
    path('detail/update/<int:post_id>/', views.PostUpdateView.as_view(), name="post_update"),
    path('create/', views.PostCreateView.as_view(), name="post_create"),
    path('reply/<int:post_id>/<int:comment_id>/', views.PostAddReplyView.as_view(), name="add_reply"),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name="post_like"),
]