import json
import uuid

from django.utils import timezone

from admin_datta.utils import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import UserToken
from services.account import UserTokenRepository


class UserTokenAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        tokens = UserToken.objects.filter()
        if not user.is_staff:
            tokens = tokens.filter(user_id=user.id)
        tokens = tokens.all()
        result = []
        for token in tokens:
            token_data = token.to_readable_dict()
            if token.expired_at < timezone.now() and token.ttl != -1:
                token_data['status'] = 'Expired'
            else:
                token_data['status'] = 'Active'
            if token.ttl == -1:
                token_data['expired_at'] = 'Never'
            result.append(token_data)

        return JsonResponse(result, safe=False)

    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        ttl = int(data.get('ttl', 3600))

        token = UserTokenRepository().create_token(user_id=user.id,
                                                   ttl=ttl,
                                                   description=data.get('description', ''))
        expired_at = token.expired_at
        token = token.to_readable_dict()
        if expired_at < timezone.now() and ttl != -1:
            token['status'] = 'Expired'
        else:
            token['status'] = 'Active'
        return JsonResponse(token)


@permission_classes([IsAuthenticated])
def delete_token(request, token_id):
    user = request.user
    token = UserToken.objects.filter(id=token_id)
    if not user.is_staff:
        token = token.filter(user_id=user.id)
    token = token.first()
    if not token:
        return JsonResponse({'success': False, 'error': 'Token not found'}, status=400)
    UserTokenRepository().delete_token(token.id)
    return JsonResponse({'success': True})
