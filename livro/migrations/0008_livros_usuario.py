# Generated by Django 4.1.3 on 2022-11-30 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('livro', '0007_categoria_livros_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='livros',
            name='usuario',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.DO_NOTHING, to='usuarios.usuario'),
            preserve_default=False,
        ),
    ]
