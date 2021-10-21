from django.urls import path, include
from .views import (HomePageView,
                    CategoryPageView,
                    HashtagPageView,AboutPageView,
                    ContactPageView,PostDetailView)
urlpatterns = [
    path('',HomePageView.as_view(), name="home"),
    path('category/<slug:slug>',CategoryPageView.as_view(),name="category"),
    path('detail/<slug:slug>',PostDetailView.as_view(), name="detail"),
    path('hashtag/<slug:slug>', HashtagPageView.as_view(), name="hashtag"),
    path('about/',AboutPageView.as_view(),name="about"),
    path('contact/',ContactPageView.as_view(),name="contact"),
    path('profile/', include('users.urls')),
]