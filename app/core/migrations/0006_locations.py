# Generated by Django 3.2.13 on 2022-06-09 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220608_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.clients')),
            ],
        ),
    ]