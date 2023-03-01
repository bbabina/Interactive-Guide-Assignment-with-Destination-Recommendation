# Generated by Django 3.2.7 on 2023-02-27 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0018_alter_places_descrption'),
        ('registration', '0021_auto_20220307_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_guide',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='destination.places'),
        ),
    ]