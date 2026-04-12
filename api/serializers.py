from rest_framework import serializers
from .models import Auteur, Livre, Emprunt, Tag


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nom']


class LivreSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source='tags',
        write_only=True,
        required=False
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_nom',
            'disponible', 'tags', 'tag_ids',
            'cree_par', 'date_creation'
        ]
        read_only_fields = ['id', 'auteur_nom', 'tags', 'cree_par', 'date_creation']

    def get_auteur_nom(self, obj):
        return obj.auteur.nom

    def validate_isbn(self, value):
        clean = value.replace('-', '')
        if not clean.isdigit() or len(clean) != 13:
            raise serializers.ValidationError("L'ISBN doit contenir exactement 13 chiffres.")
        return value

    def validate_annee_publication(self, value):
        if value < 1000 or value > 2026:
            raise serializers.ValidationError("L'année doit être entre 1000 et 2026.")
        return value

    def validate(self, data):
        if data.get('categorie') == 'essai':
            auteur = data.get('auteur')
            if auteur and not auteur.biographie:
                raise serializers.ValidationError(
                    "Les essais requièrent une biographie de l'auteur."
                )
        return data


class LivreDetailSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)
    auteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Auteur.objects.all(),
        source='auteur',
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source='tags',
        write_only=True,
        required=False
    )

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_id',
            'disponible', 'tags', 'tag_ids',
            'cree_par', 'date_creation'
        ]
        read_only_fields = ['id', 'cree_par', 'date_creation']


class EmpruntSerializer(serializers.ModelSerializer):
    utilisateur_username = serializers.ReadOnlyField(source='utilisateur.username')
    livre_titre = serializers.ReadOnlyField(source='livre.titre')

    class Meta:
        model = Emprunt
        fields = [
            'id', 'utilisateur', 'utilisateur_username',
            'livre', 'livre_titre',
            'date_emprunt', 'date_retour_prevue', 'rendu'
        ]
        read_only_fields = ['id', 'utilisateur', 'date_emprunt', 'utilisateur_username', 'livre_titre']

    def validate(self, data):
        livre = data.get('livre')
        if livre and not livre.disponible:
            raise serializers.ValidationError("Ce livre n'est pas disponible.")
        return data