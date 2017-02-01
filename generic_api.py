from __future__ import absolute_import
import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from kubernetes.client.configuration import Configuration
from kubernetes.client.api_client import ApiClient


class GenericApi(object):

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def list_generic(self, **kwargs):
        # print(kwargs)
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self._list_generic(**kwargs)
        else:
            (data) = self._list_generic(**kwargs)
            print(data)
            return data

    def _list_generic(self, **kwargs):
        resource_path = kwargs.pop('resource_path')
        kwargs['header_params'] = {
          'Accept': self.api_client.select_header_accept(['application/json', 'application/json;stream=watch']),
          'Content-Type': self.api_client.select_header_content_type(['*/*'])
        }
        kwargs['auth_settings'] = ['BearerToken']
        kwargs['response_type'] = object
        if 'query_params' not in kwargs:
          kwargs['query_params'] = {}
        if 'timeout_seconds' in kwargs:
            kwargs['query_params']['timeoutSeconds'] = kwargs.pop('timeout_seconds')
        if 'watch' in kwargs:
            kwargs['query_params']['watch'] = kwargs.pop('watch')
        return self.api_client.call_api(resource_path, 'GET', **kwargs)

    def call_api(self, resource_path, method, **kwargs):
        kwargs['response_type'] = object
        return self.api_client.call_api(resource_path, method, **kwargs)
