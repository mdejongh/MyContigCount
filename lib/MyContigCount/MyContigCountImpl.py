#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
from biokbase.fbaModelServices.Client import fbaModelServices as fbaService
#END_HEADER


class MyContigCount:
    '''
    Module Name:
    MyContigCount

    Module Description:
    A KBase module: MyContigCount
This sample module contains one small method - count_contigs.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    fbaURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.fbaURL = config['fba-url']
        #END_CONSTRUCTOR
        pass

    def count_contigs(self, ctx, workspace_name, contigset_id):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN count_contigs
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        contigSet = wsClient.get_objects([{'ref': workspace_name+'/'+contigset_id}])[0]['data']
        returnVal = {'contig_count': len(contigSet['contigs'])}
        #END count_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method count_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def run_fba(self, ctx, workspace_name, fbamodel_id):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_fba
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        print self.fbaURL
        fbaClient = fbaService(self.fbaURL, token=token)
        res = fbaClient.runfba({'workspace':workspace_name, 'model':fbamodel_id})
        fbaobj = wsClient.get_objects([{'ref': workspace_name+'/'+res[1]}])[0]['data']
        returnVal = {'flux_value': fbaobj['objectiveValue'], 'mfa_log': fbaobj['MFALog']}
        #END run_fba

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_fba return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
