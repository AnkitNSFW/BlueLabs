# Generated by Django 4.2.7 on 2024-01-11 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_notes_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='user_id',
        ),
    ]
