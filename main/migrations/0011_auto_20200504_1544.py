# Generated by Django 3.0.5 on 2020-05-04 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_auto_20200418_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_fileurl',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_note', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.Note', verbose_name='Note')),
                ('fav_user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Favourite')),
            ],
        ),
    ]