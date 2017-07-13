import kubernetes
import json, os, yaml
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from functools import lru_cache
import itertools
from clint.textui import puts, indent


from generic_api import GenericApi

kubernetes.config.load_kube_config(context="thisone")
# kubernetes.config.load_kube_config(context="l8")

# FIXME does not pick up config changes after initialized
generic = GenericApi()


def list_resources(namespace):

    api_versions = generic.call_api(f"/api", "GET")[0]["versions"]
    for api_version in api_versions:
        resources = generic.call_api(f"/api/{api_version}", "GET")[0]["resources"]
        for resource in resources:
            # if "/" in resource["name"]:
            #     continue
            if not resource["namespaced"]:
                continue
            url = f"/api/{api_version}/namespaces/{namespace}/{resource['name']}"
            try:
                result = generic.call_api(url, "GET")
                items = result[0]["items"]
            except kubernetes.client.rest.ApiException as e:
                if e.status in [404, 405]:
                    items = None
                else:
                    print(f"EXCEPTION: kubernetes.client.rest.ApiException")
                    print(f"status: {e.status}\nreason: {e.reason}\nbody: {e.body}\nheaders: {e.headers}")
            if items:
                puts(url)
                with indent(2):
                    for item in items:
                        puts(item["metadata"]["name"])

    groups = generic.call_api("/apis", "GET")[0]["groups"]
    for group in groups:
        # print(group["name"], group["preferredVersion"]["groupVersion"])
        resources = generic.call_api(f"/apis/{group['preferredVersion']['groupVersion']}", "GET")[0]["resources"]
        for resource in resources:
            if "/" in resource["name"]:
                continue
            if not resource["namespaced"]:
                continue
            url = f"/apis/{group['preferredVersion']['groupVersion']}/namespaces/{namespace}/{resource['name']}"
            try:
                result = generic.call_api(url, "GET")
                items = result[0]["items"]
            except kubernetes.client.rest.ApiException as e:
                if e.status in [404, 405]:
                    items = None
                else:
                    print(f"EXCEPTION: kubernetes.client.rest.ApiException")
                    print(f"status: {e.status}\nreason: {e.reason}\nbody: {e.body}\nheaders: {e.headers}")
            if items:
                puts(url)
                with indent(2):
                    for item in items:
                        puts(item["metadata"]["name"])

# list_resources("default")

namespaces = generic.call_api("/api/v1/namespaces", "GET")[0]["items"]
# print(namespaces)

namespaces = ["ghost-test-1"]
for namespace in namespaces:
    # namespace_name = namespace["metadata"]["name"]
    namespace_name = namespace
    puts(namespace_name)
    with indent(2):
        list_resources(namespace_name)

# generic.call_api("/api/v1/pods", "GET")
