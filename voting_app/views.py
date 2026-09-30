from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Voter, Election, Candidate, Vote
from .forms import VoterRegistrationForm, ElectionForm, CandidateForm
from .decorators import voter_required, staff_required

def home(request):
    active = Election.objects.filter(status="ACTIVE").order_by("end_date")
    return render(request, "voting_app/index.html", {"active_elections": active})

def register(request):
    if request.method == "POST":
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect("voter_login")
    else:
        form = VoterRegistrationForm()
    return render(request, "voting_app/register.html", {"form": form})

def voter_login(request):
    if request.session.get("voter_id"):
        return redirect("voter_dashboard")
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        password = request.POST.get("password", "")
        voter = Voter.objects.filter(Q(voter_id=identifier) | Q(email=identifier)).first()
        if voter and voter.status == "ACTIVE" and voter.check_password(password):
            request.session["voter_id"] = voter.id
            return redirect("voter_dashboard")
        messages.error(request, "Invalid credentials or inactive voter.")
    return render(request, "voting_app/login.html")

def voter_logout(request):
    request.session.pop("voter_id", None)
    return redirect("home")

@voter_required
def voter_dashboard(request):
    voter = get_object_or_404(Voter, id=request.session["voter_id"])
    elections = Election.objects.order_by("-created_at")
    voted_ids = set(Vote.objects.filter(voter=voter).values_list("election_id", flat=True))
    return render(request, "voting_app/voter/dashboard.html", {"voter": voter, "elections": elections, "voted_ids": voted_ids})

@voter_required
def voter_profile(request):
    voter = get_object_or_404(Voter, id=request.session["voter_id"])
    return render(request, "voting_app/voter/profile.html", {"voter": voter})

@voter_required
def candidates(request, election_id):
    voter = get_object_or_404(Voter, id=request.session["voter_id"])
    election = get_object_or_404(Election, id=election_id)
    if election.status != "ACTIVE":
        messages.error(request, "Voting is allowed only for an ACTIVE election.")
        return redirect("voter_dashboard")
    if Vote.objects.filter(voter=voter, election=election).exists():
        messages.error(request, "You have already voted in this election.")
        return redirect("voter_dashboard")
    candidates = Candidate.objects.filter(election=election, status="ACTIVE").order_by("name")
    return render(request, "voting_app/voter/candidates.html", {"election": election, "candidates": candidates})

@voter_required
@transaction.atomic
def cast_vote(request):
    if request.method != "POST":
        return redirect("voter_dashboard")
    voter = get_object_or_404(Voter, id=request.session["voter_id"])
    election = get_object_or_404(Election, id=request.POST.get("election_id"))
    candidate = get_object_or_404(Candidate, id=request.POST.get("candidate_id"), election=election)
    if election.status != "ACTIVE" or candidate.status != "ACTIVE":
        messages.error(request, "This ballot is no longer available.")
        return redirect("voter_dashboard")
    if Vote.objects.filter(voter=voter, election=election).exists():
        messages.error(request, "You have already voted in this election.")
        return redirect("voter_dashboard")
    try:
        Vote.objects.create(voter=voter, election=election, candidate=candidate)
    except IntegrityError:
        messages.error(request, "You have already voted in this election.")
        return redirect("voter_dashboard")
    request.session["vote_cast_success"] = True
    return redirect("vote_success")

@voter_required
def vote_success(request):
    if not request.session.pop("vote_cast_success", False):
        return redirect("voter_dashboard")
    return render(request, "voting_app/voter/vote_success.html")

def _result_context(election):
    candidates = Candidate.objects.filter(election=election).annotate(vote_count=Count("votes")).order_by("-vote_count", "name")
    total_votes = Vote.objects.filter(election=election).count()
    max_votes = candidates.first().vote_count if candidates else 0
    tied = [c for c in candidates if c.vote_count == max_votes and max_votes > 0]
    return {"election": election, "results": candidates, "total_votes": total_votes, "tied": tied}

@voter_required
def result(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    if election.status != "COMPLETED":
        messages.error(request, "Results are available only for completed elections.")
        return redirect("voter_dashboard")
    return render(request, "voting_app/voter/result.html", _result_context(election))

# ---------- Admin / staff ----------
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Invalid admin credentials.")
    return render(request, "voting_app/admin/login.html")

def admin_logout(request):
    logout(request)
    return redirect("home")

@staff_required
def admin_dashboard(request):
    context = {
        "voters_count": Voter.objects.count(),
        "candidates_count": Candidate.objects.count(),
        "elections_count": Election.objects.count(),
        "votes_count": Vote.objects.count(),
        "running_elections": Election.objects.filter(status="ACTIVE"),
    }
    return render(request, "voting_app/admin/dashboard.html", context)

@staff_required
def election_manage(request):
    return render(request, "voting_app/admin/elections.html", {"elections": Election.objects.order_by("-created_at")})

@staff_required
def election_create(request):
    form = ElectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Election created successfully.")
        return redirect("election_manage")
    return render(request, "voting_app/admin/election_form.html", {"form": form, "title": "Create Election"})

@staff_required
def election_edit(request, pk):
    obj = get_object_or_404(Election, pk=pk)
    form = ElectionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Election updated successfully.")
        return redirect("election_manage")
    return render(request, "voting_app/admin/election_form.html", {"form": form, "title": "Edit Election"})

@staff_required
def election_start(request, pk):
    obj = get_object_or_404(Election, pk=pk)
    obj.status = "ACTIVE"; obj.save(update_fields=["status"])
    messages.success(request, "Election started.")
    return redirect("election_manage")

@staff_required
def election_stop(request, pk):
    obj = get_object_or_404(Election, pk=pk)
    obj.status = "COMPLETED"; obj.save(update_fields=["status"])
    messages.success(request, "Election completed.")
    return redirect("election_manage")

@staff_required
def election_delete(request, pk):
    obj = get_object_or_404(Election, pk=pk)
    obj.delete()
    messages.success(request, "Election deleted.")
    return redirect("election_manage")

@staff_required
def candidate_manage(request):
    election_id = request.GET.get("election_id")
    qs = Candidate.objects.select_related("election").order_by("election__title", "name")
    if election_id:
        qs = qs.filter(election_id=election_id)
    return render(request, "voting_app/admin/candidates.html", {"candidates": qs, "elections": Election.objects.all(), "selected": election_id})

@staff_required
def candidate_add(request):
    form = CandidateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(); messages.success(request, "Candidate added."); return redirect("candidate_manage")
    return render(request, "voting_app/admin/candidate_form.html", {"form": form, "title": "Add Candidate"})

@staff_required
def candidate_edit(request, pk):
    obj = get_object_or_404(Candidate, pk=pk)
    form = CandidateForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, "Candidate updated."); return redirect("candidate_manage")
    return render(request, "voting_app/admin/candidate_form.html", {"form": form, "title": "Edit Candidate"})

@staff_required
def candidate_toggle(request, pk):
    obj = get_object_or_404(Candidate, pk=pk)
    obj.status = "INACTIVE" if obj.status == "ACTIVE" else "ACTIVE"; obj.save(update_fields=["status"])
    return redirect("candidate_manage")

@staff_required
def candidate_delete(request, pk):
    get_object_or_404(Candidate, pk=pk).delete()
    messages.success(request, "Candidate deleted.")
    return redirect("candidate_manage")

@staff_required
def voter_manage(request):
    search = request.GET.get("search", "").strip()
    voters = Voter.objects.all().order_by("-created_at")
    if search:
        voters = voters.filter(Q(name__icontains=search) | Q(email__icontains=search) | Q(voter_id__icontains=search))
    return render(request, "voting_app/admin/voters.html", {"voters": voters, "search": search})

@staff_required
def voter_toggle(request, pk):
    obj = get_object_or_404(Voter, pk=pk)
    obj.status = "INACTIVE" if obj.status == "ACTIVE" else "ACTIVE"; obj.save(update_fields=["status"])
    return redirect("voter_manage")

@staff_required
def voter_delete(request, pk):
    get_object_or_404(Voter, pk=pk).delete()
    messages.success(request, "Voter deleted.")
    return redirect("voter_manage")

@staff_required
def admin_result(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    return render(request, "voting_app/voter/result.html", _result_context(election))
