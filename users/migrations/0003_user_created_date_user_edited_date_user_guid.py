# Generated by Django 4.1.4 on 2023-03-03 11:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='edited_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
