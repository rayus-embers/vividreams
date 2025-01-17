# Generated by Django 5.1.3 on 2024-11-30 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='facebook',
            field=models.URLField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='instagram',
            field=models.URLField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='channel',
            name='tiktok',
            field=models.URLField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='x',
            field=models.URLField(blank=True, max_length=80, null=True, verbose_name='Twitter/X'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='youtube',
            field=models.URLField(blank=True, max_length=80, null=True),
        ),
    ]
