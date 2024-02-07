# Generated by Django 4.2.9 on 2024-02-07 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Auction_listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('initial_bid', models.IntegerField()),
                ('current_bid', models.IntegerField()),
                ('listing_img', models.ImageField(null=True, upload_to='images/')),
                ('listing_title', models.CharField(max_length=150)),
                ('listing_category', models.CharField(max_length=150, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
