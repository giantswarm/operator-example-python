# Kubernetes Operator

Experimantal example written in Python. Work in progress. Improve me if you like :)


Some commands to test:

```bash
docker build --tag local/opy .


kubectl apply --filename ./ghost/ghost-thirdparty.yaml

docker run -v $HOME/.kube:/root/.kube -t local/opy python opy.py \
  --api-version experimantal.giantswarm.com/v1 \
  --kind Ghost

kubectl create --filename ./ghost/ghost-1.yaml

kubectl create --filename ./ghost/ghost-2.yaml

kubectl get --all-namespaces ghosts


kubectl get --all-namespaces ingress -o wide

kubectl run -ti --rm tiny-tools --image giantswarm/tiny-tools curl ghost-1.ghost-test-1.svc:2368


kubectl --namespace ghost-test-1 delete ghost ghost-1

kubectl --namespace ghost-another-test delete ghost ghost-2

kubectl delete thirdpartyresource ghost.experimantal.giantswarm.com

kubectl delete namespace --now ghost-test-1

kubectl delete namespace --now ghost-another-test

kubectl get namespaces

```

## Todo

- Create Docker image for the `python-operator`
- Decide on naming this thing
- Add helper to list all the resources within a namespace
- Clean up code, add proper logging, more exception handling
- Decide how to identify orphans. In case not everything got deleted on the first try.
