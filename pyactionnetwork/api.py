#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote


class ActionNetworkAPI():
    """Python wrapper for Action Network API"""

    ACTION_NETWORK_API_DEFAULT_BASE_URL = 'https://actionnetwork.org/api/v2/'

    def __init__(self, api_key, **kwargs):
        """Primary object used to interact with the ActionNetwork REST API"""
        self._headers = {"OSDI-API-Token": api_key}
        self._base_url = self.ACTION_NETWORK_API_DEFAULT_BASE_URL
        self._refresh_config()
    
    def _refresh_config(self):
        """Gets up-to-date action network API config"""
        self._config = requests.get(
            url=self.ACTION_NETWORK_API_DEFAULT_BASE_URL,
            headers=self._headers
        ).json()

    def _resource_to_url(self, resource):
        if resource in self._config['_links']:
            return self._config['_links'][resource]['href']
        try:
            return self._config['_links']['osdi:{}'.format(resource)]['href']
        except KeyError:
            raise KeyError("Unknown resource {}".format(resource))

    def get_resource(self, resource):
        url = self._resource_to_url(resource.lower())
        return requests.get(url, headers=self._headers).json()

    def get_person(self, person_id=None, search_by='email', search_string=None):
        if person_id:
            url = "{0}people/{1}".format(self._base_url, person_id)
        else: 
            url = "{0}people/?filter={1} eq '{2}'".format(
                self._base_url,
                search_by,
                quote(search_string)
            )
        
        resp = requests.get(url, headers=self._headers)
        return resp.json()

    # TODO: Change this to be a general POST function that takes an ANBaseModel
    # object created with e.g. Person.new()
    def create_person(
        self,
        email=None,
        given_name='',
        family_name='',
        address=list(),
        city='',
        state='',
        country='',
        postal_code='',
        tags=list(),
        custom_fields=dict()
    ):
        url = "{0}people/".format(self._base_url)
        payload = {
            'person': {
                'family_name': family_name,
                'given_name': given_name,
                'postal_addresses': [{
                    'address_lines': list(address),
                    'locality': city,
                    'region': state,
                    'country': country,
                    'postal_code': postal_code
                }],
                'email_addresses': [{
                    'address': email
                }],
                'custom_fields': custom_fields
            },
            'add_tags': dict(tags)
        }

        resp = requests.post(url, json=payload, headers=self._headers)
        return resp.json()


