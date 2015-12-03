/*
A KBase module: MyContigCount
This sample module contains one small method - count_contigs.
*/

module MyContigCount {
	/*
	A string representing a ContigSet id.
	*/
	typedef string contigset_id;
	
	/*
	A string representing a workspace name.
	*/
	typedef string workspace_name;
	
	typedef structure {
	    int contig_count;
	} CountContigsResults;
	
	/*
	Count contigs in a ContigSet
	contigset_id - the ContigSet to count.
	*/
	funcdef count_contigs(workspace_name,contigset_id) returns (CountContigsResults) authentication required;

	/*
	A string representing an fba model id
	*/
	typedef string fbamodel_id;

	typedef structure {
	    float flux_value;
	} RunFBAResult;
	
	/*
	Run FBA on the model and return the flux value
	*/
	funcdef run_fba(workspace_name,fbamodel_id) returns (RunFBAResult) authentication required;
};