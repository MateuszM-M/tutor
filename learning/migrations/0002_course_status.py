# Generated by Django 4.1.7 on 2023-04-03 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft')], default='Published', max_length=10),
        ),
    ]
