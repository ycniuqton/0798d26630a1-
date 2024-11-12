from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.APIKeyAuthentication'  # Path to your custom authenticator
    name = 'APIKeyAuth'  # This will appear as the name in Swagger-UI

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'x-api-key',  # Customize to the header your API expects
            'description': 'API Key-based authentication with x-api-key header',
        }
