# Generated by Django 3.0.2 on 2020-01-10 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='description',
            field=models.TextField(default='Welcome!', max_length=1000, verbose_name='个性签名'),
        ),
    ]