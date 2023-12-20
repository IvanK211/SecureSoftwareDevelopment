# Generated by Django 4.1.7 on 2023-04-23 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_price_vote_pricing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='Performance',
            new_name='comfort',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='Pricing',
            new_name='durability',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='Quality',
            new_name='performance',
        ),
        migrations.AddField(
            model_name='product',
            name='comfort_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='product',
            name='durability_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='product',
            name='performance_average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='vote',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]