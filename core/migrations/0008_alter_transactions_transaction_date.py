# Generated by Django 4.2.3 on 2023-10-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_transactions_transaction_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
