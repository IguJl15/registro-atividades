# Generated by Django 4.2.7 on 2023-12-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0003_alter_scholarship_options_alter_scholarship_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='max_hours',
            field=models.IntegerField(default='40', verbose_name='horas mensais'),
            preserve_default=False,
        ),
    ]
