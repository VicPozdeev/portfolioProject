# Generated by Django 4.1.7 on 2023-04-17 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_rename_account_path_socialaccount_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfoliopage',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
