# Generated by Django 2.2.6 on 2019-10-03 13:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='code',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
    ]
