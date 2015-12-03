import unittest
import os
import json
import time

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from biokbase.fbaModelServices.Client import fbaModelServices as fbaService
from MyContigCount.MyContigCountImpl import MyContigCount


class MyContigCountTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.ctx = {'token': token}
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MyContigCount'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = MyContigCount(cls.cfg)
        cls.fbaURL = cls.cfg['fba-url']
        cls.fbaClient = fbaService(cls.fbaURL, token=token)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getFBAClient(self):
        return self.__class__.fbaClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_MyContigCount_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def est_count_contigs(self):
        obj_name = "contigset.1"
        contig = {'id': '1', 'length': 10, 'md5': 'md5', 'sequence': 'agcttttcat'}
        obj = {'contigs': [contig], 'id': 'id', 'md5': 'md5', 'name': 'name', 
                'source': 'source', 'source_id': 'source_id', 'type': 'type'}
        self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects':
            [{'type': 'KBaseGenomes.ContigSet', 'name': obj_name, 'data': obj}]})
        ret = self.getImpl().count_contigs(self.getContext(), self.getWsName(), obj_name)
        self.assertEqual(ret[0]['contig_count'], 1)
        return ret
        
    def test_run_fba(self):
        obj_name = "test.1"
        sbml = open("testmodel.xml").read()
        self.getFBAClient().import_fbamodel({'workspace':self.getWsName(), 'genome':'Rhodobacter_sphaeroides_2.4.1', 'genome_workspace':'KBaseExampleData', 'model':obj_name, 'biomass':'biomass0', 'sbml':sbml})
        ret = self.getImpl().run_fba(self.getContext(), self.getWsName(), obj_name)
        self.assertEqual(ret[0]['flux_value'], 500.0)
        self.assertEqual(ret[0]['MFALog'], 'Shutting down mass-imbalanced reaction: my99994-c_c0 [C]')
        return ret
