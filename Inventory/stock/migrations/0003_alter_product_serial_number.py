# Generated by Django 4.2.1 on 2024-04-01 18:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_product_serial_number_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='serial_number',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]