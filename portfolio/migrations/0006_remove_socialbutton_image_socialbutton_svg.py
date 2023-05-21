# Generated by Django 4.1.7 on 2023-04-17 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_alter_socialbutton_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialbutton',
            name='image',
        ),
        migrations.AddField(
            model_name='socialbutton',
            name='svg',
            field=models.FileField(blank=True, null=True, upload_to='svg', validators=[django.core.validators.FileExtensionValidator(['svg'])]),
        ),
    ]
