# Generated by Django 3.2.9 on 2023-01-13 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_boardquestion_on_best'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardanswer',
            name='on_best',
            field=models.BooleanField(default=False),
        ),
    ]
