"""
test
--------

Runs tests of matching methods.
"""

import unittest
import yaml
import entwine
import pdb

class ClusterTestDefault(unittest.TestCase):

    def setUp(self):
        config_file = "./tests/config_cluster.yaml"

        with open(config_file, 'r') as f:
            self.config = yaml.load(f)


class ClusterTests(ClusterTestDefault):

    def run_cluster_method(self, method_name):
        self.config['match']['params']['method'] = method_name
        output = entwine.run_from_config(self.config)
        self.assertTrue(output != False)

    def test_order(self):
        self.run_cluster_method('order')

    def test_random(self):
        self.run_cluster_method('random')

    def test_greedy(self):
        self.run_cluster_method('greedy')

    def test_adaptive(self):
        self.run_cluster_method('adaptive')



class AssignTestDefault(unittest.TestCase):

    def setUp(self):
        config_file = "./tests/config_assign.yaml"

        with open(config_file, 'r') as f:
            self.config = yaml.load(f)

class AssignTests(AssignTestDefault):

    def test_assign(self):
        output = entwine.run_from_config(self.config)
        self.assertTrue(output != False)


if __name__ == '__main__':
    unittest.main()