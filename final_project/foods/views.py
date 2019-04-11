from foods.models import Cafe, Meal, Food, Comment, Favorite

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, RedirectView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


from foods.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from foods.forms import CreateForm, CommentForm


class FoodListView(OwnerListView):
    model = Food
    template_name = "food_list.html"

    def get(self, request):
        food_list = Food.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_foods.values('id')
            favorites = [row['id'] for row in rows]
        ctx = {'food_list': food_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


class FoodDetailView(OwnerDetailView):
    model = Food
    template_name = "food_detail.html"

    def get(self, request, pk):
        food = Food.objects.get(id=pk)
        comments = Comment.objects.filter(food=food).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'food': food, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)


class FoodDeleteView(DeleteView):
    model = Food
    template_name = "food_delete.html"


class FoodFormView(LoginRequiredMixin, View):
    template = 'food_form.html'
    success_url = reverse_lazy('foods')

    def get(self, request, pk=None):
        if not pk:
            form = CreateForm()
        else:
            food = get_object_or_404(Food, id=pk)
            form = CreateForm(instance=food)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk=None):
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            food = get_object_or_404(Food, id=pk)
            form = CreateForm(request.POST, request.FILES or None, instance=food)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        food = form.save(commit=False)
        food.owner = self.request.user
        food.save()
        return redirect(self.success_url)


def stream_file(request, pk):
    food = get_object_or_404(Food, id=pk)
    response = HttpResponse()
    response['Content-Type'] = food.content_type
    response['Content-Length'] = len(food.picture)
    response.write(food.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        food = get_object_or_404(Food, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, food=food)
        comment.save()
        return redirect(reverse_lazy('food_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        food = self.object.food
        return reverse_lazy('food_detail', args=[food.id])


class CafeListView(OwnerListView):
    model = Cafe
    template_name = "cafe_list.html"


class MealListView(OwnerListView):
    model = Meal
    template_name = "meal_list.html"

    def get(self, request, cafe_name=None):
        meals = Meal.objects.filter(cafe__name=cafe_name) if cafe_name else Meal.objects.all()
        context = {'meal_list': meals}
        return render(request, self.template_name, context)


class MealCreateView(CreateView):
    model = Meal
    fields = ['name', 'date', 'cafe', 'price', 'foods']
    template_name = "meal_form.html"


class MealUpdateView(UpdateView):
    model = Meal
    fields = ['name', 'date', 'cafe', 'price', 'foods']
    template_name = "meal_form.html"


class MealDeleteView(DeleteView):
    model = Meal
    template_name = "meal_delete.html"


class FavoriteToggleView(LoginRequiredMixin, View):
    def get(self, request, food_id):
        saved_dishes = Favorite.objects.filter(user=request.user, food_id=food_id)
        if saved_dishes.count() == 0:
            instance = Favorite(user=request.user, food_id=food_id)
            instance.save()
        else:
            saved_dishes.delete()
        return redirect(reverse_lazy('favorites'))


class FavoriteListView(OwnerListView):
    model = Food
    template_name = "favorite_list.html"

    def get(self, request):
        foods = (fav.food for fav in Favorite.objects.filter(user=request.user))
        return render(request, self.template_name, {'food_list': foods})


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add PK", pk)
        food = get_object_or_404(Food, id=pk)
        fav = Favorite(user=request.user, food=food)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        food = get_object_or_404(Food, id=pk)
        try:
            fav = Favorite.objects.get(user=request.user, food=food).delete()
        except Favorite.DoesNotExist as e:
            pass

        return HttpResponse()

