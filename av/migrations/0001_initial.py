# Generated by Django 2.0.4 on 2018-04-15 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='Defines the id.', primary_key=True, serialize=False)),
                ('folder_id', models.CharField(blank=True, help_text='Defines the folder id of user', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='updation time')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='folder', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'drive directories',
                'db_table': 'folders',
                'get_latest_by': 'created_at',
            },
        ),
    ]
