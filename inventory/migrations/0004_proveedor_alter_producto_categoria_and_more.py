# Generated by Django 5.1.4 on 2025-01-15 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_producto_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del proveedor')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico')),
            ],
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='inventory.categoria', verbose_name='Categoría'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='inventory.proveedor', verbose_name='Proveedor'),
        ),
    ]
