from django.db import models

# All the classes which are used to create the whole database
# Django automatically creates SQL code based on them (all the tables and relation are included)
class TenantConnections(models.Model):
    connectionName = models.CharField(max_length=300,primary_key=True)
    def __str__(self):
        return self.connectionName

class TenantProducts(models.Model):
    productName = models.CharField(max_length=300,primary_key=True)

    def __str__(self):
        return self.productName

class TenantApps(models.Model):
    appName = models.CharField(max_length=300,primary_key=True)

    def __str__(self):
        return self.appName

class TenantUsers(models.Model):
    userName = models.CharField(max_length=300,primary_key=True)

    def __str__(self):
        return self.userName

class TenantCloud(models.Model):
    cloudName = models.CharField(max_length=300,primary_key=True)
    def __str__(self):
        return self.cloudName

class TenantServiceBoxName(models.Model):
    serviceBoxName = models.CharField(max_length=300, primary_key=True)
    def __str__(self):
        return self.serviceBoxName

class Tenant (models.Model):
    name = models.CharField(max_length=100)
    parentName = models.CharField(max_length=250,null=True,blank=True)
    tenantID = models.CharField(max_length=250,null=True,blank=True)
    parentID = models.CharField(max_length=250,null=True,blank=True)
    tenantDescription = models.CharField(max_length=250,null=True,blank=True)
    tenantConnections = models.ManyToManyField(TenantConnections)
    leaf = models.BooleanField(default=False)
    demoTenant = models.BooleanField(default=False)
    products= models.ManyToManyField(TenantProducts)
    apps = models.ManyToManyField(TenantApps)
    users = models.ManyToManyField(TenantUsers)
    cloud = models.ForeignKey(TenantCloud,on_delete=models.CASCADE)
    serviceBox = models.ForeignKey(TenantServiceBoxName,on_delete=models.CASCADE,null=True, blank=True)
    installedVersion = models.CharField(max_length=250, null=True, blank=True)
    lastUpdate = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return str(self.cloud)+ ' | ' + str(self.name)

    






