# Generated by Django 4.1.7 on 2023-04-17 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_remove_socialbutton_image_socialbutton_svg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialaccount',
            old_name='account_path',
            new_name='account',
        ),
    ]