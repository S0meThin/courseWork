# Generated by Django 4.1.3 on 2023-12-28 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UPC', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('mpq', models.IntegerField()),
                ('oh', models.IntegerField()),
                ('pack', models.IntegerField()),
                ('oOrd', models.IntegerField(default=0)),
                ('oRet', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('retail', models.FloatField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('qty', models.IntegerField()),
                ('timeTr', models.DateField(default='2004-12-12')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.itemlist')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.store')),
            ],
        ),
        migrations.CreateModel(
            name='returns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateR', models.DateField()),
                ('qty', models.IntegerField()),
                ('user', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.itemlist')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.store')),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delN', models.CharField(max_length=9, unique=True)),
                ('dateO', models.DateField()),
                ('dateD', models.DateField(default='2004-12-12')),
                ('status', models.BooleanField(default=False)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.store')),
            ],
        ),
        migrations.CreateModel(
            name='itemOrdered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.itemlist')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.orders')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.store')),
            ],
        ),
        migrations.AddField(
            model_name='itemlist',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.store'),
        ),
    ]