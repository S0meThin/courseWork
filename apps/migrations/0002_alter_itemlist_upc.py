# Generated by Django 4.1.3 on 2023-12-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemlist',
            name='UPC',
            field=models.CharField(max_length=12),
        ),
    ]