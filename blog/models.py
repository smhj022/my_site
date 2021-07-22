from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(50)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null="True", related_name="posts")
    tags = models.ManyToManyField(Tag)

    # overwrite method, here we overwriting save method to slugify over title(Harry Potter 1-->harry-potter-1)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
