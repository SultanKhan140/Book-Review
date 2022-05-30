from django.urls import path
from . import views,api_views
urlpatterns = [
    path('', views.index),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('book-search/', views.book_search, name='book_search'),
    path('books/<int:book_pk>/reviews/new/',views.review_edit,name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/',views.review_edit,name='review_edit'),
    path('books/<int:pk>/media/',views.book_media,name='book_media'),
    # path('api/all_books_count/',api_views.first_api_view,name='all_books_count'),
    # path('api/all_books/',api_views.all_books,name='all_books'),
    path('api/all_books/',api_views.AllBooks.as_view(),name='all_books'),
    path('api/contributors/',api_views.ContributorView.as_view(),name='contributors'),
    path('api/login/',api_views.Login.as_view(),name='login'),
    path('api/review/',api_views.ReviewView.as_view(),name='reviews')

]