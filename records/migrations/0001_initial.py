# Generated by Django 4.2.7 on 2023-11-14 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, verbose_name='Descrição')),
                ('date', models.DateField(verbose_name='Data')),
                ('start', models.TimeField(verbose_name='Hora inicial')),
                ('end', models.TimeField(verbose_name='Hora final')),
                ('scholarship', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scholarship.scholarship', verbose_name='Projeto')),
                ('scholar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Bolsista')),
            ],
            options={
                'verbose_name': 'registro',
                'verbose_name_plural': 'registros',
            },
        ),
    ]
