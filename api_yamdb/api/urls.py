from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, create_user,
                    get_token)

auth_patterns = [
    path('signup/', create_user),
    path('token/', get_token)
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename="reviews")
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename="comments")

v1_urls = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
