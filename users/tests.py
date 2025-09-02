from django.contrib.auth import get_user
from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse

from users.forms import CustomUserCreationForm


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        form_data = {
            'username': 'jakhongir',
            'first_name': 'Jakhongir',
            'last_name': 'Xojayev',
            'email': 'jakhongir@example.com',
            'password1': 'mystrongpassword123',
            'password2': 'mystrongpassword123',
        }

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()

        # Check that user exists in DB
        self.assertTrue(CustomUser.objects.filter(username='jakhongir').exists())

        # Check user info
        user = CustomUser.objects.get(username='jakhongir')
        self.assertEqual(user.email, 'jakhongir@example.com')

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Jakhongir",
                "email": "jrahmonov@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.assertFormError(response.context["form"], "password1", "This field is required.")

    def test_passwords_do_not_match(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password456',  # farqli
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_username_already_exists(self):
        CustomUser.objects.create_user(username='existinguser', password='password123')

        form_data = {
            'username': 'existinguser',  # mavjud
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'duplicate@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_email_required(self):
        form_data = {
            'username': 'noemailuser',
            'first_name': 'No',
            'last_name': 'Email',
            'email': '',  # email yo‘q
            'password1': 'password123',
            'password2': 'password123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_weak_password_rejected(self):
        form_data = {
            'username': 'weakpassword',
            'first_name': 'Weak',
            'last_name': 'Password',
            'email': 'weak@example.com',
            'password1': '123',  # juda kuchsiz
            'password2': '123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

class LoginTestCase(TestCase):
    def setUp(self):

        self.db_user = CustomUser.objects.create(username="jakhongir", first_name="Jakhongir")
        self.db_user.set_password("mystrongpassword123")
        self.db_user.save()

    def test_successfull_login(self):
        # db_user = User.objects.create_user(username="jakhongir",first_name="Jakhongir")
        # db_user.set_password('mystrongpassword123')
        # db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username":"jakhongir",
                "password":"mystrongpassword123"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        # db_user = User.objects.create(username='jakhongir',first_name='Jakhongir')
        # db_user.set_password('mystrongpassword123')
        # db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username":"wrong_username",
                "password":"mystrongpassword123"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        # db_user = User.objects.create(username="jakhongir", first_name="Jakhongir")
        # db_user.set_password("somepass")
        # db_user.save()

        self.client.login(username="jakhongir",password="mystrongpassword123")
        self.client.get(reverse("users:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov",email="jrahmonv2@gmail.com"
        )

        user.set_password("somepass")
        user.save()

        self.client.login(username="jakhongir", password="somepass")

        response = self.client.get(reverse("users:profile"))


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov",email="jrahmonv2@gmail.com"
        )

        user.set_password("somepass")
        user.save()
        self.client.login(username="jakhongir", password="somepass")
        response = self.client.post(reverse("users:profile-edit"), data={
            "username":"jakhongir",
            "first_name":"Jakhongir",
            "last_name":"Doe",
            "email":"jrahmonv3@gmail.com",
        })

        user.refresh_from_db()

        #user = User.objects.get(pk=user.pk)
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "jrahmonv3@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))
