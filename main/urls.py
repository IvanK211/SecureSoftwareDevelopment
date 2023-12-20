from django.urls import path
from . import views
from .views import ProductDetailView
app_name = "main"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("products/", views.products, name="products"),
    path('register/', views.register, name='register'),
    path("login", views.login_request, name ="login"),
    path("logout", views.logout_request, name= "logout"),
    path("user", views.userpage, name = "userpage"),
    path('search/', views.search_view, name='search'),
    path("api/products/", views.ProductAvailabilityView.as_view(), name="api-products"),
    path('api/products/<int:pk>/decrease_stock/', views.ProductDetailView.as_view(), name='decrease-stock'),
]