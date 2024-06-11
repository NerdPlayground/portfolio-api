import re
from .models import Profile
from django.core import mail
from django.urls import reverse
from knox.models import AuthToken
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

'''
TESTED ENDPOINTS:
- login and logout
- register user
- verify user email
- change user details
- delete user
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
    
    def verify_user_email(self,username):
        pattern="token: (?P<key>[-:\w]+)"
        key=re.search(pattern,mail.outbox[0].body).group("key")
        response=self.client.post(reverse("rest_verify_email"),{"key":key})
        self.assertEqual(response.status_code,200)

        current_user=get_user_model().objects.get(username=username)
        email_address=EmailAddress.objects.get(user=current_user)
        self.assertTrue(email_address.verified)

    def setup_profile_details(self,token,username,email,details):
        response=self.client.put(
            headers={"Authorization": f"Bearer {token}"},
            path=reverse("current-user"),
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
        email=f"{username}@gmail.com"
        response=self.client.post(reverse("rest_register"),{
            "username":username,
            "email":email,
            "password1":self.password,
            "password2":self.password,
        })
        self.assertEqual(response.status_code,204)
        self.assertEqual(len(mail.outbox),1)
        self.verify_user_email(username)

        profile=Profile.objects.last()
        token=self.member_login(profile,self.password)
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
        self.setup_profile_details(token,username,email,details)

        profile=Profile.objects.last()
        self.assertEqual(profile.user.username,username)
        self.assertEqual(profile.user.email,email)
        self.assertEqual(profile.user.first_name,details.get('first_name'))
        self.assertEqual(profile.user.last_name,details.get('last_name'))
        self.assertEqual(profile.bio,details.get('profile').get('bio'))
        self.assertEqual(profile.skills,details.get('profile').get('skills'))
        self.assertEqual(profile.socials,details.get('profile').get('socials'))

    def test_member_delete_account(self):
        token=self.member_login(self.member)
        total_members=Profile.objects.count()
        response=self.client.delete(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(Profile.objects.count(),total_members-1)

    def test_member_change_password(self):
        token=self.member_login(self.member)
        password="QWERTY23!@#"
        response=self.client.post(
            headers={"Authorization": f"Bearer {token}"},
            path=reverse("rest_password_change"),
            data={
                "old_password":self.password,
                "new_password1":password,
                "new_password2":password,
            }
        )
        self.assertEqual(response.status_code,200)

        logout_response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(logout_response.status_code,204)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)

    def test_member_password_reset(self):
        response=self.client.post(
            path=reverse("password_reset:reset-password-request"),
            data={"email":self.member.user.email},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(mail.outbox),1)

        pattern="Authentication Token: (?P<token>[\w]+)"
        token=re.search(pattern,mail.outbox[0].body).group("token")
        token_response=self.client.post(
            path=reverse("password_reset:reset-password-validate"),
            data={"token":token}
        )
        self.assertEqual(token_response.status_code,200)

        password="QWERTY23!@#"
        reset_response=self.client.post(
            path=reverse("password_reset:reset-password-confirm"),
            data={"token":token,"password":password,}
        )
        self.assertEqual(reset_response.status_code,200)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)
    
    def test_member_logout(self):
        token_counter=AuthToken.objects.count()
        token=self.member_login(self.member)
        self.assertEqual(AuthToken.objects.count(),token_counter+1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(AuthToken.objects.count(),token_counter)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def test_admin_access_all_users(self):
        token=self.member_login(self.admin)
        profile_count=Profile.objects.count()
        response=self.client.get(
            path=reverse("user-list"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),profile_count)
    
    def test_member_access_all_users(self):
        token=self.member_login(self.member)
        response=self.client.get(
            path=reverse("user-list"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,403)