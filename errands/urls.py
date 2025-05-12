from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'errands'  # Change namespace to 'errands' for template URLs

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'errands', views.ErrandViewSet, basename='errand')
router.register(r'applications', views.ErrandApplicationViewSet, basename='application')
router.register(r'reviews', views.ReviewViewSet, basename='review')


# API URLs
api_urlpatterns = [
    path('', include(router.urls)),
]

# Template URLs
urlpatterns = [
    path('', views.errand_list, name='errand_list'), # Main errand list view
    path('about/', views.about_page, name='about'),  
    path('help/', views.help_page, name='help'),  
     path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    
]