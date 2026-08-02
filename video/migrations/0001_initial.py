"""
Initial migration for video app
"""
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
                ('meeting_url', models.URLField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('ended', 'Ended')], default='pending', max_length=20)),
                ('sos_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_sessions', to='sos.sosevent')),
            ],
        ),
    ]
