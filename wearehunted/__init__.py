from wearehunted.models import *
import urllib
import urllib2
import json

API_URL = 'http://api.bandcamp.com/api/%(object_type)s/%(version)s/%(method)s?%(params)s'

SINGLES_CHART_URL = 'http://wearehunted.com/api/chart/%(chart)s/singles/%(period)s/'
ARTIST_CHART_URL  = 'http://wearehunted.com/api/chart/%(chart)s/artists/%(period)s/'
USER_CHART_URL    = 'http://wearehunted.com/api/chart/by/%(user)/'
ARTIST_LOOKUP_URL = 'http://wearehunted.com/api/lookup/artist/'

DAILY   = 1
WEEKLY  = 7
MONTHLY = 30

ROCK        = 'rock'
POP         = 'pop'
FOLK        = 'folk'
METAL       = 'metal'
ALTERNATIVE = 'alternative'
ELECTRONIC  = 'electronic'
PUNK        = 'punk'
RAP_HIP_HOP = 'rap-hip-hop'
TWITTER     = 'twitter'
REMIX       = 'remix'

class WeAreHuntedError(Exception):
  pass

class WeAreHuntedService(object):
  def get_artists_chart(self, chart, period = WEEKLY, providers = (), count = 50):
    url = ARTIST_CHART_URL % {'chart': chart, 'period': period}

    return [ArtistChartEntry.new_from_json(o) for o in self._fetch(url, {'providers': providers, 'count': count, 'allow_blanks': False})]

  def get_singles_chart(self, chart, period = WEEKLY, providers = (), count = 50):
    url = SINGLES_CHART_URL % {'chart': chart, 'period': period}

    return [SingleChartEntry.new_from_json(o) for o in self._fetch(url, {'providers': providers, 'count': count, 'allow_blanks': False})]

  def get_user_chart(self, user, providers = (), count = 50):
    url = USER_CHART_URL % {'user': user}

    return [SingleChartEntry.new_from_json(o) for o in self._fetch(url, {'providers': providers, 'count': count, 'allow_blanks': False})]

  # Cannot really accept multiple artists
  # order is reversed, artists that are not found are simply not returned
  def lookup_artist(self, artist):
    return self._fetch(ARTIST_LOOKUP_URL, {'name': artist})[0]

  def _fetch(self, url, params):
    fetch_url = '%s?%s' % (url, urllib.urlencode(params))

    res = urllib2.urlopen(url)

    data = json.loads(res.read())

    return data['results']
