# Generated by Django 4.0 on 2022-10-31 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_chat_message_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='chat.chat', verbose_name='Чат'),
        ),
    ]
