# Generated by Django 4.2.4 on 2023-08-24 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='название продукта')),
                ('price', models.IntegerField(verbose_name='цена товара')),
                ('description', models.TextField(verbose_name='описание товара')),
                ('is_published', models.BooleanField(default=True, verbose_name='публикация')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('price',),
            },
        ),
    ]
