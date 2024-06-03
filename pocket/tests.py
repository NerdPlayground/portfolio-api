from django.urls import reverse
from django.test import TestCase
from profiles.factories import ProfilesFactory
from projects.factories import ProjectsFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.admin=ProfilesFactory.create(user__is_staff=True)
        cls.admin_projects=ProjectsFactory.create_batch(2,user=cls.admin.user)
        cls.member,cls.other_member=ProfilesFactory.create_batch(2)
        cls.member_projects=ProjectsFactory.create_batch(2,user=cls.member.user)

    def member_login(self,member,password=None):
        password=password or self.password
        response=self.client.post(reverse("rest_login"),{
            "password":password,
            "email":member.user.email,
        })
        self.assertEqual(response.status_code,200)
        return response.json()

    def get_current_user(self):
        response=self.client.get(reverse("rest_user_details"))
        return response
    
    def project_data(self):
        print("name:",self.member_project.name)
        print("link:",self.member_project.link)
        print("start_date:",self.member_project.start_date)
        print("end_date:",self.member_project.end_date)
        print("ongoing:",self.member_project.ongoing)
        print("description:",self.member_project.description)
        print("objectives:",self.member_project.objectives)
        print("tools:",self.member_project.tools)