# Generated by Django 4.1.7 on 2023-03-11 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]