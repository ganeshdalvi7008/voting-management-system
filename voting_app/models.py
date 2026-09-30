from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password

class Voter(models.Model):
    STATUS_CHOICES = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    voter_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.voter_id} - {self.name}"

class Election(models.Model):
    STATUS_CHOICES = [
        ("UPCOMING", "UPCOMING"),
        ("ACTIVE", "ACTIVE"),
        ("COMPLETED", "COMPLETED"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="UPCOMING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    STATUS_CHOICES = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    name = models.CharField(max_length=100)
    party_name = models.CharField(max_length=100)
    party_symbol = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="candidates/", blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="candidates")
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.election.title}"

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name="votes")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["voter", "election"], name="unique_voter_election")
        ]
        ordering = ["-voted_at"]

    def __str__(self):
        return f"{self.voter.voter_id} -> {self.candidate.name}"
