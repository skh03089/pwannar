# Generated by Django 2.0.1 on 2018-02-09 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='due',
            field=models.DateTimeField(verbose_name='마감 기한'),
        ),
    ]
