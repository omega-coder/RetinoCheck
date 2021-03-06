# Generated by Django 2.1.15 on 2020-08-08 03:16

import app.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DRModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('model_type', models.PositiveIntegerField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestImage',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(upload_to=app.models.f)),
                ('pred_class', models.PositiveIntegerField()),
                ('preds', models.CharField(max_length=255, null=True)),
                ('uploaded_at', models.DateTimeField(default=datetime.datetime.now)),
                ('real_label', models.PositiveIntegerField()),
                ('eye_orientation', models.CharField(choices=[('L', 'LEFT'), ('R', 'RIGHT')], default=None, max_length=1, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
