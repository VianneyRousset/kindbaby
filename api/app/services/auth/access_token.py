from datetime import UTC, datetime

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.config import AuthConfig
from app.errors.auth import InvalidCredentialError
from app.schemas.auth.data import UserAccessTokenData


def create_access_token(
    *,
    user_id: int,
    validated: bool,
    config: AuthConfig,
) -> str:
    """Create a new access token."""
    # issued at time
    iat = datetime.now(UTC)

    return jwt.encode(
        payload={
            "iat": iat,
            "exp": iat + config.access_token_duration,
            "sub": str(user_id),
            "validated": validated,
        },
        key=config.secret_key,
        algorithm=config.algorithm,
    )


def verify_access_token(
    token: str,
    *,
    config: AuthConfig,
) -> UserAccessTokenData:
    """Check that `token` is valid and not expired."""

    try:
        payload = jwt.decode(
            jwt=token,
            key=config.secret_key,
            algorithms=[config.algorithm],
        )

        return UserAccessTokenData(**payload)

    except (InvalidTokenError, ValidationError) as error:
        raise InvalidCredentialError() from error
