from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.AdListView.as_view(), name='menu_main'),
    path('ads', views.AdListView.as_view(), name='ads'),
    path('ad/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/create',
    views.AdCreateView.as_view(success_url=reverse_lazy('ads')), name='ad_create'),
    path('ad/<int:pk>/update',
    views.AdUpdateView.as_view(success_url=reverse_lazy('ads')), name='ad_update'),
    path('ad/<int:pk>/delete',
    views.AdDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_delete'),
]

# urlpatterns = [
#     path('', views.TheView.as_view(), name='menu_main'),
#     path('page1', views.TheView.as_view(), name='menu_page1'),
#     path('page2', views.TheView.as_view(), name='menu_page2'),
#     path('page3', views.TheView.as_view(), name='menu_page3'),
# ]