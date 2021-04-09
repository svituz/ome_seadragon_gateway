import logging
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.viewsets import ViewSet

import ome_seadragon_gateway.settings as gws

logger = logging.getLogger('ome_seadragon_gw')


class SimpleGetWrapper(ViewSet):
    if settings.AUTH_TYPE == 'oauth2':
        permission_classes = (TokenHasScope,)
        required_scopes = ['read']

    # else:
    # keycloak_roles = {
    #     'GET': ['digital-biobank-pathologist'],
    # }

    def _get_ome_seadragon_url(self, url):
        return urljoin(
            gws.OME_SEADRAGON_BASE_URL, url
        )

    def _get(self, client, url, params=None):
        logger.debug('_get --- URL: %s --- params: %r', url, params)
        response = client.get(url, params=params,
                              headers={'X-Requested-With': 'XMLHttpRequest'})
        if response.status_code == status.HTTP_200_OK:
            print(response.content)
            return HttpResponse(
                response.content, status=status.HTTP_200_OK,
                content_type=response.headers.get('content-type')
            )
        else:
            logger.error('ERROR CODE: %s', response.status_code)
            raise NotAuthenticated()
