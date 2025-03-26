from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

def generate_jwt_token(user, token_type='access'):
    """
    Creates JWT tokens for authentication.
    
    Args:
        user: User object for whom to generate tokens
        token_type: Type of token ('access' or 'refresh')
    
    Returns:
        string: JWT token
    """
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims
    refresh['user_id'] = str(user.user_id)
    refresh['username'] = user.username
    refresh['role'] = user.role
    
    if token_type == 'access':
        return str(refresh.access_token)
    return str(refresh)

def validate_token(token):
    """
    Validates a JWT token.
    
    Args:
        token: JWT token string to validate
        
    Returns:
        dict: Token payload if valid
        None: If token is invalid
    """
    try:
        # This will validate signature and expiration
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
