# Generated by Django 3.1.7 on 2021-03-29 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('leveduras', '0002_remove_yeast_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=50, verbose_name='Atividade')),
                ('content_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Atividade',
                'verbose_name_plural': 'Atividades',
                'ordering': ('-created_at',),
            },
        ),
    ]
