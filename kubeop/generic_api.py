from __future__ import absolute_import
import sys
import os
import re
from functools import lru_cache

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

    def call_api(self, resource_path, method, **kwargs):
        kwargs['response_type'] = object
        kwargs['auth_settings'] = ['BearerToken'] # FIXME default?
        return self.api_client.call_api(resource_path, method, **kwargs)

    def list_generic(self, **kwargs):
        # print(kwargs)
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self._list_generic(**kwargs)
        else:
            (data) = self._list_generic(**kwargs)
            # print(data)
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


    # FIXME use ttl_cache instead
    @lru_cache(maxsize=128)
    def lookup_resource(self, api_version, kind):
        api_prefix = "api" if api_version == "v1" else "apis"
        resources = self.call_api(f"/{api_prefix}/{api_version}", "GET")[0]["resources"]
        # FIXME if not api_version, search through all
        for resource in resources:
            if resource["kind"]==kind and "/" not in resource["name"]:
                return resource

    def build_url(self, api_version, kind, namespace=None):
        resource = self.lookup_resource(api_version, kind)
        if not resource:
            print("ERR", api_version, kind)
            # FIXME raise exception?
            return None

        api_prefix = "api" if api_version == "v1" else "apis"
        if resource["namespaced"] and namespace:
            return f"/{api_prefix}/{api_version}/namespaces/{namespace}/{resource['name']}"

        return f"/{api_prefix}/{api_version}/{resource['name']}"


    def apply_manifest(self, manifest):
        url = self.build_url(
            manifest['apiVersion'],
            manifest['kind'],
            manifest['metadata'].get('namespace'))

        result = self.generic.call_api(url, "POST", body=manifest)

        # try:
        #     result = self.generic.call_api(url, "POST", body=manifest)
        #     print(f"result: ", result)
        # except kubernetes.client.rest.ApiException as e:
        #     print(f"! kubernetes.client.rest.ApiException: {e}")
