# Generated by Django 4.0.6 on 2022-07-08 04:33

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
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=150, verbose_name='Books Name')),
                ('book_description', models.CharField(max_length=150, verbose_name='Books Description')),
                ('status', models.CharField(choices=[('BORROWED', 'BORROWED'), ('AVAILABLE', 'AVAILABLE')], default='AVAILABLE', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ReadBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
