# Generated by Django 4.2.7 on 2023-11-14 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('campus', models.CharField(max_length=150, verbose_name='Campus')),
            ],
            options={
                'verbose_name': 'projeto',
                'verbose_name_plural': 'projetos',
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, verbose_name='Descrição')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor por hora')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scholarship.project', verbose_name='Projeto')),
                ('scholars', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Bolsistas')),
            ],
            options={
                'verbose_name': 'bolsa',
                'verbose_name_plural': 'bolsas',
            },
        ),
    ]