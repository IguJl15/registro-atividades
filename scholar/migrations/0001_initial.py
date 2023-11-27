# Generated by Django 4.2.7 on 2023-11-25 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'bolsista',
                'verbose_name_plural': 'bolsistas',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ispb', models.CharField(max_length=10, verbose_name='ISPB')),
                ('code', models.IntegerField(null=True, verbose_name='Código')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Banco',
                'verbose_name_plural': 'Bancos',
            },
        ),
        migrations.CreateModel(
            name='Scholar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'bolsista',
                'verbose_name_plural': 'bolsistas',
            },
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rg', models.CharField(max_length=100, unique=True, verbose_name='RG')),
                ('phone', models.CharField(max_length=50, verbose_name='Telefone')),
                ('birthday', models.DateField(verbose_name='Nascimento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scholar.scholar')),
            ],
            options={
                'verbose_name': 'Dados pessoais',
                'verbose_name_plural': 'Dados pessoais',
            },
        ),
        migrations.CreateModel(
            name='InstitutionalSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(choices=[('0', 'Segunda-Feira'), ('1', 'Terça-Feira'), ('2', 'Quarta-Feira'), ('3', 'Quinta-Feira'), ('4', 'Sexta-Feira'), ('5', 'Sábado'), ('6', 'Domingo')], max_length=2)),
                ('start', models.TimeField(verbose_name='Hora inicial')),
                ('end', models.TimeField(verbose_name='Hora final')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholar.scholar')),
            ],
            options={
                'verbose_name': 'Horário Institucional',
                'verbose_name_plural': 'Horários Institucionais',
            },
        ),
        migrations.CreateModel(
            name='BankingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('CR', 'Corrente'), ('PP', 'Poupança')], max_length=2)),
                ('account_number', models.CharField(max_length=50)),
                ('agency_number', models.CharField(max_length=10)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scholar.bank', verbose_name='Banco')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scholar.scholar')),
            ],
            options={
                'verbose_name': 'Dados bancários',
                'verbose_name_plural': 'Dados bancários',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(max_length=8, verbose_name='CEP')),
                ('street', models.CharField(max_length=250, verbose_name='Logradouro')),
                ('number', models.CharField(max_length=10, verbose_name='Nº')),
                ('state', models.CharField(max_length=250, verbose_name='Estado')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scholar.scholar')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
    ]