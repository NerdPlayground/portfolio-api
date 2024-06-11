from django.urls import reverse
from django.test import TestCase
from profiles.factories import ProfilesFactory
from projects.factories import ProjectsFactory
from experiences.factories import ExperiencesFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        
        cls.admin=ProfilesFactory.create(user__is_staff=True)
        cls.admin_projects=ProjectsFactory.create_batch(2,user=cls.admin.user)
        cls.admin_experiences=ExperiencesFactory.create_batch(2,user=cls.admin.user)

        cls.member,cls.other_member=ProfilesFactory.create_batch(2)
        cls.member_projects=ProjectsFactory.create_batch(2,user=cls.member.user)
        cls.member_experiences=ExperiencesFactory.create_batch(2,user=cls.member.user)

    def member_login(self,member,password=None):
        password=password or self.password
        response=self.client.post(reverse("knox_login"),{
            "password":password,
            "username":member.user.username,
        })
        self.assertEqual(response.status_code,200)
        return response.json().get("token")

    def get_current_user(self,token):
        response=self.client.get(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response