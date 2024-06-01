from django.urls import reverse
from django.test import TestCase
from profiles.factories import ProfilesFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.member,cls.other_member=ProfilesFactory.create_batch(2)
        cls.admin,cls.other_admin=ProfilesFactory.create_batch(2,user__is_staff=True)

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