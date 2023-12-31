# Generated by Django 4.2.3 on 2023-10-14 10:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_useraccount_accountid_alter_useraccount_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactions',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
