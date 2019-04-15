import json
from rauth import OAuth2Service
from flask import url_for, request, redirect, session

from app import app

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class ORCIDSignIn(OAuthSignIn):
    def __init__(self):
        super(ORCIDSignIn, self).__init__('orcid')
        # These will need to be updated to point to the non-sandbox orcid
        # site for a production app
        auth_url = 'https://sandbox.orcid.org/oauth/authorize'
        base_url = 'https://sandbox.orcid.org'
        token_url = 'https://sandbox.orcid.org/oauth/token'

        self.service = OAuth2Service(name='orcid', client_id=self.consumer_id,
                client_secret=self.consumer_secret, authorize_url=auth_url,
                base_url=base_url, access_token_url=token_url)

    def authorize(self):
        return redirect(self.service.get_authorize_url(scope='/authenticate',
                response_type='code', redirect_uri=self.get_callback_url()))

    def callback(self):
        if 'code' not in request.args:
            return None, None

        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads)

        access_token = oauth_session.access_token
        orcid_id = json.loads(oauth_session.access_token_response.content)['orcid']

        return access_token, orcid_id