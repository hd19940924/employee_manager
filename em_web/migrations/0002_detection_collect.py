# Generated by Django 4.0.4 on 2023-05-24 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='detection_collect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, null=True)),
                ('url', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
