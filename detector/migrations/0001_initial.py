# Generated by Django 5.2 on 2025-05-18 21:11

import detector.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nodes.node')),
            ],
        ),
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('detected', models.BooleanField()),
                ('confidence', models.FloatField()),
                ('output', models.ImageField(upload_to=detector.models.output_path)),
                ('input', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='detector.imagefile')),
            ],
        ),
    ]
