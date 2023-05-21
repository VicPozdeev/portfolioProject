# Generated by Django 4.1.7 on 2023-04-17 13:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('first_name', models.CharField(blank=True, max_length=35, null=True)),
                ('last_name', models.CharField(blank=True, max_length=35, null=True)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
                ('short_info', models.CharField(blank=True, max_length=100, null=True)),
                ('about_me', wagtail.fields.RichTextField(blank=True, null=True)),
                ('skills_top_text', models.TextField(blank=True, null=True)),
                ('contacts_cta', models.TextField(blank=True, null=True)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=70, null=True)),
                ('stars', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0)),
                ('figure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('portfolio', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='portfolio.portfoliopage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('account_path', models.CharField(blank=True, max_length=255, null=True)),
                ('portfolio', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_accounts', to='portfolio.portfoliopage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250, null=True)),
                ('figure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('portfolio', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='works', to='portfolio.portfoliopage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='HomePage',
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='social_button',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_buttons', to='portfolio.socialbutton'),
        ),
    ]
