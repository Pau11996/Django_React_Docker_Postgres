import operator

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from utils.uploading import upload_function


class Products(models.Model):
    """Модель всех товаров"""

    name = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Катеригоя товара")
    price = models.IntegerField(verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара", default="Описание появится позже")
    image = models.ImageField(upload_to=upload_function)
    out_of_stock = models.BooleanField(default=False, verbose_name='Нет в наличии')
    offer_of_the_week = models.BooleanField(default=False, verbose_name="Предложение недели")
    released_data = models.DateField(verbose_name="Дата релиза")
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE, verbose_name="Мастерская" )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий товаров"""

    name = models.CharField(max_length=255, verbose_name='Название категории товара')
    slug = models.SlugField()

    def __str__(self):
        return self.name


class CartProduct(models.Model):
    """Продукт корзины"""

    MODEL_CARTPRODUCT_DISPLAY_NAME_MAP = {
        'Products': {'is_constructable': True, 'fields': ['name', 'category.name'], 'separator': ' - '}

    }

    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return f"Продукт: {self.content_object.name} (для корзины)"

    @property
    def display_name(self):
        model_fields = self.MODEL_CARTPRODUCT_DISPLAY_NAME_MAP.get(self.content_object.__class__._meta.model_name.capitalize())
        if model_fields and model_fields['is_constructable']:
            display_name = model_fields['separator'].join(
                [operator.attrgetter(field)(self.content_object) for field in model_fields['fields']]
            )
            return display_name
        if model_fields and not model_fields['is_constructable']:
            display_name = operator.attrgetter(model_fields['field'])(self.content_object)
            return display_name

        return self.content_object

    def save(self, *args, **kwargs):
        self.final_price = self.content_object.price * self.qty
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Корзина"""

    owner = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name="related_cart", verbose_name="Продукты для корзины"
    )
    total_products = models.IntegerField(default=0, verbose_name="Общее количество товара")
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена", null=True, blank=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def products_in_cart(self):
        return [c.content_object for c in self.products.all()]

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name= "Корзина"
        verbose_name_plural = "Корзины"


class Order(models.Model):
    """Заказ покупателя"""

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ получен покупателем')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey('Customer', verbose_name='Покупатель', related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateField(verbose_name='Дата создания заказа', auto_now=True)
    order_date = models.DateField(verbose_name='Дата заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Customer(models.Model):
    """Покупатель"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    customer_orders = models.ManyToManyField(
        Order, blank=True, verbose_name='Заказы покупателя', related_name='related_customer'
    )
    wishlist = models.ManyToManyField(Products, blank=True, verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=55, null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Workshop(models.Model):
    """Модель мастерских"""

    name = models.CharField(max_length=255, verbose_name='Название мастерской')
    slug = models.SlugField()

    def __str__(self):
        return self.name



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




