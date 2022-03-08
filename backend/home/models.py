from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.safestring import mark_safe

from backend.utils.uploading import upload_function


class Products(models.Model):
    """Модель всех товаров"""

    name = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Катеригоя товара")
    price = models.IntegerField(verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара", default="Описание появится позже")
    image = models.ImageField(upload_to=upload_function)


class ImageGallery(models.Model):
    """Галерея изображений"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)
    use_in_slider = models.BooleanField(default=False)

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="200px"')

    def __str__(self):
        return f'изображение для {self.content_object}'

    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name




