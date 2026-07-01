@description('Azure region')
param location string = resourceGroup().location

@description('ACR name (globally unique, alphanumeric only)')
param acrName string = 'zenscreeneracr'

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: { name: 'Basic' }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
    policies: {
      retentionPolicy: {
        status: 'enabled'
        days: 30
      }
    }
  }
}

output acrLoginServer string = acr.properties.loginServer
output acrName string = acr.name
