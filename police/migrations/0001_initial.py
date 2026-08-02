"""
Initial migration for police app
"""
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PoliceStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('place_id', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=80, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PoliceNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payload', models.TextField(blank=True, help_text='JSON payload sent to police or notes')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('acknowledged', 'Acknowledged'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('response', models.TextField(blank=True, null=True)),
                ('notified_at', models.DateTimeField(auto_now_add=True)),
                ('police_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='police.policestation')),
                ('sos_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='police_notifications', to='sos.sosevent')),
            ],
        ),
    ]
