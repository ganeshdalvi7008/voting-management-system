from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import date
from voting_app.models import Voter, Election, Candidate, Vote

class Command(BaseCommand):
    help = "Create demo data matching the original PHP project."

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username="admin")
        admin.email = "admin@voting.com"; admin.is_staff = True; admin.is_superuser = True
        admin.set_password("admin123"); admin.save()

        voters = [
            ("VOTER001","Rahul Sharma","rahul@example.com","9876543210",date(2000,1,15),26,"Male","123, Main Street, Delhi"),
            ("VOTER002","Priya Patel","priya@example.com","9876543211",date(1998,5,20),28,"Female","456, Park Avenue, Mumbai"),
            ("VOTER003","Amit Verma","amit@example.com","9876543212",date(2002,11,5),23,"Male","789, Residency Road, Bangalore"),
        ]
        for vid,name,email,mobile,dob,age,gender,address in voters:
            Voter.objects.update_or_create(voter_id=vid, defaults={
                "name":name,"email":email,"password":make_password("voter123"),
                "mobile":mobile,"dob":dob,"age":age,"gender":gender,"address":address,"status":"ACTIVE"
            })

        e2,_=Election.objects.get_or_create(title="National General Election 2026", defaults={
            "description":"Demo active election.","start_date":date(2026,8,20),"end_date":date(2026,8,30),"status":"ACTIVE"
        })
        e3,_=Election.objects.get_or_create(title="Local Municipal Election 2026", defaults={
            "description":"Demo completed election.","start_date":date(2026,8,1),"end_date":date(2026,8,5),"status":"COMPLETED"
        })
        candidates=[
            ("Amit Shah","Democratic Alliance","Star",e2,"Focusing on community welfare, clean energy, and better public transit."),
            ("Priya Das","Progressive Coalition","Sun",e2,"Advocating for student support programs, job opportunities, and technical education."),
            ("Vikram Malhotra","Independent Voice","Shield",e2,"Dedicated to local development, security improvements, and transparency."),
            ("Ravi Kumar","Development First Party","Gear",e3,"Improving street lights, road sanitation, and neighborhood parks."),
            ("Sonal Mehta","Green City Initiative","Leaf",e3,"Focused on waste management and planting trees."),
        ]
        for name,party,symbol,election,desc in candidates:
            Candidate.objects.get_or_create(name=name,election=election,defaults={
                "party_name":party,"party_symbol":symbol,"description":desc,"status":"ACTIVE"
            })
        r=Voter.objects.get(voter_id="VOTER001"); p=Voter.objects.get(voter_id="VOTER002"); a=Voter.objects.get(voter_id="VOTER003")
        r_candidate=Candidate.objects.get(name="Ravi Kumar",election=e3)
        s_candidate=Candidate.objects.get(name="Sonal Mehta",election=e3)
        for voter,cand in [(r,r_candidate),(p,s_candidate),(a,r_candidate)]:
            Vote.objects.get_or_create(voter=voter,election=e3,defaults={"candidate":cand})
        self.stdout.write(self.style.SUCCESS("Demo data ready. Admin: admin / admin123; Voters: VOTER001..003 / voter123"))
