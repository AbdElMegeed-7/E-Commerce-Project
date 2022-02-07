# Generated by Django 4.0.1 on 2022-02-04 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=250)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD ORDER TOTAL')),
                ('email_address', models.EmailField(blank=True, max_length=250, verbose_name='EMAIL')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('billing_name', models.CharField(blank=True, max_length=250)),
                ('billing_address', models.CharField(blank=True, max_length=250)),
                ('billing_city', models.CharField(blank=True, max_length=250)),
                ('billing_postcode', models.CharField(blank=True, max_length=250)),
                ('billing_country', models.CharField(blank=True, max_length=250)),
                ('shipping_name', models.CharField(blank=True, max_length=250)),
                ('shipping_address', models.CharField(blank=True, max_length=250)),
                ('shipping_city', models.CharField(blank=True, max_length=250)),
                ('shipping_postcode', models.CharField(blank=True, max_length=250)),
                ('shipping_country', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'db_table': 'Order',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=250)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
    ]