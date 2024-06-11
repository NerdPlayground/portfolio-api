from .models import Experience
from django.urls import reverse
from datetime import date,timedelta
from pocket.tests import PocketTestCase
from pocket.views import get_date_object

'''
TESTED ENDPOINTS:
- create experience
- list personal experiences
- list all experiences
- list all experiences (member)
- update experience
- update experience (intruder)
- delete experience
- delete experience (intruder)
- create and set end date past today
- update end date past today

UNTESTED ENDPOINTS:
'''

class ExperienceTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_member_create_experience(self):
        token=self.member_login(self.member)
        experiences=Experience.objects.count()
        data={
            "company":"Django Test Case",
            "title":"Experience in Test Case",
            "link":"http://127.0.0.1:8000/experience-in-test-case",
            "display":True,
            "start_date":"2024-01-01",
            "end_date":"2024-02-01",
            "description":"Experience created in Django Test Case",
            "objectives":[
                "Testing users apps",
                "Testing projects apps",
                "Testing experiences apps",
            ],
            "tools":["Python","Django","Django REST Framework"]
        }
        response=self.client.post(
            path=reverse("experience-list"),
            content_type="application/json",
            headers={"Authorization":f"Bearer {token}"},
            data=data,
        )
        self.assertEqual(response.status_code,201)
        self.assertEqual(Experience.objects.count(),experiences+1)

        experience=Experience.objects.last()
        self.assertEqual(experience.user,self.member.user)
        self.assertEqual(experience.company,data.get("company"))
        self.assertEqual(experience.title,data.get("title"))
        self.assertEqual(experience.link,data.get("link"))
        self.assertEqual(experience.display,data.get("display"))
        self.assertEqual(experience.start_date,get_date_object(data.get("start_date")))
        self.assertEqual(experience.end_date,get_date_object(data.get("end_date")))
        self.assertEqual(experience.description,data.get("description"))
        self.assertEqual(experience.objectives,data.get("objectives"))
        self.assertEqual(experience.tools,data.get("tools"))

    def test_member_get_experiences(self):
        token=self.member_login(self.member)
        experiences=Experience.objects.filter(user=self.member.user).count()
        response=self.client.get(
            path=reverse("experience-list"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),experiences)

    def test_admin_get_all_experiences(self):
        token=self.member_login(self.admin)
        experiences=Experience.objects.count()
        response=self.client.get(
            path=reverse("all-experiences"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),experiences)

    def test_member_get_all_experiences(self):
        token=self.member_login(self.member)
        response=self.client.get(
            path=reverse("all-experiences"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,403)

    def test_member_update_experience(self):
        token=self.member_login(self.member)
        experience=self.member_experiences[0]
        description="Experience updated in Django Test Case"
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":experience.start_date,
            "end_date":experience.end_date,
            "description":description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.put(
            path=reverse("experience-detail",kwargs={"pk":experience.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        self.assertEqual(response.status_code,200)

        upddated_experience=Experience.objects.get(id=experience.id)
        self.assertEqual(upddated_experience.description,description)

    def test_intruder_update_experience(self):
        token=self.member_login(self.other_member)
        experience=self.member_experiences[0]
        response=self.client.put(
            path=reverse("experience-detail",kwargs={"pk":experience.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data={},
        )
        self.assertEqual(response.status_code,403)

    def test_member_delete_experience(self):
        token=self.member_login(self.member)
        experiences=Experience.objects.count()
        experience=self.member_experiences[-1]
        response=self.client.delete(
            path=reverse("experience-detail",kwargs={"pk":experience.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(Experience.objects.count(),experiences-1)

    def test_intruder_delete_experience(self):
        token=self.member_login(self.other_member)
        experience=self.member_experiences[-1]
        response=self.client.delete(
            path=reverse("experience-detail",kwargs={"pk":experience.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code,403)

    def test_create_experience_with_future_end_date(self):
        token=self.member_login(self.member)
        start_date=date.today()
        end_date=start_date+timedelta(days=1)
        experience=self.member_experiences[0]
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":start_date,
            "end_date":end_date,
            "description":experience.description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.post(
            path=reverse("experience-list"),
            content_type="application/json",
            headers={"Authorization":f"Bearer {token}"},
            data=data,
        )
        self.assertEqual(response.status_code,201)
        
        experience=Experience.objects.last()
        self.assertTrue(experience.ongoing)
        self.assertIsNone(experience.end_date)

    def test_update_experience_with_future_end_date(self):
        token=self.member_login(self.member)
        experience=self.member_experiences[0]
        end_date=date.today()+timedelta(days=1)
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":experience.start_date,
            "end_date":end_date,
            "description":experience.description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.put(
            path=reverse("experience-detail",kwargs={"pk":experience.id}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        self.assertEqual(response.status_code,200)

        experience=Experience.objects.get(id=experience.id)
        self.assertTrue(experience.ongoing)
        self.assertIsNone(experience.end_date)
    
    def test_create_experience_without_end_date_and_ongoing(self):
        token=self.member_login(self.member)
        experience=self.member_experiences[0]
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":experience.start_date,
            "description":experience.description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.post(
            path=reverse("experience-list"),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        self.assertEqual(response.status_code,400)
    
    def test_create_experience_with_end_date_and_ongoing(self):
        token=self.member_login(self.member)
        experience=self.member_experiences[0]
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":experience.start_date,
            "end_date":experience.end_date,
            "ongoing":True,
            "description":experience.description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.post(
            path=reverse("experience-list"),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        self.assertEqual(response.status_code,400)
    
    def test_create_experience_with_end_date_ahead_of_start_date(self):
        token=self.member_login(self.member)
        experience=self.member_experiences[0]
        end_date=experience.start_date-timedelta(days=10)
        end_date_str=end_date.strftime("%Y-%m-%d")
        data={
            "company":experience.company,
            "title":experience.title,
            "link":experience.link,
            "display":experience.display,
            "start_date":experience.start_date,
            "end_date":end_date_str,
            "ongoing":experience.ongoing,
            "description":experience.description,
            "objectives":experience.objectives,
            "tools":experience.tools,
        }
        response=self.client.post(
            path=reverse("experience-list"),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        self.assertEqual(response.status_code,400)