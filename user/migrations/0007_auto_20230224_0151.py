# Generated by Django 3.2.9 on 2023-02-24 01:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_sns_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='UID',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
