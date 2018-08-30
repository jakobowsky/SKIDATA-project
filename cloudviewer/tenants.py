import requests
import time
from bs4 import BeautifulSoup
import datetime
import dateutil.parser
import pandas as pd

# admin = # ADMIN credentials #

class mdict(dict): #my helping class which provides me function to add items to array in dictionary

    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)


############################################################
####################### PART 1 #############################
################### TENANTS CREATOR  #######################
############################################################
class CloudTenant: #Class which represents tenant of selected cloud
    def __init__(self,JSONdata,cloud):
        self.name = JSONdata['name']
        self.description = JSONdata['description']
        self.id = JSONdata['id']
        self.parentID = JSONdata['parentID']
        self.parentName = '' #we dont know the name of parent, we know only his id, we will define it with the function
        self.users = []
        self.numberOfUsers = 0 #we will count the number of users who are under the current tenant
        self.cloud = cloud #selected cloud
        self.connections = [] #connections of the tenant, we will find them with the function
        self.products = []
        self.productStr = '' # the additional string, concatenation of products
        self.apps = []  # the apps of tenant
        self.leaf = False #leaf means that the current tenant doesn't have any more 'under' tenants (children in tree)
        #links for API requests:
        self.USERS_LINK = str(cloud[1]) +'#LINK#' + str(self.id) + '/users'
        self.CONNECTIONS_LINK = str(cloud[1]) +'#LINK#' + str(self.id) + '/connections'
        self.APPS_LINK = str(cloud[1]) +'#LINK#' + str(self.id) + '/applications'
        self.demoTenant = False # if the tenant is demo
        self.serviceBoxName = 'None'
        self.installedVersion = 'None'
        self.lastUpdate = 'None'
    def attributeUsers(self):
        r = requests.get(self.USERS_LINK,auth=admin) #getting info from the website
        usersJSON = r.json()  #exporting info to json format
        for x in usersJSON: #adding users to array
            self.users.append(x["login"])
        self.numberOfUsers = len(usersJSON) #checking how many users are in current tenant
    def attributeProductStr(self):
        for x in self.products:
            self.productStr+=str(x)+ " | "
    def changeLeaf(self):
        self.leaf = True
    def changeDemoTenant(self):
        self.demoTenant = True



def createCloudTenants(cloud): #Creating array of cloudTenants of selected cloud
    tenantsOfCloud = []
    TENANTS_LINK = '#LINK#'
    tenants = str(cloud[1])+str(TENANTS_LINK)
    try:
        r = requests.get(tenants,auth=admin) #API REQUEST
        jsonFullData = r.json()
        for tenant in jsonFullData: #iterating through whole tenants in the cloud
            tenantsOfCloud.append(CloudTenant(tenant,cloud)) #creating objects in array
        return tenantsOfCloud
    except:
        print(' smth went wrong with creating tenants \n')
        return 0

def attributeParents(tenantsOfCloud): #functions which find every parent of tenant
    for tenant in tenantsOfCloud: #iterating throught every tenant
        for parent in tenantsOfCloud:  #checking every tenant for each tenant to find parent name
            if tenant.id != parent.id and tenant.parentID == parent.id:
                tenant.parentName = parent.name
                break
    for tenant in tenantsOfCloud:
        if tenant.parentName == '':
            tenant.parentName='None' #if tenant has no parent then attribute 'None"
    return tenantsOfCloud

def attributeAmountOfUsers(tenantsOfCloud): #calling function for every tenant
    for tenant in tenantsOfCloud:
        try:
            tenant.attributeUsers()
        except:
            print(' smth went wrong with attributing users for tenant:'+str(tenant.name)+ '\n ')
    return tenantsOfCloud

def attributeConnections(tenantsOfCloud):
    for tenant in tenantsOfCloud:
        try:
            r = requests.get(tenant.CONNECTIONS_LINK,auth=admin) #making requsts to get connections of selected tenant
            connections = r.json() #export to json format
            for conn in connections:
                tenant.connections.append(conn['systemName']) #attributing connections for tenants
        except:
            print(' smth went wrong with attributing connections to tenant:'+ str(tenant.name)+'\n')
    return tenantsOfCloud

def checkLeaves(tenantsOfCloud):
    graph = mdict()  #create speciall structure wich represents graph of tenants to define which tenants are leaves
    for tenant in tenantsOfCloud:
        if tenant.parentID == None:
            graph[tenant.id] = None
        else:
            graph[tenant.parentID] = tenant.id
    for tenant in tenantsOfCloud:
        if tenant.id not in graph:
            graph[tenant.id] = None

    for tenant in graph.values():
        if None in tenant:
            tenant.remove(None)

    for tenant in tenantsOfCloud:
        if tenant.id in graph and not graph[tenant.id]: #if tenant is in graph and it has no children then it is a leaf
            tenant.changeLeaf()
    return tenantsOfCloud

def attributeProducts(tenantsOfCloud): #function which attribute products for every tenant
    for tenant in tenantsOfCloud:
        if tenant.leaf == True:
            if '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#')
            elif '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#') # not sure about name
            if '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#')
            elif '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections and '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#')
            if '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#')
            if '#SECRET#' in tenant.connections:
                tenant.products.append('#SECRET#')
        tenant.attributeProductStr()
    return tenantsOfCloud

def attributeApps(tenantsOfCloud):
    for tenant in tenantsOfCloud:
        try:
            r = requests.get(tenant.APPS_LINK,auth=admin) #making API Request for apps of tenant
            appJson = r.json() #getting apps for every tenant
            for app in appJson: #getting json format
                if app['applicationId'] == "#SECRET#" or app['label'] == "#SECRET#": #checking if it is demo tenant
                    tenant.changeDemoTenant()
                tenant.apps.append(app['applicationId'])
        except:
            print(' smth went wrong with attributing apps for tenant: '+ str(tenant.name)+'\n')
    return tenantsOfCloud

def attributeActiveProducts(tenantsOfCloud,cloud): #checking if the products are active
    for tenant in tenantsOfCloud: #iterate though every tenant
        if tenant.demoTenant == False: #demo tenant cannot be counted as active
            if '#SECRET#' in tenant.products or '#SECRET#' in tenant.products:
                r = requests.get(
                    str(cloud[1]) + '#LINK#' + str(
                        tenant.name), auth=admin)
                info = r.json()
                checked = False
                for row in info:
                    if (checked):
                        break
                    try:
                        if '#SECRET#' in row['name']:
                            id = row['id']
                            r = requests.get(str(cloud[1])+'#LINK#'+str(id)+'#SECRET#',auth=admin)
                            states = r.json()
                            for state in states['monitoringState']: #if the state is equel RUNNING then product is active
                                if str(state['state']) == '#SECRET#':
                                    if '#SECRET#' in tenant.products:
                                        tenant.products.remove('#SECRET#')
                                        tenant.products.append('#SECRET#')

                                    else:
                                        tenant.products.remove('#SECRET#')
                                        tenant.products.append('#SECRET#')

                                    checked = True #if one is running then we dont have to check the rest
                                    break
                    except: print(' smth wrong with checking sweb.Control active for tenant : '+str(row) + " "+str(tenant.name) + '\n' )

            if  '#SECRET#' in tenant.products or '#SECRET#' in tenant.products:
                ########## SOAP REQUEST #########
                body = """<soapenv:Envelope xmlns:soapenv="#LINK#" xmlns:soap="#LINK#" xmlns:con="#LINK#">
                                      <soapenv:Header>
                                         <soap:AuthenticationHeader>
                                            <soap:ClientName>#SECRET#</soap:ClientName>
                                            <soap:UserName>#SECRET#</soap:UserName>
                                            <soap:Password>#SECRET#</soap:Password>
                                         </soap:AuthenticationHeader>
                                      </soapenv:Header>
                                      <soapenv:Body>
                                         <con:#SECRET#>
                                            <con:#SECRET#>%s</con:#SECRET#>
                                         </con:#SECRET#>
                                      </soapenv:Body>
                                   </soapenv:Envelope>""" % (tenant.name)
                urlForDTA = str(cloud[1])+'#LINK#'

                headers = {
                    'content-type': 'text/xml',
                    'Accept-Encoding': 'gzip,deflate',
                    'Content-Type': 'text/xmlcharset=UTF-8',
                    'SOAPAction': '#SECRET#',
                    'User-Agent': '#SECRET#'}
                try:
                    response = requests.post(urlForDTA, data=body, headers=headers)  # FULL SOAP REQUEST
                    dateText = BeautifulSoup(response.content, features='xml').#SECRET#.get_text() #checking the method called #SECRET#
                    dateParsed = dateutil.parser.parse(dateText).strftime('%x')  # parsed date, format for comparing
                    dateToCompare = datetime.datetime.strptime(dateParsed, '%x')
                    todayDate = datetime.datetime.now()

                    if ((todayDate - dateToCompare) < datetime.timedelta(
                            days=30)):  # if the date is not  older than 30 days then product is active
                        if '#SECRET#' in tenant.products:
                            tenant.products.remove('#SECRET#)
                            tenant.products.append('#SECRET#')
                        elif '#SECRET#' in tenant.products:
                            tenant.products.remove('#SECRET#')
                            tenant.products.append('#SECRET#')
                except:
                    print(' smth wrong with checking DTA or sweb.Reserve/Contract for tenant: ' + str(tenant.name) + '\n')
        else:
            print(tenant.name + " is demo Tenant \n")
    return tenantsOfCloud


def attributeServiceBoxes(tenantsOfCloud,cloud):
    for tenant in tenantsOfCloud:
        try:
            idOfServiceBox = ''
            link = str(cloud[1] + '#LINK#' + str(tenant.name))
            r = requests.get(link, auth=admin)  # making API Request for tenant
            for row in r.json():
                if (row['subType']=='#SECRET#'):
                    idOfServiceBox = row['id']
                    tenant.serviceBoxName = row['name']
                    break
            if idOfServiceBox != '':
                link2 = str(cloud[1] + '#LINK#'+str(idOfServiceBox)+'?workingClient='+str(tenant.name))
                r = requests.get(link2, auth=admin)  # making API Request
                output = r.json()
                tenant.installedVersion = (output['#LINK#']['#LINK#'][0]['#LINK#']) #attribute version of box
                dateText = (output['#SECRET#']['#SECRET#'][0]['#SECRET#'])
                dateParsed = dateutil.parser.parse(dateText).strftime('%x')
                tenant.lastUpdate = dateParsed #attribute last update date
        except:
            if tenant.serviceBoxName == '':
                tenant.serviceBoxName = 'None'
                tenant.installedVersion = 'None'
                tenant.lastUpdate = 'None'
            print(' smth went wrong with attributing serviceBox for tenant: ' +str(tenant.name)+ ' \n ')
    return tenantsOfCloud
def CreatorofCloudUsers(cloud): #function for call other functions

    print('NOW: Creating Tenants')
    start = time.time()
    tenantsOfCloud = createCloudTenants(cloud)
    end = time.time()
    print("CreateTenants: "+str(end-start))
    #####################
    print('NOW: Attributing Parents')
    start = time.time()
    tenantsOfCloud = attributeParents(tenantsOfCloud)
    end = time.time()
    print("AttributeParents: " + str(end - start))
    #########################
    print('NOW: Checking leaves')
    start = time.time()
    tenantsOfCloud = checkLeaves(tenantsOfCloud)
    end = time.time()
    print("checkLeaves: " + str(end - start))
    ###################
    print('NOW: Attributing Amount of Users')
    start = time.time()
    tenantsOfCloud = attributeAmountOfUsers(tenantsOfCloud)
    end = time.time()
    print("attributeAmountOfUsers: " + str(end - start))
    #####################
    print('NOW: Attributing Connections')
    start = time.time()
    tenantsOfCloud = attributeConnections(tenantsOfCloud)
    end = time.time()
    print("attributeConnections: " + str(end - start))
    ###############
    print('NOW: Attributing Products')
    start = time.time()
    tenantsOfCloud = attributeProducts(tenantsOfCloud)
    end = time.time()
    print("attributeProducts: " + str(end - start))
    ####################
    print('NOW: Attributing Apps')
    start = time.time()
    tenantsOfCloud = attributeApps(tenantsOfCloud)
    end = time.time()
    print("attributeApps: " + str(end - start))
    ####################
    print('NOW: Attributing Active Products')
    start = time.time()
    tenantsOfCloud = attributeActiveProducts(tenantsOfCloud,cloud)
    end = time.time()
    print("attributeActiveProducts: " + str(end - start))
    ####################
    print('NOW: Attributing Service Boxes')
    start = time.time()  ####
    tenantsOfCloud = attributeServiceBoxes(tenantsOfCloud, cloud)
    end = time.time()
    print("attributeServiceBoxes: " + str(end - start))


    return tenantsOfCloud



