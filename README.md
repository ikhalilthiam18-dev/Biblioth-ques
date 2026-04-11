# 📚 API Bibliothèque

API REST complète pour la gestion d'une bibliothèque numérique — construite avec **Django REST Framework**, authentification **JWT**, documentation **Swagger/Redoc** intégrée.

---

## 🚀 Démarrage rapide (local)

```bash
# 1. Cloner et entrer dans le projet
cd bibliotheque_api

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Migrations
python manage.py migrate

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

Accédez à :
- 🏠 **Accueil** → http://localhost:8000/
- 📖 **Swagger UI** → http://localhost:8000/docs/
- 📄 **Redoc** → http://localhost:8000/redoc/
- ⚙️ **Admin** → http://localhost:8000/admin/
- 🔌 **API** → http://localhost:8000/api/

---

## ☁️ Déploiement sur Render (recommandé)

1. Pusher votre code sur GitHub
2. Créer un nouveau **Web Service** sur [render.com](https://render.com)
3. Connecter votre repo
4. Render détecte automatiquement `render.yaml` — configurer les variables d'env :

| Variable | Valeur |
|----------|--------|
| `SECRET_KEY` | Générer une clé secrète sécurisée |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `votre-app.onrender.com` |
| `DATABASE_URL` | URL de votre base PostgreSQL Render |

5. Cliquer **Deploy** — Render exécute `build.sh` automatiquement.

---

## ☁️ Déploiement sur Vercel

> ⚠️ Vercel est adapté pour les fonctions serverless. Vous devez utiliser une base de données externe (ex: Neon, Supabase, PlanetScale).

```bash
npm i -g vercel
vercel
```

Configurer les variables d'env dans le dashboard Vercel.

---

## 🔑 Authentification JWT

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "motdepasse"}'

# Utiliser le token
curl http://localhost:8000/api/livres/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..."
```

---

## 📡 Endpoints

| Ressource | URL | Méthodes |
|-----------|-----|----------|
| Livres | `/api/livres/` | GET, POST |
| Livre détail | `/api/livres/{id}/` | GET, PUT, PATCH, DELETE |
| Livres disponibles | `/api/livres/disponibles/` | GET |
| Emprunter | `/api/livres/{id}/emprunter/` | POST |
| Auteurs | `/api/auteurs/` | GET, POST |
| Auteur livres | `/api/auteurs/{id}/livres/` | GET |
| Auteur stats | `/api/auteurs/stats/` | GET |
| Emprunts | `/api/emprunts/` | GET, POST |
| Rendre un livre | `/api/emprunts/{id}/rendre/` | POST |
| Tags | `/api/tags/` | GET, POST |
| Token JWT | `/api/auth/token/` | POST |
| Rafraîchir token | `/api/auth/token/refresh/` | POST |

### Filtres disponibles sur `/api/livres/`

```
?search=victor hugo          # Recherche titre/auteur/ISBN
?categorie=roman             # roman, essai, poesie, bd, science, histoire
?disponible=true             # Disponibilité
?annee_min=1900&annee_max=2024  # Plage d'années
?auteur_nom=hugo             # Filtrer par nom d'auteur
?ordering=-annee_publication # Tri (- = décroissant)
?page=2&size=20              # Pagination
```

---

## 🛠️ Stack technique

- **Django 5.1** + **Django REST Framework 3.16**
- **Simple JWT** — Authentification par token
- **drf-spectacular** — Documentation OpenAPI/Swagger
- **django-filter** — Filtres avancés
- **WhiteNoise** — Fichiers statiques en production
- **dj-database-url** — Configuration DB par URL
- **Gunicorn** — Serveur WSGI production

---

## 📁 Structure

```
bibliotheque_api/
├── api/
│   ├── models.py          # Auteur, Livre, Emprunt, Tag
│   ├── views.py           # ViewSets + HomeView
│   ├── serializers.py     # Sérialisation DRF
│   ├── urls.py            # Routes API
│   ├── filters.py         # Filtres livres
│   ├── pagination.py      # Pagination personnalisée
│   ├── permissions.py     # Permission propriétaire
│   └── admin.py           # Interface admin
├── bibliotheque_project/
│   ├── settings.py        # Configuration principale
│   ├── urls.py            # URLs globales
│   └── wsgi.py
├── templates/
│   ├── home.html          # Page d'accueil moderne
│   ├── admin/             # Admin personnalisé (dark mode)
│   └── rest_framework/    # DRF browsable API
├── static/css/custom.css  # Design premium
├── requirements.txt
├── render.yaml            # Config Render
├── vercel.json            # Config Vercel
├── Procfile               # Config Heroku/Render
└── build.sh               # Script de build
```
