# Generated by Django 3.2.9 on 2022-12-21 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='test_take_num',
            field=models.IntegerField(default=0),
        ),
    ]
