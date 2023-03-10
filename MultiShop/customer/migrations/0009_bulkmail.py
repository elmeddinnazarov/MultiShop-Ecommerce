# Generated by Django 4.1.4 on 2023-01-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_passwordreset_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('customers', models.ManyToManyField(to='customer.customer')),
            ],
        ),
    ]
