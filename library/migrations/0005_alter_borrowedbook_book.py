# Generated by Django 5.0.1 on 2024-02-02 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_borrowedbook_borrowed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_by', to='library.book', unique=True),
        ),
    ]
