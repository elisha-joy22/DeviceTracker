# Generated by Django 5.0.1 on 2024-01-04 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('took_at', models.DateTimeField(auto_now_add=True)),
                ('returned_at', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=models.SET('Device removed'), to='device.device')),
                ('user', models.ForeignKey(on_delete=models.SET('User removed'), to='accounts.customuser')),
            ],
        ),
    ]
