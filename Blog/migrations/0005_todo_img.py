# Generated by Django 5.1.1 on 2024-12-24 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_alter_todo_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='img',
            field=models.ImageField(blank=True, default=False, null=True, upload_to='pics'),
        ),
    ]