from django.urls import path
from posts.api import views


urlpatterns = [
    path('post_headline/',views.PostHeadlineAPIView.as_view(),name="PostHeadline"),
    path('post_summary/',views.ShowPostwithSummary.as_view(),name="PostSummary"),
    path('summary/',views.PostSummary.as_view(),name="Summary"),
    path('category_posts/',views.PostCategorywise.as_view(),name="CategoryPosts"),
]
