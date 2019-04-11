from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class Cafe(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300)

    # Picture path
    pic_path = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=300)

    def __str__(self):
        return self.category


class Food(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(default="Description of food")
    categories = models.ManyToManyField(Category)

    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorite', related_name='favorite_foods')

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateField()
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 30:
            return self.text
        return self.text[:26] + ' ...'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('food', 'user')

    def __str__(self):
        return self.user.username + ', ' + self.food.name
