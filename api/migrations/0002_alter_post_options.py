# Generated by Django 4.1.2 on 2022-10-04 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['created'], 'permissions': (('can_post_blog', 'can post blog'),)},
        ),
    ]
