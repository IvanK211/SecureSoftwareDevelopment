# Generated by Django 4.1.7 on 2023-04-22 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Performance', models.IntegerField(default=0)),
                ('Quality', models.IntegerField(default=0)),
                ('Price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.profile')),
            ],
        ),
    ]