"""
Initial migration for reports app
"""
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportExport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('daily', 'Daily Emergencies'), ('weekly', 'Weekly Emergencies'), ('monthly', 'Monthly Emergencies'), ('user_activity', 'User Activity'), ('emergency_types', 'Emergency Type Stats'), ('police_stats', 'Police Notification Stats'), ('sms_stats', 'SMS Notification Stats'), ('video_stats', 'Video Session Stats')], max_length=50)),
                ('file_type', models.CharField(choices=[('csv', 'CSV'), ('pdf', 'PDF')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('record_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
        ),
    ]
