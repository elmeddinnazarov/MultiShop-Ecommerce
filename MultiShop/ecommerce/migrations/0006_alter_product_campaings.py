# Generated by Django 4.1.4 on 2023-01-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_alter_product_campaings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='campaings',
            field=models.ManyToManyField(blank=True, null=True, to='ecommerce.campaing'),
        ),
    ]