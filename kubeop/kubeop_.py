import kubernetes
import json, os, yaml
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from functools import lru_cache
import itertools
import click
from .generic_api import GenericApi


# FIXME
# use revision of `Ghost` manifest as label for all derived templates
# or created_at or something.
# to be able to identify orphans.

class Operator(object):

    def __init__(self, context):
        # kubernetes.config.load_kube_config(context="thisone")
        kubernetes.config.load_kube_config(context=context)

        # FIXME does not pick up config changes after initialized
        self.generic = GenericApi()

    # FIXME use ttl_cache instead
    @lru_cache(maxsize=128)
    def lookup_resource(self, api_version, kind):
        api_prefix = "api" if api_version == "v1" else "apis"
        resources = self.generic.call_api(f"/{api_prefix}/{api_version}", "GET")[0]["resources"]
        for resource in resources:
            if resource["kind"]==kind and "/" not in resource["name"]:
                return resource

    def build_url(self, api_version, kind, namespace=None):
        resource = self.lookup_resource(api_version, kind)
        if not resource:
            print("ERR", api_version, kind)
            exit

        api_prefix = "api" if api_version == "v1" else "apis"
        if resource["namespaced"] and namespace:
            # if not namespace:
            #     namespace = "default"
            return f"/{api_prefix}/{api_version}/namespaces/{namespace}/{resource['name']}"

        return f"/{api_prefix}/{api_version}/{resource['name']}"


    # FIXME api/kind to watch as config-parameter

    # maybe base_path + rel?
    def apply_templates(self, path, values):
        env = Environment(loader=FileSystemLoader(os.fspath(path)))

        for item in sorted(path.iterdir()):
            if not item.is_file():
                continue
            # print(item) # FIXME log

            rel_path = os.path.relpath(item, start=path)
            template = env.get_template(rel_path)
            manifest = yaml.load(template.render(values))
            # print(manifest)
            # print(values)

            api_version = manifest['apiVersion']
            kind = manifest['kind']
            namespace = manifest['metadata'].get('namespace')
            url = self.build_url(api_version, kind, namespace)
            #^ or: build_url_for_manifest

            # FIXME check for changes in manifest and take care to re-apply
            # and restart pods if necessary
            print(f"POST {url}") # FIXME log

            try:
                result = self.generic.call_api(url, "POST", body=manifest)
                print(f"result: ", result)
            except kubernetes.client.rest.ApiException as e:
                print(f"! kubernetes.client.rest.ApiException: {e}")


    def delete_thirdparty(self, thirdparty):
        # FIXME add selectors
        namespace = thirdparty['metadata'].get('namespace')
        name = thirdparty['metadata']['name']
        thirdparty_kind = thirdparty["kind"]

        # patch Deployment
        url = self.build_url("extensions/v1beta1", "Deployment", namespace) + f"/{name}"
        print(f"PATCH {url}")

        body = {"spec":{"revisionHistoryLimit":0, "paused": True}}
        headers = {"Content-Type":"application/strategic-merge-patch+json"}
        result = self.generic.call_api(url, "PATCH", body=body, header_params=headers)

        # delete
        kinds = [
            ("extensions/v1beta1", "Deployment"),
            ("extensions/v1beta1", "ReplicaSet"),
            ("v1", "Pod"),
            ("v1", "ConfigMap"),
            ("v1", "Service"),
            ("extensions/v1beta1", "Ingress")
            ]

        for api_version, kind in kinds:
            url = self.build_url(api_version, kind, namespace) + f"?labelSelector=app={name},thirdparty={thirdparty_kind}"
            print(f"DELETE {url}")
            try:
                self.generic.call_api(url, "DELETE")
            except kubernetes.client.rest.ApiException as e:
                if e.status in [405]:
                    print(e.reason)
                    url = self.build_url(api_version, kind, namespace) + f"/{name}"
                    print(f"DELETE {url}")
                    self.generic.call_api(url, "DELETE")
                else:
                    print(f"[EXCEPTION] kubernetes.client.rest.ApiException")
                    print(f"status: {e.status}\nreason: {e.reason}\nbody: {e.body}\nheaders: {e.headers}")


    def watch_thirdparty(self, api_version, kind, namespace ):
        # self.lookup_resource(api_version, kind)
        self.lookup_resource("experimantal.giantswarm.com/v1", "Ghost")
        #^ if missing? wait loop? watcher? exit?

        # FIXME build_url to watch
        url = self.build_url(api_version, kind, namespace)
        print(f"url: {url}")
        watch = kubernetes.watch.Watch(return_type=object)
        for event in watch.stream(self.generic.list_generic, resource_path=url, timeout_seconds=90000):
            # resource_path=f"/apis/experimantal.giantswarm.com/v1/ghosts", timeout_seconds=90000):

            # print(f"event: {json.dumps(event, indent=2)}")

            if event['type'] == "ADDED" and event['object']['kind'] == kind:
                self.apply_templates(
                    path=Path(os.path.dirname(__file__)) / ".." / "thirdparties" / kind.lower() / "manifests",
                    values=event['object'])

            # FIXME check regularly for absent `ghost`s
            # and compare to selectors. in case delete event is missed
            #
            # or: just cleanup orphans
            #
            elif event['type'] == "DELETED" and event['object']['kind'] == kind:
                # print(f"DELETE")
                # print(f"event: {json.dumps(event, indent=2)}")
                self.delete_thirdparty(event['object'])

            else:
                print(f"event: {json.dumps(event, indent=2)}")


@click.command()
@click.option('--context', help='kubectl context to use.')
@click.option('--api-version', help='Thirdparty api-version to watch.')
@click.option('--kind', help='Thirdparty kind to watch.')
@click.option('--namespace', default=None, help='Namespace to watch. Use None for All')

def click(context, api_version, kind, namespace):
    operator = Operator(context)
    operator.watch_thirdparty(api_version, kind, namespace)


if __name__ == '__main__':
    click()
