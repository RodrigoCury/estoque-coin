# Generated by Django 3.1.7 on 2021-03-30 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leveduras', '0004_auto_20210329_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fermentativeprofile',
            options={'ordering': ('name',), 'verbose_name': 'Perfil Fermentativo', 'verbose_name_plural': 'Perfis Fermentativos'},
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=50)),
                ('complete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ToDo',
                'verbose_name_plural': 'ToDos',
                'ordering': ('id',),
            },
        ),
    ]
