# Generated by Django 3.2.9 on 2023-04-16 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_alter_quiztaker_test_take_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.CharField(default='', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='quiztaker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_taker', to='user.user'),
        ),
    ]