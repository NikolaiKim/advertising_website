# Generated by Django 4.2.5 on 2023-09-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='активный'),
        ),
    ]
