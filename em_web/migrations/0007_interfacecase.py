# Generated by Django 4.0.4 on 2023-06-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em_web', '0006_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterfaceCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casetitle', models.CharField(max_length=30)),
                ('remethod', models.CharField(max_length=10)),
                ('reparameter', models.CharField(max_length=30)),
                ('parametertype', models.CharField(max_length=30)),
                ('readdr', models.CharField(max_length=30)),
                ('exresult', models.CharField(max_length=10)),
                ('acresult', models.CharField(max_length=10)),
            ],
        ),
    ]
