# Generated by Django 2.2.7 on 2019-11-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_admin', '0007_auto_20191123_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set(),
        ),
    ]