from typing import Any, cast

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class HasEditPermissionOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only owners of the object, moderators and admins to edit it.
    Assumes the model instance has an `added_by` attribute.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if type(user) != User:
            return False

        if not hasattr(user, "profile"):
            return False

        if user.profile.role == "regular":  # type: ignore
            # Instance must have an attribute named `added_by`.
            return cast(bool, obj.added_by == request.user)

        # Moderators and admins can edit everything
        return True
