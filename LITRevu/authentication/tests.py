from django.test import TestCase, Client
from django.urls import reverse
from authentication.forms import LoginForm, LoginFormLarge, LoginFormMedium, SignUpForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Tests formulaires.
class AuthenticationFormsTestCase(TestCase):
    def test_login_form_valid(self):
        form = LoginForm(data={"username": "alice", "password": "password123"})
        self.assertTrue(form.is_valid())

    def test_login_form_large_and_medium_have_custom_ids(self):
        form_large = LoginFormLarge()
        self.assertEqual(form_large.fields['username'].widget.attrs.get('id'), 'id_username_large')
        self.assertEqual(form_large.fields['password'].widget.attrs.get('id'), 'id_password_large')

        form_medium = LoginFormMedium()
        self.assertEqual(form_medium.fields['username'].widget.attrs.get('id'), 'id_username_medium')
        self.assertEqual(form_medium.fields['password'].widget.attrs.get('id'), 'id_password_medium')

    def test_signup_form_valid(self):
        form = SignUpForm(data={
            "username": "bob",
            "password1": "S3cur3P@ssw0rd!",
            "password2": "S3cur3P@ssw0rd!"
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_passwords_mismatch(self):
        form = SignUpForm(data={
            "username": "bob",
            "password1": "S3cur3P@ssw0rd!",
            "password2": "differentpassword"
        })
        self.assertFalse(form.is_valid())


# Tests Views
class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="alice", password="password123")

    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "username": "alice",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)  

    def test_login_view_failure(self):
        response = self.client.post(reverse("login"), {
            "username": "alice",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Identifiants invalides")

    def test_logout_view(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  

    def test_signup_view_creates_user(self):
        response = self.client.post(reverse("signup"), {
            "username": "charlie",
            "password1": "S3cur3P@ssw0rd!",
            "password2": "S3cur3P@ssw0rd!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="charlie").exists())
