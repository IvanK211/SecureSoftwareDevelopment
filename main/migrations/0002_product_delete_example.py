# Generated by Django 4.1.7 on 2023-04-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_type', models.CharField(max_length=25)),
                ('product_description', models.TextField()),
                ('affiliate_url', models.SlugField(blank=True, null=True)),
                ('product_image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='Example',
        ),
    ]
