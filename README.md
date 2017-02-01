# Kubernetes Operator

Experimantal example written in Python. Work in progress. Improve me if you like :)


Some commands to test:

```bash
docker build --tag local/opy .

context="my-kubectl-config-context"


kubectl --context $context apply --filename ./ghost/ghost-thirdparty.yaml

docker run -v $HOME/.kube:/root/.kube -t local/opy python opy.py \
  --context $context \
  --api-version experimantal.giantswarm.com/v1 \
  --kind Ghost

kubectl --context $context create --filename ./ghost/ghost-1.yaml

kubectl --context $context create --filename ./ghost/ghost-2.yaml

kubectl --context $context get --all-namespaces ghosts


kubectl --context $context get --all-namespaces ingress -o wide

kubectl --context $context run -ti --rm tiny-tools --image giantswarm/tiny-tools curl ghost-1.ghost-test-1.svc:2368


kubectl --context $context --namespace ghost-test-1 delete ghost ghost-1

kubectl --context $context --namespace ghost-another-test delete ghost ghost-2

kubectl --context $context delete thirdpartyresource ghost.experimantal.giantswarm.com

kubectl --context $context delete namespace --now ghost-test-1

kubectl --context $context delete namespace --now ghost-another-test

kubectl --context $context get namespaces

```
