from ads.models import Ad

from django.views import View
from django.views import generic
from django.shortcuts import render

from ads.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class TheView(View) :
    def get(self, request) :
        x = { 'request' : request }
        return render(request, 'main_menu.html', x)

class AdListView(OwnerListView):
    model = Ad
    template_name = "ad_list.html"

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ad_detail.html"


class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = "ad_form.html"


class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = "ad_form.html"


class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ad_delete.html"



