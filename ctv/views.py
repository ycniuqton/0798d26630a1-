import requests
from django.http import HttpResponse
from django.conf import settings

import requests
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedServer, CachedOS
from home.models import Vps

from django.http import JsonResponse

UPSTREAM_URL = 'https://upstream-server.com/some_path/'


@permission_classes([IsAuthenticated])
def proxy_view(request, proxy_path):
    # Construct the full URL to the upstream server
    upstream_url = f'{UPSTREAM_URL}{proxy_path}'

    # Get the full query string
    query_string = request.META.get('QUERY_STRING', '')

    # Include the query string if it exists
    if query_string:
        upstream_url = f'{upstream_url}?{query_string}'

    # Pre-processing: You can add custom logic here
    # For example, logging the request or modifying headers
    print(f"Proxying request to: {upstream_url}")

    # Perform the request to the upstream server
    try:
        upstream_response = requests.request(
            method=request.method,
            url=upstream_url,
            headers=request.headers,
            data=request.body,
            allow_redirects=False,
        )
    except requests.RequestException as e:
        return HttpResponse(f"Error occurred while proxying: {str(e)}", status=500)

    # Post-processing: You can add custom logic here
    # For example, logging the response or modifying the response content
    print(f"Response from upstream: {upstream_response.status_code}")

    # Prepare and return the response
    response = HttpResponse(
        upstream_response.content,
        status=upstream_response.status_code,
        content_type=upstream_response.headers.get('Content-Type', 'text/html')
    )

    # Copy headers from upstream response to Django response
    # for header, value in upstream_response.headers.items():
    #     if header.lower() != 'content-encoding':  # Avoid issues with encoding
    #         response[header] = value

    return response
