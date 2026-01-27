import hashlib
from rest_framework import authentication, exceptions
from .models import Hospital


class HospitalAPIKeyAuthentication(authentication.BaseAuthentication):
    """Simple API key authentication for hospital integrations."""

    keyword = "X-API-Key"

    def authenticate(self, request):
        api_key = request.headers.get(self.keyword)
        if not api_key:
            return None

        hashed = hashlib.sha256(api_key.encode()).hexdigest()
        try:
            hospital = Hospital.objects.get(api_key_hash=hashed, is_active=True)
        except Hospital.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid API key.")

        # DRF expects a (user, auth) tuple. We pass the hospital as the user-like object.
        return (hospital, None)


def hash_api_key(raw_key: str) -> str:
    """Utility to hash an API key with SHA-256."""
    return hashlib.sha256(raw_key.encode()).hexdigest()
