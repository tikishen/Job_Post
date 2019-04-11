from . import views
from django.views.generic import TemplateView
from django.urls import reverse_lazy, path, register_converter
from django.conf.urls import url, include

urlpatterns = [
    path('', views.FoodListView.as_view(), name='menu_main'),

    # Paths of food
    path('foods', views.FoodListView.as_view(), name='foods'),
    path('food/<int:pk>', views.FoodDetailView.as_view(), name='food_detail'),
    path('food/create', views.FoodFormView.as_view(success_url=reverse_lazy('foods')), name='food_create'),
    path('food/<int:pk>/update', views.FoodFormView.as_view(success_url=reverse_lazy('foods')), name='food_update'),
    path('food/<int:pk>/delete', views.FoodDeleteView.as_view(success_url=reverse_lazy('foods')), name='food_delete'),
    path('food_picture/<int:pk>', views.stream_file, name='food_picture'),
    # Paths of comments of food
    path('food/<int:pk>/comment', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('foods')),
         name='comment_delete'),

    # Paths of cafe
    path('cafes', views.CafeListView.as_view(), name='cafes'),

    # Paths of meal
    path('meals/', views.MealListView.as_view(), name='meals'),
    path('meals/<str:cafe_name>', views.MealListView.as_view(), name='meals'),
    path('meal/create', views.MealCreateView.as_view(success_url=reverse_lazy('meals')), name='meal_create'),
    path('meal/<int:pk>/update', views.MealUpdateView.as_view(success_url=reverse_lazy('meals')), name='meal_update'),
    path('meal/<int:pk>/delete', views.MealDeleteView.as_view(success_url=reverse_lazy('meals')), name='meal_delete'),

    # Paths of favorite
    path('favorite/<int:food_id>', views.FavoriteToggleView.as_view(), name='favorite_toggle'),
    path('favorites', views.FavoriteListView.as_view(), name='favorites'),
    path('food/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='food_favorite'),
    path('food/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='food_unfavorite'),
]
