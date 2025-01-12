# Generated by Django 5.0.7 on 2024-07-22 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='traveldetails',
            name='drop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='travel_details_by_drop', to='api.location'),
        ),
        migrations.AlterField(
            model_name='traveldetails',
            name='pickup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='travel_details_by_pickup', to='api.location'),
        ),
    ]
