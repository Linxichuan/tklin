# Generated by Django 2.0.7 on 2019-09-30 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=64, unique=True)),
                ('sex', models.BooleanField(default=False)),
                ('icon', models.ImageField(upload_to='icons')),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'axf_users',
            },
        ),
    ]
