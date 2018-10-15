from django.conf import settings
from django.utils import timezone
from horizon.utils import memoized
import requests

import logging
LOG = logging.getLogger(__name__)

CACHE_TTL = 5  # Minutes


@memoized.memoized(max_size=1)
def _get_available_sites_memo(key):
    reference_api_url = settings.CHAMELEON_REFERENCE_API_URL
    if not reference_api_url:
        return []

    sites = []
    try:
        res = requests.get(
            url='/'.join([reference_api_url, 'sites.json']),
            timeout=5)
        res.raise_for_status()
        items = res.json().get('items', [])
        sites = sorted([
            {'id': s['uid'], 'name': s['name'], 'url': s['web']}
            for s in items
        ], key=lambda x: x['id'])
    except requests.Timeout:
        LOG.error('Timeout occurred fetching sites')
    except requests.HTTPError as http_err:
        LOG.error('Unexpected HTTP error occurred fetching sites: %s', http_err)
    except:
        LOG.exception('An unexpected error occurred fetching sites')

    return sites


def get_available_sites():
    """Get a list of all available Chameleon sites.

    This will fetch the list of sites from the Chameleon reference API, which
    contains metadata about the site's web location, its id, and display name,
    amongst other things.

    Returns:
        List[(id,name,url)]: a list of dict structures containing the id, name,
            and site URL for each site found.
    """
    now = timezone.now()
    key = round(now.minute / CACHE_TTL)
    # We use the @memoized decorator with a max_size=1 to turn this in to what
    # is really a 'debounced' function that only executes once per some time
    # interval (TTL).
    return _get_available_sites_memo(key)


def get_current_site():
    site_id = settings.CHAMELEON_SITE_ID
    return next(iter([
        site for site in get_available_sites()
        if site['id'] == site_id
    ]), None)
