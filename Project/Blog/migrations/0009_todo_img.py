# Generated by Django 5.1.1 on 2024-12-27 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_delete_todoimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='img',
            field=models.ImageField(blank=True, default=False, null=True, upload_to='pics'),
        ),
    ]
