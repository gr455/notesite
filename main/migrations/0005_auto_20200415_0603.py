# Generated by Django 3.0.5 on 2020-04-15 06:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200415_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_whenPublished',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published'),
        ),
    ]
