from datetime import date,timedelta
from .models import Project
from django.urls import reverse
from .factories import ProjectsFactory
from pocket.tests import PocketTestCase
from pocket.views import get_date_object

'''
TESTED ENDPOINTS:
- create project
- list personal projects
- list all projects
- list all projects (member)
- update project
- update project (intruder)
- delete project
- delete project (intruder)
- create and set end date past today
- update end date past today

UNTESTED ENDPOINTS:
'''

class ProjectTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_member_create_project(self):
        self.member_login(self.member)
        projects=Project.objects.count()
        data={
            "name":"Project in Test Case",
            "link":"http://127.0.0.1:8000/project-in-test-case",
            "start_date":"2024-01-01",
            "end_date":"2024-02-01",
            "description":"Project created in Django Test Case",
            "objectives":[
                "Testing user apps",
                "Testing projects apps",
                "Testing experience apps",
            ],
            "tools":["Python","Django","Django REST Framework"]
        }
        response=self.client.post(
            path=reverse("project-list"),
            data=data,content_type="application/json",
        )
        self.assertEqual(response.status_code,201)
        self.assertEqual(Project.objects.count(),projects+1)

        project=Project.objects.last()
        self.assertEqual(project.user,self.member.user)
        self.assertEqual(project.name,data.get("name"))
        self.assertEqual(project.link,data.get("link"))
        self.assertEqual(project.start_date,get_date_object(data.get("start_date")))
        self.assertEqual(project.end_date,get_date_object(data.get("end_date")))
        self.assertEqual(project.description,data.get("description"))
        self.assertEqual(project.objectives,data.get("objectives"))
        self.assertEqual(project.tools,data.get("tools"))

    def test_member_get_projects(self):
        self.member_login(self.member)
        projects=Project.objects.filter(user=self.member.user).count()
        response=self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),projects)

    def test_admin_get_all_projects(self):
        self.member_login(self.admin)
        projects=Project.objects.count()
        response=self.client.get(reverse("all-projects"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),projects)

    def test_member_get_all_projects(self):
        self.member_login(self.member)
        response=self.client.get(reverse("all-projects"))
        self.assertEqual(response.status_code,403)

    def test_member_update_project(self):
        self.member_login(self.member)
        project=self.member_projects[0]
        description="Project updated in Django Test Case"
        data={
            "name":project.name,
            "link":project.link,
            "start_date":project.start_date,
            "end_date":project.end_date,
            "description":description,
            "objectives":project.objectives,
            "tools":project.tools,
        }
        response=self.client.put(
            path=reverse("project-detail",kwargs={"pk":project.id}),
            data=data,content_type="application/json",
        )
        self.assertEqual(response.status_code,200)

        upddated_project=Project.objects.get(id=project.id)
        self.assertEqual(upddated_project.description,description)

    def test_intruder_update_project(self):
        self.member_login(self.other_member)
        project=self.member_projects[0]
        response=self.client.put(
            path=reverse("project-detail",kwargs={"pk":project.id}),
            data={},content_type="application/json"
        )
        self.assertEqual(response.status_code,403)

    def test_member_delete_project(self):
        self.member_login(self.member)
        projects=Project.objects.count()
        project=self.member_projects[-1]
        response=self.client.delete(
            path=reverse("project-detail",kwargs={"pk":project.id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(Project.objects.count(),projects-1)

    def test_intruder_delete_project(self):
        self.member_login(self.other_member)
        project=self.member_projects[-1]
        response=self.client.delete(
            path=reverse("project-detail",kwargs={"pk":project.id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code,403)

    def test_create_project_with_future_end_date(self):
        self.member_login(self.member)
        start_date=date.today()
        end_date=start_date+timedelta(days=1)
        project=self.member_projects[0]
        data={
            "name":project.name,
            "link":project.link,
            "start_date":start_date,
            "end_date":end_date,
            "description":project.description,
            "objectives":project.objectives,
            "tools":project.tools,
        }
        response=self.client.post(
            path=reverse("project-list"),
            data=data,content_type="application/json"
        )
        self.assertEqual(response.status_code,201)
        
        project=Project.objects.last()
        self.assertTrue(project.ongoing)

    def test_update_project_with_future_end_date(self):
        self.member_login(self.member)
        project=self.member_projects[0]
        end_date=date.today()+timedelta(days=1)
        data={
            "name":project.name,
            "link":project.link,
            "start_date":project.start_date,
            "end_date":end_date,
            "description":project.description,
            "objectives":project.objectives,
            "tools":project.tools,
        }
        response=self.client.put(
            path=reverse("project-detail",kwargs={"pk":project.id}),
            data=data,content_type="application/json"
        )
        self.assertEqual(response.status_code,200)

        project=Project.objects.get(id=project.id)
        self.assertTrue(project.ongoing)