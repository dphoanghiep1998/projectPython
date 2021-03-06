# Generated by Django 3.1.3 on 2020-11-23 23:29

from django.db import migrations, models
import home.validators


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201123_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='imageBook',
            field=models.ImageField(blank=True, null=True, upload_to='image/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=models.FileField(upload_to='documents/%Y/%m/%d/', validators=[home.validators.validate_ContentChapter]),
        ),
    ]
