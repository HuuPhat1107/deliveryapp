# Generated by Django 4.0.4 on 2022-05-17 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryapp', '0003_alter_shipperreceiver_shipper'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_name',
            new_name='name',
        ),
    ]
