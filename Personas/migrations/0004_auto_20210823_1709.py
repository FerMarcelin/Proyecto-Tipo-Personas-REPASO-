# Generated by Django 3.1 on 2021-08-23 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0003_auto_20210823_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='Personas.persontype'),
        ),
    ]
