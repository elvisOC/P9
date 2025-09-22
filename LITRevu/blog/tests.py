from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Ticket, Review, UserFollows
from blog import forms

User = get_user_model()


# ---------- TESTS DES MODÈLES ----------
class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="S3cur3P@ssw0rd!")
        self.ticket = Ticket.objects.create(
            title="Titre Test", description="Description Test", user=self.user
        )
        self.review = Review.objects.create(
            ticket=self.ticket,
            rating=4,
            user=self.user,
            headline="Super",
            body="Critique détaillée"
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.title, "Titre Test")
        self.assertEqual(self.ticket.user.username, "alice")

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.ticket, self.ticket)

    def test_user_follows_unique(self):
        bob = User.objects.create_user(username="bob", password="S3cur3P@ssw0rd!")
        UserFollows.objects.create(user=self.user, followed_user=bob)
        with self.assertRaises(Exception):  # doublon interdit
            UserFollows.objects.create(user=self.user, followed_user=bob)


# ---------- TESTS DES FORMULAIRES ----------
class FormsTestCase(TestCase):
    def test_ticket_form_valid(self):
        form = forms.ticketForm(data={"title": "Un titre", "description": "Une description"})
        self.assertTrue(form.is_valid())

    def test_review_form_valid(self):
        form = forms.ReviewForm(data={"rating": 3, "headline": "Titre", "body": "Texte"})
        self.assertTrue(form.is_valid())

    def test_search_user_form_valid(self):
        form = forms.search_user(data={"query": "alice"})
        self.assertTrue(form.is_valid())


# ---------- TESTS DES VUES ----------
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="alice", password="S3cur3P@ssw0rd!")
        self.client.force_login(self.user)  # connexion directe pour tester les vues protégées

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_posts_view(self):
        response = self.client.get(reverse("posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/posts.html")

    def test_publier_ticket_view(self):
        response = self.client.post(reverse("ticket_upload"), {
            "title": "Nouveau ticket",
            "description": "Texte",
        })
        self.assertEqual(response.status_code, 302)  # redirection après création
        self.assertTrue(Ticket.objects.filter(title="Nouveau ticket").exists())

    def test_create_review_for_existing_ticket(self):
        ticket = Ticket.objects.create(title="Ticket existant", description="desc", user=self.user)
        url = reverse('reply_to_ticket', args=[ticket.id])
        response = self.client.post(url, {
            'rating': 4,
            'headline': "Réponse",
            'body': "Critique attachée au ticket"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(ticket=ticket, headline="Réponse").exists())

    def test_create_ticket_and_review_together(self):
        url = reverse('review_upload')  
        response = self.client.post(url, {
            'title': "Nouveau ticket",
            'description': "Description ticket",
            'rating': 5,
            'headline': "Ma review",
            'body': "Texte review"
        })
        self.assertEqual(response.status_code, 302)
        ticket = Ticket.objects.get(title="Nouveau ticket")
        self.assertTrue(Review.objects.filter(ticket=ticket, headline="Ma review").exists())

    def test_edit_ticket_view(self):
        ticket = Ticket.objects.create(title="Ancien titre", description="desc", user=self.user)
        response = self.client.post(reverse("edit_ticket", args=[ticket.id]), {
            "title": "Nouveau titre",
            "description": "Nouvelle desc"
        })
        self.assertEqual(response.status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, "Nouveau titre")

    def test_delete_ticket_view(self):
        ticket = Ticket.objects.create(title="A supprimer", description="desc", user=self.user)
        response = self.client.post(reverse("delete_ticket", args=[ticket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())

    def test_edit_review_view(self):
        ticket = Ticket.objects.create(title="Test Ticket", description="test", user=self.user)
        review = Review.objects.create(
            ticket=ticket, rating=3, user=self.user,
            headline="Ancien titre", body="Ancien texte"
        )
        response = self.client.post(reverse("edit_review", args=[review.id]), {
            "rating": 4,
            "headline": "Nouveau titre",
            "body": "Nouveau texte"
        })
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.headline, "Nouveau titre")

    def test_delete_review_view(self):
        ticket = Ticket.objects.create(title="Test Ticket", description="test", user=self.user)
        review = Review.objects.create(ticket=ticket, rating=2, user=self.user, headline="À supprimer", body="texte")
        response = self.client.post(reverse("delete_review", args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_subscribe_follow_unfollow(self):
        bob = User.objects.create_user(username="bob", password="S3cur3P@ssw0rd!")
        # Vérifier que la recherche fonctionne
        response = self.client.get(reverse("subscribe"), {"query": "bob"})
        self.assertEqual(response.status_code, 200)
        # Suivre bob
        self.client.get(reverse("follow_user", args=[bob.id]))
        self.assertTrue(UserFollows.objects.filter(user=self.user, followed_user=bob).exists())
        # Se désabonner
        self.client.get(reverse("unfollow_user", args=[bob.id]))
        self.assertFalse(UserFollows.objects.filter(user=self.user, followed_user=bob).exists())
