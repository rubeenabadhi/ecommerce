# Generated by Django 4.2.6 on 2023-10-23 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='categ',
        ),
        migrations.DeleteModel(
            name='product',
        ),
    ]