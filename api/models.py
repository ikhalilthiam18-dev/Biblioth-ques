from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Auteur(models.Model):
    nom = models.CharField(max_length=200, verbose_name='Nom complet')
    biographie = models.TextField(blank=True, null=True, verbose_name='Biographie')
    nationalite = models.CharField(max_length=100, blank=True, default='', verbose_name='Nationalité')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'


class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Livre(models.Model):
    CATEGORIES = [
        ('roman', 'Roman'),
        ('essai', 'Essai'),
        ('poesie', 'Poésie'),
        ('bd', 'Bande dessinée'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
    ]

    titre = models.CharField(max_length=300, verbose_name='Titre')
    isbn = models.CharField(max_length=17, unique=True, verbose_name='ISBN')
    annee_publication = models.IntegerField(verbose_name='Année de publication')
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='roman', verbose_name='Catégorie')

    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.CASCADE,
        related_name='livres',
        verbose_name='Auteur'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='livres'
    )

    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    # IMPORTANT pour la permission propriétaire
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livres_crees'
    )

    def __str__(self):
        return f'{self.titre} ({self.annee_publication})'

    class Meta:
        ordering = ['-annee_publication', 'titre']


class Emprunt(models.Model):
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emprunts'
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='emprunts'
    )
    date_emprunt = models.DateField(default=timezone.now)
    date_retour_prevue = models.DateField()
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.utilisateur.username} - {self.livre.titre}'

    class Meta:
        ordering = ['-date_emprunt']