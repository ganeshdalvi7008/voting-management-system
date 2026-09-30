from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Election",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("status", models.CharField(choices=[("UPCOMING","UPCOMING"),("ACTIVE","ACTIVE"),("COMPLETED","COMPLETED")], default="UPCOMING", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Voter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("voter_id", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=128)),
                ("mobile", models.CharField(max_length=20)),
                ("dob", models.DateField()),
                ("age", models.PositiveIntegerField()),
                ("gender", models.CharField(choices=[("Male","Male"),("Female","Female"),("Other","Other")], max_length=10)),
                ("address", models.TextField()),
                ("status", models.CharField(choices=[("ACTIVE","ACTIVE"),("INACTIVE","INACTIVE")], default="ACTIVE", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("party_name", models.CharField(max_length=100)),
                ("party_symbol", models.CharField(max_length=100)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="candidates/")),
                ("description", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("ACTIVE","ACTIVE"),("INACTIVE","INACTIVE")], default="ACTIVE", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("election", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="candidates", to="voting_app.election")),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("voted_at", models.DateTimeField(auto_now_add=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="voting_app.candidate")),
                ("election", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="voting_app.election")),
                ("voter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="voting_app.voter")),
            ],
            options={"ordering":["-voted_at"]},
        ),
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(fields=("voter","election"), name="unique_voter_election"),
        ),
    ]
