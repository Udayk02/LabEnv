# Generated by Django 4.1.3 on 2022-11-24 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_alter_answer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.CharField(default='ongoing', max_length=20),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=500)),
                ('option_one', models.CharField(blank=True, max_length=30)),
                ('option_two', models.CharField(blank=True, max_length=30)),
                ('option_three', models.CharField(blank=True, max_length=30)),
                ('option_four', models.CharField(blank=True, max_length=30)),
                ('option_five', models.CharField(blank=True, max_length=30)),
                ('option_one_count', models.IntegerField(default=-1)),
                ('option_two_count', models.IntegerField(default=-1)),
                ('option_three_count', models.IntegerField(default=-1)),
                ('option_four_count', models.IntegerField(default=-1)),
                ('option_five_count', models.IntegerField(default=-1)),
                ('assignment_in', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='lab.assignment')),
            ],
        ),
    ]