import uuid
from datetime import timedelta
from typing import Any

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from movieswebapp.moviesapp.models import UserProfile
from movieswebapp.moviesapp.serializers import UserProfileSerializer


class UserRegistrationView(generics.CreateAPIView[UserProfile]):
    """
    View to register a new user.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validation_expiry_date = str(timezone.now() + timedelta(minutes=10))
        validation_code = str(uuid.uuid4())
        data = request.data.copy()
        data["validation_code"] = validation_code
        data["validation_expiry_date"] = validation_expiry_date
        data["active"] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {validation_code: validation_code},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserValidationView(generics.UpdateAPIView[UserProfile]):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validation_code = request.data.get("validation_code")
        try:
            user_profile: UserProfile = UserProfile.objects.get(
                validation_code=validation_code
            )
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Validation code not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_profile.validation_expiry_date < timezone.now():
            return Response(
                {"error": "Validation code expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_profile.active = True
        user_profile.save()
        return Response(
            {"success": "User profile activated"}, status=status.HTTP_200_OK
        )
