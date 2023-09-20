# Generated by Django 4.2.5 on 2023-09-20 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0006_reportcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportcard',
            name='date_of_report_card_generation',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='reportcard',
            unique_together={('student_rank', 'date_of_report_card_generation')},
        ),
    ]