# Generated by Django 4.2.10 on 2024-04-30 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=100)),
            ],
        ),
    ]
