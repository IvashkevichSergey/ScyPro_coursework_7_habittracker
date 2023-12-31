# Generated by Django 4.2.6 on 2023-10-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('where', models.CharField(max_length=25)),
                ('when', models.TimeField(null=True)),
                ('what', models.TextField()),
                ('how_long_seconds', models.PositiveIntegerField()),
                ('how_often_days', models.PositiveIntegerField(default=1)),
                ('is_enjoyable', models.BooleanField(default=False)),
                ('reward', models.TextField(null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
