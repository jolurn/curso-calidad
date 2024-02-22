# Generated by Django 4.1.7 on 2024-02-22 04:02

from django.db import migrations, models
import pfimapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pfimapp', '0002_alter_customuser_apellidomaterno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='apellidoMaterno',
            field=models.CharField(max_length=50, validators=[pfimapp.validators.validate_min_length_and_letters]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='apellidoPaterno',
            field=models.CharField(max_length=50, validators=[pfimapp.validators.validate_min_length_and_letters]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='correoUNI',
            field=models.EmailField(max_length=50, unique=True, validators=[pfimapp.validators.validate_min_length_correo]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Este correo electrónico ya está en uso.'}, max_length=50, unique=True, validators=[pfimapp.validators.validate_min_length_correo]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='fechaNacimiento',
            field=models.DateField(help_text='Formato: AAAA-MM-DD', validators=[pfimapp.validators.validate_past_date]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nacionalidad',
            field=models.CharField(max_length=20, validators=[pfimapp.validators.validate_min_length_and_letters]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='numeroDocumento',
            field=models.CharField(error_messages={'unique': 'Este número de documento ya está en uso.'}, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='numeroUbigeoNacimiento',
            field=models.CharField(help_text='Ingrese un número de 6 dígitos.', max_length=6, validators=[pfimapp.validators.validate_numeric_length]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='primerNombre',
            field=models.CharField(max_length=50, validators=[pfimapp.validators.validate_min_length_and_letters]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='segundoNombre',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[pfimapp.validators.validate_min_length_and_letters]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telefono',
            field=models.CharField(max_length=15, validators=[pfimapp.validators.validate_min_numeric_length]),
        ),
    ]
