from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.ThreadListView.as_view(), name='thread_list'),
    path('thread/create/', views.create_thread, name='create_thread'),
    path('thread/<slug:slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/<slug:slug>/delete/', views.delete_thread, name='delete_thread'),
    path('thread/<slug:thread_slug>/post/create/', views.create_post, name='create_post'),
]
