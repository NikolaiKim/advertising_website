from rest_framework import permissions


# Кастомное ограничение на админа или создателя объявления
class IsAdminOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return request.user == obj.author
