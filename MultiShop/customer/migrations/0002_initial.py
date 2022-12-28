# Generated by Django 4.1.4 on 2022-12-27 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.order'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.product'),
        ),
        migrations.AddField(
            model_name='ordercoupon',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.coupon'),
        ),
        migrations.AddField(
            model_name='ordercoupon',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='customer.order'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coupon',
            name='used_customers',
            field=models.ManyToManyField(blank=True, related_name='used_coupons', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='bascetitem',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.color'),
        ),
        migrations.AddField(
            model_name='bascetitem',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AddField(
            model_name='bascetitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product'),
        ),
        migrations.AddField(
            model_name='bascetitem',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.size'),
        ),
    ]