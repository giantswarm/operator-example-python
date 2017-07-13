from .context import kubeop
# import kubeop


import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == '__main__':
    # unittest.main()
    context = "l8"
    api_version = "experimantal.giantswarm.com/v1"
    kind = "Ghost"
    namespace = None

    op = kubeop.Operator(context)
    op.watch_thirdparty(api_version, kind, namespace)
    # FIXME! in background..

    

# idea:
# use different thirdparty resources
# like ghost-testrun-{random-hex}.experimantal.giantswarm.com
#
# so different tests/versions may run in parallel \o/!!




# get apiserver/context to use

# bring up local/opy -> giantswarm/operator-python
# should this ensure ghost.experimantal.giantswarm.com exists? yes

# create two ghost instances

# test ingress addresses

# take down both

# including namespaces

# remove ghost.experimantal.giantswarm.com
# and deployment for operator

# if __name__ == '__main__':
#     print(kubeop)
#     op = operator.Operator(context)
#     op.watch_thirdparty(api_version, kind, namespace)
