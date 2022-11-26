# Generated by Django 4.0 on 2022-10-31 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='message',
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='chat.chat', verbose_name='Чат'),
            preserve_default=False,
        ),
    ]
