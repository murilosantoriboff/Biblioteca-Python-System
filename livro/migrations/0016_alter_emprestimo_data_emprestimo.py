# Generated by Django 4.1.3 on 2022-12-16 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0015_emprestimo_avalicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 9, 50, 16, 899797)),
        ),
    ]
