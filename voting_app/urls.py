from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.voter_login, name="voter_login"),
    path("register/", views.register, name="register"),
    path("logout/", views.voter_logout, name="voter_logout"),
    path("voter/dashboard/", views.voter_dashboard, name="voter_dashboard"),
    path("voter/profile/", views.voter_profile, name="voter_profile"),
    path("voter/candidates/<int:election_id>/", views.candidates, name="candidates"),
    path("voter/cast-vote/", views.cast_vote, name="cast_vote"),
    path("voter/success/", views.vote_success, name="vote_success"),
    path("voter/result/<int:election_id>/", views.result, name="result"),

    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/logout/", views.admin_logout, name="admin_logout"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/elections/", views.election_manage, name="election_manage"),
    path("admin/elections/create/", views.election_create, name="election_create"),
    path("admin/elections/<int:pk>/edit/", views.election_edit, name="election_edit"),
    path("admin/elections/<int:pk>/start/", views.election_start, name="election_start"),
    path("admin/elections/<int:pk>/stop/", views.election_stop, name="election_stop"),
    path("admin/elections/<int:pk>/delete/", views.election_delete, name="election_delete"),
    path("admin/candidates/", views.candidate_manage, name="candidate_manage"),
    path("admin/candidates/add/", views.candidate_add, name="candidate_add"),
    path("admin/candidates/<int:pk>/edit/", views.candidate_edit, name="candidate_edit"),
    path("admin/candidates/<int:pk>/toggle/", views.candidate_toggle, name="candidate_toggle"),
    path("admin/candidates/<int:pk>/delete/", views.candidate_delete, name="candidate_delete"),
    path("admin/voters/", views.voter_manage, name="voter_manage"),
    path("admin/voters/<int:pk>/toggle/", views.voter_toggle, name="voter_toggle"),
    path("admin/voters/<int:pk>/delete/", views.voter_delete, name="voter_delete"),
    path("admin/results/<int:election_id>/", views.admin_result, name="admin_result"),
]
