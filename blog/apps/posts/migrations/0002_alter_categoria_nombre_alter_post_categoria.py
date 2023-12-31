# Generated by Django 5.0 on 2023-12-29 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(default='Sin categoría', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.categoria'),
        ),
    ]
