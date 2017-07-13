
docker build --tag giantswarm/python-operator-test:db1 ./tests/database
docker push giantswarm/python-operator-test:db1


kubectl --context l8 apply --recursive --filename tests/database/manifests/operator
kubectl --context l8 --namespace dbop get pods


kubectl --context l8 delete namespace dbop


---
import dbop

dbop.kubernetes.client.configuration.api_key
dbop.kubernetes.client.configuration.ssl_ca_cert

dbop.kubernetes.config.load_incluster_config()

dbop.kubernetes.client.configuration.api_key
dbop.kubernetes.client.configuration.ssl_ca_cert

dbop.kubernetes.client.CoreV1Api().list_pod_for_all_namespaces(watch=False)

op = dbop.Operator(context=None)

op.generic.api_client.config.api_key

op.generic.api_client.call_api("/api/v1", "GET")

---
import dbop
dbop.kubernetes.config.load_incluster_config()
dbop.kubernetes.client.CoreV1Api().list_pod_for_all_namespaces(watch=False)

---
import dbop
dbop.kubernetes.client.CoreV1Api().list_pod_for_all_namespaces(watch=False)

---
import dbop
api_client = dbop.kubernetes.client.ApiClient()
dbop.kubernetes.client.CoreV1Api(api_client).list_pod_for_all_namespaces(watch=False)

dbop.kubernetes.config.load_incluster_config()
api_client = dbop.kubernetes.client.ApiClient()
dbop.kubernetes.client.CoreV1Api(api_client).list_pod_for_all_namespaces(watch=False)

from generic_api import GenericApi
GenericApi(api_client).call_api("/", "GET")


dbop.kubernetes.client.ApiClient().call_api("/", "GET")


dbop.kubernetes.client.ApiClient(config=dbop.kubernetes.config.incluster_config.configuration).call_api("/", "GET")

---
import dbop
dbop.kubernetes.config.load_incluster_config()
api_client = dbop.kubernetes.client.ApiClient()

from generic_api import GenericApi
GenericApi(api_client).call_api("/", "GET")

GenericApi(api_client).call_api("/", "GET", auth_settings=["BearerToken"])
