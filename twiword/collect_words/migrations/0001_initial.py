# Generated by Django 2.1.4 on 2019-01-10 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenName', models.CharField(max_length=50)),
                ('userId', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.CharField(max_length=200)),
                ('word', models.CharField(max_length=200)),
                ('trans', models.CharField(max_length=200)),
                ('category', models.IntegerField(default=0)),
                ('quiz', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collect_words.Users')),
            ],
        ),
    ]