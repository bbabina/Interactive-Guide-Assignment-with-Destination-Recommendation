# Generated by Django 3.2.11 on 2022-01-21 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratinghome', '0004_rename_tags_rateinfo_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rateinfo',
            old_name='tag',
            new_name='tag_title',
        ),
    ]