from .context import kubeop
import os
# import unittest

# $ cd tests/ghost/
# $ docker run -v $HOME/.kube:/root/.kube -ti local/python-operator python


# FIXME
# start operator/controller as deployment in the cluster
# for a specific api_version
# then apply test-manifests
#

context = "l8"
operator = kubeop.kubeop.Operator(context)
# operator.watch_thirdparty(api_version, kind, namespace)


values = {
    "metadata": {
        "name": "ghost-operator-test-a",
        "namespace": "ghost-operator-test-a"
    },
    "command": "kubeop --context=l8 --api-version=ghost-operator-test-a.giantswarm.com/v1 --kind=ghost --namespace=ghost-operator-test-a".split(" ")
}

# FIXME belongs to generic_api
# operator.apply_template("tests/ghost/operator", "deployment.templ.yaml", values)
operator.apply_template("operator", "deployment.templ.yaml", values)


thirdparty_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../thirdparty/ghost'))

print(thirdparty_path)

print(kubeop)

if __name__ == '__main__':
    # unittest.main()
    context = "l8"
    api_version = "experimantal.giantswarm.com/v1"
    kind = "Ghost"
    namespace = None

    import pdb; pdb.set_trace()

    op = kubeop.Operator(context)
    op.watch_thirdparty(api_version, kind, namespace)


    # FIXME! in background..
