# Generated by Django 4.2.7 on 2023-12-14 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_email_usercred_user_id'),
        ('notion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WidgetsTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_count', models.JSONField()),
                ('modified_at', models.DateTimeField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usercred', unique=True)),
            ],
        ),
    ]
