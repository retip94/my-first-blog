# Generated by Django 2.2.5 on 2019-09-24 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='mail',
            new_name='email',
        ),
    ]
