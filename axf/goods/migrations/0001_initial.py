# Generated by Django 2.0.7 on 2019-09-30 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.CharField(max_length=16)),
                ('typename', models.CharField(max_length=100)),
                ('childtypenames', models.CharField(max_length=200)),
                ('typesort', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_foodtypes',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(max_length=16)),
                ('productimg', models.CharField(max_length=200)),
                ('productname', models.CharField(max_length=100)),
                ('productlongname', models.CharField(max_length=200)),
                ('isxf', models.IntegerField(default=1)),
                ('pmdesc', models.CharField(max_length=100)),
                ('specifics', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('marketprice', models.FloatField(default=1)),
                ('categoryid', models.CharField(max_length=16)),
                ('childcid', models.CharField(max_length=16)),
                ('childcidname', models.CharField(max_length=100)),
                ('dealerid', models.CharField(max_length=16)),
                ('storenums', models.IntegerField(default=1)),
                ('productnum', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_goods',
            },
        ),
        migrations.CreateModel(
            name='MainNav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_nav',
            },
        ),
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
                ('categoryid', models.CharField(max_length=16)),
                ('brandname', models.CharField(max_length=100)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.CharField(max_length=16)),
                ('productid1', models.CharField(max_length=16)),
                ('longname1', models.CharField(max_length=100)),
                ('price1', models.FloatField(default=0)),
                ('marketprice1', models.FloatField(default=1)),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.CharField(max_length=16)),
                ('productid2', models.CharField(max_length=16)),
                ('longname2', models.CharField(max_length=100)),
                ('price2', models.FloatField(default=0)),
                ('marketprice2', models.FloatField(default=1)),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.CharField(max_length=16)),
                ('productid3', models.CharField(max_length=16)),
                ('longname3', models.CharField(max_length=100)),
                ('price3', models.FloatField(default=0)),
                ('marketprice3', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
        migrations.CreateModel(
            name='MainWheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_wheel',
            },
        ),
    ]
