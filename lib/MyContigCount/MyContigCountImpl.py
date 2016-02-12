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

    def run_fba(self, ctx, workspace_name, fbamodel_id, elements):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_fba
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)

        # load the method provenance from the context object
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[workspace_name+'/'+fbamodel_id]

        fbaClient = fbaService(self.fbaURL, token=token)
        res = fbaClient.runfba({'workspace':workspace_name, 'model':fbamodel_id, 'massbalance':elements})
        fbaobj = wsClient.get_objects([{'ref': workspace_name+'/'+res[1]}])[0]
        reportMessage = "No mass imbalance found"
        if len(fbaobj['data']['MFALog']) > 0 :
            reportMessage = fbaobj['data']['MFALog']
    
        reportObj = {
            'objects_created':[{'ref':workspace_name+'/'+str(fbaobj['info'][0]), 'description':'FBA output'}],
            'text_message':reportMessage
        }

        reportName = 'massbalance_report_'+fbamodel_id
        report_obj_info = wsClient.save_objects({
                'id':fbaobj['info'][6],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1,
                        'provenance':provenance
                    }
                ]
            })[0]

        returnVal = { 'report_name': reportName, 'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]) }

        #END run_fba

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_fba return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
