from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


# Modèle représentant un ticket (une demande de critique sur un livre).
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


# Modèle représentant une critique (review) liée à un ticket.
class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192)
    time_created = models.DateTimeField(auto_now_add=True)


# Modèle représentant la relation "abonnement" entre deux utilisateurs.
class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following'
        )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='followed_by'
        )

    class Meta():
        # Contraint la base à empêcher les doublons : 
        # un même utilisateur ne peut pas suivre deux fois la même personne.
        unique_together = ('user', 'followed_user')
