from django.shortcuts import render,redirect
from .models import *
from . import tenants
import pandas as pd
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import *
EU_Demo = ["EU_DEMO","#SECRET#"]
EU_Live = ["EU_LIVE","#SECRET#"]
US_Live = ["US_LIVE","#SECRET#"]
EU_PA_Live = ["EU_PA_LIVE","#SECRET#"]
AU_Live = ["AU_Live","#SECRET#"]


def productsToString(products): #function which concatenates strings of products
    strOfProducts = ''
    for x in products.all():
        strOfProducts+=str(x)+'   '
    return strOfProducts



def exportPandas(request,report,cloud): #function which export data of selected report to excel

    from io import BytesIO as IO
    if report == str(1):
        output = [{'Tenant Name':x.name,'Parent Name':x.parentName,'Products':productsToString(x.products),'Amount of Users':x.users.count(),'Amount of Apps':x.apps.count()} for x in Tenant.objects.all()]
        df = pd.DataFrame(output)
        df = df[['Parent Name', 'Tenant Name', 'Products', 'Amount of Users', 'Amount of Apps']]

        excel_file = IO()

        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(xlwriter, 'sheetname',index=False)

        xlwriter.save()
        xlwriter.close()
        # important step, rewind the buffer or when it is read() you'll get nothing
        # but an error message when you try to open your zero length file in Excel
        excel_file.seek(0)
        # set the mime type so that the browser knows what to do with the file
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename='+str(cloud)+'_report_'+str(report)+'.xlsx'
        return response
    elif report == str(2):
        context = getContext2(cloud)
        output = [{'Product Name': x['name'], 'Active': x['active'], 'Inactive': x['inactive'],
                   'All': str(int(x['active']) +  int(x['inactive'])) } for x in context['products']]
        df = pd.DataFrame(output)
        df = df[['Product Name', 'Active','Inactive', 'All']]

        excel_file = IO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(xlwriter, 'sheetname', index=False)
        xlwriter.save()
        xlwriter.close()
        # important step, rewind the buffer or when it is read() you'll get nothing
        # but an error message when you try to open your zero length file in Excel
        excel_file.seek(0)
        # set the mime type so that the browser knows what to do with the file
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename='+str(cloud)+'_report_'+str(report)+'.xlsx'
        return response

    elif report == str(3):
        context = getContext3(cloud)
        excel_file = IO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        for product in context['products']:
            newContext = []  # special format for excel
            for tenant in product['active']:
                dictToExcel = {
                    'tenantName':tenant,
                    'status':'active',
                }
                newContext.append(dictToExcel)
            for tenant in product['inactive']:
                dictToExcel = {
                    'tenantName':tenant,
                    'status':'inactive',
                }
                newContext.append(dictToExcel)
            output = [{'Tenant Name': x['tenantName'].name, 'Status': x['status']} for x in newContext]
            df = pd.DataFrame(output)
            df = df[['Tenant Name', 'Status']]
            df.to_excel(xlwriter, str(product['name'].replace('/','_')), index=False)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename='+str(cloud)+'_report_'+str(report)+'.xlsx'
        return response

    elif report == str(4):
        context = getContext4(cloud)
        newContext = []
        for x in context['tenants']:
            if str(x['serviceBox']).upper() != 'None'.upper():
                newContext.append(x)
        output = [{'Tenant Name':x['name'],'Parent Name':x['parentName'],'Demo':x['demoTenant'],'Service Box':x['serviceBox'],'Installed Version':x['installedVersion'],'Last Updated':x['lastUpdate'],'Products':productsToString(x['products'])} for x in newContext]
        df = pd.DataFrame(output)
        df = df[['Parent Name', 'Tenant Name', 'Demo', 'Service Box', 'Installed Version','Last Updated','Products']]

        excel_file = IO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(xlwriter, 'sheetname',index=False)

        xlwriter.save()
        xlwriter.close()
        # important step, rewind the buffer or when it is read() you'll get nothing
        # but an error message when you try to open your zero length file in Excel
        excel_file.seek(0)
        # set the mime type so that the browser knows what to do with the file
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename='+str(cloud)+'_report_'+str(report)+'.xlsx'
        return response






def updateDatabse(cloudName): #function which updates the wholce database, it takes a long time.
    CLOUD = EU_Demo
    if cloudName == EU_Live[0]:
        CLOUD = EU_Live
    elif cloudName == US_Live[0]:
        CLOUD = US_Live
    elif cloudName == EU_PA_Live[0]:
        CLOUD = EU_PA_Live
    elif cloudName == AU_Live[0]:
        CLOUD = AU_Live
    #update clouds
    cloud = TenantCloud(cloudName=EU_Demo[0])
    cloud.save()
    cloud = TenantCloud(cloudName=EU_Live[0])
    cloud.save()
    cloud = TenantCloud(cloudName=US_Live[0])
    cloud.save()
    cloud = TenantCloud(cloudName=EU_PA_Live[0])
    cloud.save()
    cloud = TenantCloud(cloudName=AU_Live[0])
    cloud.save()

    #admin = (####)
    #first we have to delete tenants to make sure everything is updated and database contains only current data from servers
    TENANTS_OF_CLOUD = tenants.CreatorofCloudUsers(CLOUD)
    tenantsOBJ = Tenant.objects.all()
    for tenantOBJ in tenantsOBJ:
        if str(tenantOBJ.cloud)==str(CLOUD[0]):
            tenantOBJ.delete()

    cloudOBJ = TenantCloud(cloudName=str(CLOUD[0]))

    print('Updating Database ...')
    for tenant in TENANTS_OF_CLOUD:


        serviceBoxObj = TenantServiceBoxName(serviceBoxName=tenant.serviceBoxName)
        serviceBoxObj.save()
        new_tenant = Tenant(name=tenant.name, tenantID=tenant.id,
                            parentID=tenant.parentID, tenantDescription=tenant.description,
                            leaf=tenant.leaf, cloud=cloudOBJ,parentName=tenant.parentName,demoTenant=tenant.demoTenant,
                            serviceBox=serviceBoxObj,installedVersion=tenant.installedVersion,lastUpdate= str(tenant.lastUpdate))
        new_tenant.save()
        for tenantConn in tenant.connections:
            new_conn = TenantConnections(connectionName=str(tenantConn))
            new_conn.save()
            new_tenant.tenantConnections.add(new_conn)
        for tenantProduct in tenant.products:
            new_product = TenantProducts(productName=str(tenantProduct))
            new_product.save()
            new_tenant.products.add(new_product)
        for tenantApp in tenant.apps:
            new_app = TenantApps(appName=str(tenantApp))
            new_app.save()
            new_tenant.apps.add(new_app)
        for tenantUser in tenant.users:
            new_user = TenantUsers(userName=str(tenantUser))
            new_user.save()
            new_tenant.users.add(new_user)
        new_tenant.save()
    print("Database updated")


def getContext1(cloudName):
    tenants = []
    tenantsOBJ = Tenant.objects.all()
    for tenantOBJ in tenantsOBJ:
        tenant = {
            'name': tenantOBJ.name,
            'tenantID': tenantOBJ.tenantID,
            'parentID': tenantOBJ.parentID,
            'parentName': tenantOBJ.parentName,
            'description': tenantOBJ.tenantDescription,
            'connections': tenantOBJ.tenantConnections.all(),
            'leaf':tenantOBJ.leaf,
            'products':tenantOBJ.products.all(),
            'apps':tenantOBJ.apps.all(),
            'users':tenantOBJ.users.all(),
            'cloud':tenantOBJ.cloud,
            'demoTenant': tenantOBJ.demoTenant,

        }

        if str(tenant['cloud']) == str(cloudName):
            tenants.append(tenant)

    context = {'tenants': tenants,'cloud':cloudName,'report':1}
    return context

def checkingIfProdutNotIncluded(newProduct,products): #if reutrn true then we can add product
    for pr in products:
        if pr['name'] == newProduct:
            return False
    return True

def getContext2(cloudName): #context for the report number 2 , counting products per cloud
    products = []
    productsOBJ = TenantProducts.objects.all() #gettin all the names of products of current cloud
    for pr in productsOBJ:
        newPr = str(pr).replace('ACTIVE ','')
        PRODUCT = {
            'name' : newPr,
            'active':0,
            'inactive':0,
        }
        if checkingIfProdutNotIncluded(newPr,products):
            products.append(PRODUCT)
    for pr in products: #count active and inactive
        #first inactive
        x = TenantProducts.objects.get(productName=str(pr['name']))
        pr['inactive'] = x.tenant_set.filter(demoTenant=False, leaf=True,cloud=str(cloudName)).exclude(name__icontains='root').count()
        #active
        nameOfActivePr= str('ACTIVE '+str(pr['name']))
        try:
            x = TenantProducts.objects.get(productName=nameOfActivePr)
            pr['active'] = x.tenant_set.filter(demoTenant=False, leaf=True,cloud=str(cloudName)).exclude(name__icontains='root').count()
        except: pr['active'] = 0
    context = {'products':products,'cloud':cloudName,'report':2}
    return context

def getContext3(cloudName):
    products = []
    productsOBJ = TenantProducts.objects.all()
    for pr in productsOBJ:
        newPr = str(pr).replace('ACTIVE ','')
        PRODUCT = {
            'name' : newPr,
            'active':[],
            'inactive':[],
        }
        if checkingIfProdutNotIncluded(newPr,products):
            products.append(PRODUCT)

    for pr in products: #count active and inactive
        #first inactive
        x = TenantProducts.objects.get(productName=str(pr['name']))
        pr['inactive'] = x.tenant_set.filter(demoTenant=False, leaf=True,cloud=str(cloudName)).exclude(name__icontains='root')
        #active
        nameOfActivePr= str('ACTIVE '+str(pr['name']))
        try:
            x = TenantProducts.objects.get(productName=nameOfActivePr)
            pr['active'] = x.tenant_set.filter(demoTenant=False, leaf=True,cloud=str(cloudName)).exclude(name__icontains='root')
        except: pr['active'] = []
    context = {'products':products,'cloud':cloudName,'report':3}

    return context

def getContext4(cloudName):
    tenants = []
    tenantsOBJ = Tenant.objects.all()
    for tenantOBJ in tenantsOBJ:
        tenant = {
            'name': tenantOBJ.name,
            'parentName': tenantOBJ.parentName,
            'leaf':tenantOBJ.leaf,
            'cloud':tenantOBJ.cloud,
            'demoTenant': tenantOBJ.demoTenant,
            'serviceBox':tenantOBJ.serviceBox,
            'installedVersion':tenantOBJ.installedVersion,
            'lastUpdate':tenantOBJ.lastUpdate,
            'products': tenantOBJ.products.all(),
        }

        if str(tenant['cloud']) == str(cloudName):
            tenants.append(tenant)

    context = {'tenants': tenants,'cloud':cloudName,'report':4}
    return context




def home(request):
    if request.method == 'POST': #it is equal to click submit button
        form = CloudAndReportForm(request.POST) #get the choosen information
        if form.is_valid(): #checking if users gave all the info
            chosenOption = {
                'cloud': form.cleaned_data.get('cloud'),
                'report': form.cleaned_data.get('report')
            }
            return HttpResponseRedirect('report/'+str(chosenOption['cloud'])+'/'+str(chosenOption['report']))
        else: print("NOT VALID FORM")
    else:
        form = CloudAndReportForm()
    return render(request,'cloudviewer/homepage.html',{'form':form})

def report(request,cloud,report):
    context = {}
    if request.method == 'POST':
        updateDatabse(cloud)
    if report == str(1) :
        context = getContext1(cloud)
    if report == str(2):
        context = getContext2(cloud)
    if report == str(3):
        context = getContext3(cloud)
    if report == str(4):
        context = getContext4(cloud)
    return render(request, 'cloudviewer/report' + str(report) + '.html', context)




