from django.contrib import admin
from .models import Voter, Election, Candidate, Vote

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("voter_id", "name", "email", "status", "age", "created_at")
    search_fields = ("voter_id", "name", "email")
    list_filter = ("status", "gender")

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "party_name", "election", "status", "created_at")
    list_filter = ("status", "election")
    search_fields = ("name", "party_name")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("voter", "election", "candidate", "voted_at")
    list_filter = ("election",)
    search_fields = ("voter__voter_id", "candidate__name")
