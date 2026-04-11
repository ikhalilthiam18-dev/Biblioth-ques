from rest_framework.permissions import BasePermission, SAFE_METHODS


class EstProprietaireOuReadOnly(BasePermission):
    """
    Lecture libre.
    Modification uniquement par le propriétaire ou un admin.
    """
    message = "Vous devez être le propriétaire pour modifier cet objet."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.cree_par == request.user or request.user.is_staff