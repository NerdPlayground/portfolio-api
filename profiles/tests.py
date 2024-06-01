import re
from .models import Profile
from django.core import mail
from django.urls import reverse
from pocket.tests import PocketTestCase
from rest_framework.authtoken.models import Token

'''
TESTED ENDPOINTS:
- login and logout
- register user
- verify user email
- change user details
- change user details (intruder)
- delete user
- delete user (intruder)
- change password
- reset password
- admin access all users
- member access all users

UNTESTED ENDPOINTS:
'''

class ProfilesTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def verify_user_email(self):
        pattern='http://testserver/api/v1/dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/'
        key=re.search(pattern,mail.outbox[0].body).group("key")
        response=self.client.post(reverse("rest_verify_email"),{"key":key})
        self.assertEqual(response.status_code,200)

    def setup_profile_details(self,username,email,details):
        response=self.client.put(
            path=reverse("user-detail",kwargs={"username":username}),
            content_type="application/json",
            data={
                'username':username,'email':email,
                'first_name':details.get('first_name'),
                'last_name':details.get('last_name'),
                'profile':details.get('profile'),
            }
        )
        self.assertEqual(response.status_code,200)

    def test_member_registration(self):
        username="dorobu"
        email="{}@gmail.com".format(username)
        response=self.client.post(reverse("rest_register"),{
            "username":username,
            "email":email,
            "password1":self.password,
            "password2":self.password,
        })
        self.assertEqual(response.status_code,204)
        self.assertEqual(len(mail.outbox),1)
        self.verify_user_email()

        details={
            "first_name":"George",
            "last_name":"Mobisa",
            "profile":{
                "bio": "Profile bio",
                "skills": ["skill-01","skill-02","skill-03"],
                "socials": {
                    "social-01":"http://127.0.0.1:8000/",
                    "social-02":"http://127.0.0.1:8000/",
                    "social-03":"http://127.0.0.1:8000/"
                }
            }
        }
        self.setup_profile_details(username,email,details)

        profile=Profile.objects.last()
        self.assertEqual(profile.user.username,username)
        self.assertEqual(profile.user.email,email)
        self.assertEqual(profile.user.first_name,details.get('first_name'))
        self.assertEqual(profile.user.last_name,details.get('last_name'))
        self.assertEqual(profile.bio,details.get('profile').get('bio'))
        self.assertEqual(profile.skills,details.get('profile').get('skills'))
        self.assertEqual(profile.socials,details.get('profile').get('socials'))


    def test_intruder_change_information(self):
        self.member_login(self.other_member)
        response=self.client.put(reverse(
            "user-detail",
            kwargs={"username":self.member.user.username}
        ))
        self.assertEqual(response.status_code,403)

    def test_member_delete_account(self):
        self.member_login(self.member)
        total_members=Profile.objects.count()
        response=self.client.delete(reverse(
            "user-detail",
            kwargs={"username":self.member.user.username}
        ))
        self.assertEqual(response.status_code,204)
        self.assertEqual(Profile.objects.count(),total_members-1)

    def test_intruder_delete_account(self):
        self.member_login(self.other_member)
        response=self.client.delete(reverse(
            "user-detail",
            kwargs={"username":self.member.user.username}
        ))
        self.assertEqual(response.status_code,403)

    def test_member_change_password(self):
        self.member_login(self.member)
        password="QWERTY23!@#"
        response=self.client.post(reverse("rest_password_change"),{
            "old_password":self.password,
            "new_password1":password,
            "new_password2":password,
        })
        self.assertEqual(response.status_code,200)

        user_response=self.get_current_user()
        self.assertEqual(user_response.status_code,403)
        
        login_response=self.member_login(self.member,password)
        self.assertIn("key",login_response)

    def test_member_password_reset(self):
        self.member_login(self.member)
        response=self.client.post(
            reverse('password_reset:reset-password-request'),
            {"email":self.member.user.email}
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(mail.outbox),1)

        pattern="Authentication Token: (?P<token>[\w]+)"
        token=re.search(pattern,mail.outbox[0].body).group("token")
        token_response=self.client.post(
            reverse("password_reset:reset-password-validate"),
            {"token":token}
        )
        self.assertEqual(token_response.status_code,200)

        password="QWERTY23!@#"
        reset_response=self.client.post(
            reverse('password_reset:reset-password-confirm'),
            {"token":token,"password":password,}
        )
        self.assertEqual(reset_response.status_code,200)

        user_response=self.get_current_user()
        self.assertEqual(user_response.status_code,403)
        
        login_response=self.member_login(self.member,password)
        self.assertIn("key",login_response)
    
    def test_member_logout(self):
        token_counter=Token.objects.count()
        self.member_login(self.member)
        self.assertEqual(Token.objects.count(),token_counter+1)

        user_response=self.get_current_user()
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(reverse("rest_logout"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(Token.objects.count(),token_counter)

        user_response=self.get_current_user()
        self.assertEqual(user_response.status_code,403)
    
    def test_admin_access_all_users(self):
        self.member_login(self.admin)
        profile_count=Profile.objects.count()
        response=self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),profile_count)
    
    def test_member_access_all_users(self):
        self.member_login(self.member)
        response=self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code,403)