# Generated by Django 4.1.3 on 2022-12-16 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0016_alter_emprestimo_data_emprestimo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_devolucao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 9, 50, 54, 960531)),
        ),
    ]
