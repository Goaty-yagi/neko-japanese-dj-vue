# Generated by Django 3.2.9 on 2023-01-13 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20230112_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardquestion',
            name='on_best',
            field=models.BooleanField(default=False),
        ),
    ]
