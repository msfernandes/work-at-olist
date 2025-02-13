# Generated by Django 2.2.2 on 2019-06-14 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=11)),
                ('period', models.DateField()),
            ],
            options={
                'verbose_name': 'Bill',
                'verbose_name_plural': 'Bills',
                'unique_together': {('telephone', 'period')},
            },
        ),
        migrations.CreateModel(
            name='BillRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=11)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('duration', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='core.Bill')),
            ],
            options={
                'verbose_name': 'Bill Record',
                'verbose_name_plural': 'Bill Records',
            },
        ),
    ]
