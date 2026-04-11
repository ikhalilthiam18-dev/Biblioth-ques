from datetime import timedelta

from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import Auteur, Livre, Emprunt, Tag
from .serializers import (
    AuteurSerializer,
    LivreSerializer,
    LivreDetailSerializer,
    EmpruntSerializer,
    TagSerializer
)
from .permissions import EstProprietaireOuReadOnly
from .filters import LivreFilter
from .pagination import StandardPagination


# ===== PAGE D'ACCUEIL =====
class HomeView(TemplateView):
    template_name = 'home.html'


# ===== AUTEURS =====
class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='livres')
    def livres(self, request, pk=None):
        auteur = self.get_object()
        livres = auteur.livres.all()
        serializer = LivreSerializer(livres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        data = {
            'total_auteurs': Auteur.objects.count(),
            'total_livres': Livre.objects.count(),
            'nationalites': list(
                Auteur.objects.exclude(nationalite='').values_list('nationalite', flat=True).distinct()
            ),
        }
        return Response(data)


# ===== TAGS =====
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ===== LIVRES =====
class LivreViewSet(viewsets.ModelViewSet):
    queryset = (
        Livre.objects
        .select_related('auteur', 'cree_par')
        .prefetch_related('tags')
        .all()
    )
    permission_classes = [EstProprietaireOuReadOnly]
    pagination_class = StandardPagination
    filterset_class = LivreFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['titre', 'auteur__nom', 'isbn']
    ordering_fields = ['titre', 'annee_publication', 'date_creation']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LivreDetailSerializer
        return LivreSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'disponibles']:
            return [AllowAny()]
        if self.action in ['create', 'emprunter']:
            return [IsAuthenticated()]
        return [EstProprietaireOuReadOnly()]

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        qs = self.get_queryset().filter(disponible=True)
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        livre = self.get_object()
        if not livre.disponible:
            return Response(
                {'detail': 'Ce livre est déjà emprunté.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        date_retour_prevue = timezone.now().date() + timedelta(days=14)
        Emprunt.objects.create(
            utilisateur=request.user,
            livre=livre,
            date_retour_prevue=date_retour_prevue
        )
        livre.disponible = False
        livre.save()
        return Response(
            {
                'message': 'Livre emprunté avec succès.',
                'livre': livre.titre,
                'date_retour_prevue': date_retour_prevue
            },
            status=status.HTTP_200_OK
        )


# ===== EMPRUNTS =====
class EmpruntViewSet(viewsets.ModelViewSet):
    serializer_class = EmpruntSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Emprunt.objects.filter(utilisateur=self.request.user).select_related('livre', 'utilisateur')

    def perform_create(self, serializer):
        livre = serializer.validated_data['livre']
        if not livre.disponible:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Ce livre n'est pas disponible.")
        serializer.save(utilisateur=self.request.user)
        livre.disponible = False
        livre.save()

    @action(detail=True, methods=['post'])
    def rendre(self, request, pk=None):
        emprunt = self.get_object()
        if emprunt.rendu:
            return Response(
                {'detail': 'Ce livre a déjà été rendu.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        emprunt.rendu = True
        emprunt.save()
        livre = emprunt.livre
        livre.disponible = True
        livre.save()
        return Response({'message': 'Livre rendu avec succès.'}, status=status.HTTP_200_OK)
