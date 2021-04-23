#ZENO-AK
#imports the intrinio sdk
import intrinio_sdk as sdk
#screener method
def screen():
    #api config
    sdk.ApiClient().configuration.api_key['api_key'] = 'Ojg5YTMwZTNmYzA3Nzc3MTZkNmNkN2I1YzdjZDllODcw'
    
    secApi = sdk.SecurityApi()
    
    
    #json body of screener clauses and info
    clause1 = {"operator": "AND",
               "clauses": [
                               {
                                   "field" : "close_price",
                                   "operator" : "gt",
                                   "value" : "25"
                               },               
                               {
                                   "field" : "close_price",
                                   "operator" : "lte",
                                   "value" : "200"
                               },
                               {
                                   "field" : "volume",
                                   "operator" : "gt",
                                   "value" : "2000000"
                               }
                                
                          ]
               }
    
    
    #gets the screener results in order of volume(highest to lowest)
    response = secApi.screen_securities(logic=clause1, order_column = 'volume', order_direction="desc" )
    #returns the list of stocks
    
    return response
response = screen()

