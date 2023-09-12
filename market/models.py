from django.conf import settings
from django.db import models


class Product(models.Model):
    """Модель товара"""
    title = models.CharField(max_length=50, verbose_name='название продукта')
    price = models.IntegerField(default=0, verbose_name='цена товара')
    cost_price = models.IntegerField(verbose_name='себестоимость товара')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='product/', verbose_name='изображение', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              null=True, blank=True)
    is_published = models.BooleanField(default=True, verbose_name='публикация')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('price',)

    def __str__(self):
        return f'Товар {self.title} (цена: {self.price})'

    def delete(self, using=None, keep_parents=False):
        self.is_published = False
        self.save()
