from django.urls import path
from posts.api import views


urlpatterns = [
    path('post_headline/',views.PostHeadlineAPIView.as_view(),name="PostHeadline"),
    path('post_summary/',views.ShowPostwithSummary.as_view(),name="PostSummary"),
    path('summary/',views.PostSummary.as_view(),name="Summary"),
    path('category_posts/',views.PostCategorywise.as_view(),name="CategoryPosts"),
    path('whole_post/',views.WholePostAPIView.as_view(),name="WholePost"),
    path('keyword_wikipedia/',views.WikipediaKeywordAPIView.as_view(),name="WikipediaKeyword"),
    path('save_categories/',views.SaveCategories.as_view(),name="SaveCategories"),
    path('get_categories/',views.GetCategories.as_view(),name="GetCategories"),
    path('get_category_post/',views.SpecificCategoryPost.as_view(),name="SpecificCategoryPost"),
    path('get_post_by_date/',views.PostByDate.as_view(),name="PostByDate"),
    path('get_today_date/',views.GetDates.as_view(),name="GetDates"),
    path('get_by_latest_date/',views.Last3DatesPosts.as_view(),name="Last3Posts"),
]
