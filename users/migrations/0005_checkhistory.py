# Generated by Django 4.2.20 on 2025-03-16 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_checkcounter_alter_table_check_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_number', models.PositiveIntegerField()),
                ('table_number', models.PositiveIntegerField()),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('opened_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
