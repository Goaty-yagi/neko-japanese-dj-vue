# Generated by Django 3.2.9 on 2023-01-24 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_remove_boardquestion_on_best'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardusertag',
            options={'ordering': ['-total_num']},
        ),
    ]