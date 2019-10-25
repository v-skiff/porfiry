# Generated by Django 2.2.6 on 2019-10-20 15:45

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]