# Generated by Django 3.2.9 on 2023-04-13 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_auto_20230315_0421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eachfavoritequestion',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterField(
            model_name='eachfavoritequestion',
            name='question',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='each_question', to='board.boardquestion'),
        ),
    ]
