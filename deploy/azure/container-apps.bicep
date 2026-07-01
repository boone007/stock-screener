@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Environment name (dev/staging/prod)')
param environment string = 'prod'

@description('ACR login server (e.g. myacr.azurecr.io)')
param acrLoginServer string

@description('ACR username')
param acrUsername string

@secure()
@description('ACR password')
param acrPassword string

@description('Backend image tag')
param backendImageTag string = 'latest'

@description('Frontend image tag')
param frontendImageTag string = 'latest'

@description('Data source: mock or real')
param dataSource string = 'mock'

// ── Log Analytics Workspace ───────────────────────────────────────────────────
resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'zen-screener-logs-${environment}'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

// ── Container Apps Environment ────────────────────────────────────────────────
resource caEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'zen-screener-env-${environment}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logWorkspace.properties.customerId
        sharedKey: logWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// ── Redis Cache ───────────────────────────────────────────────────────────────
resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: 'zen-redis-${environment}'
  location: location
  properties: {
    sku: { name: 'Basic', family: 'C', capacity: 0 }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
  }
}

var redisUrl = 'rediss://:${redisCache.listKeys().primaryKey}@${redisCache.properties.hostName}:6380/0'

// ── Backend Container App ─────────────────────────────────────────────────────
resource backendApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'zen-backend-${environment}'
  location: location
  properties: {
    managedEnvironmentId: caEnvironment.id
    configuration: {
      registries: [{
        server: acrLoginServer
        username: acrUsername
        passwordSecretRef: 'acr-password'
      }]
      secrets: [
        { name: 'acr-password', value: acrPassword }
        { name: 'redis-url', value: redisUrl }
      ]
      ingress: {
        external: true
        targetPort: 8000
        transport: 'http'
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'OPTIONS']
          allowedHeaders: ['*']
        }
      }
    }
    template: {
      containers: [{
        name: 'backend'
        image: '${acrLoginServer}/zen-backend:${backendImageTag}'
        resources: { cpu: json('0.5'), memory: '1Gi' }
        env: [
          { name: 'ENVIRONMENT', value: environment }
          { name: 'DATA_SOURCE', value: dataSource }
          { name: 'REDIS_URL', secretRef: 'redis-url' }
          { name: 'ALLOWED_ORIGINS', value: 'https://zen-frontend-${environment}.azurecontainerapps.io' }
        ]
        probes: [{
          type: 'Liveness'
          httpGet: { path: '/health', port: 8000 }
          initialDelaySeconds: 15
          periodSeconds: 30
        }]
      }]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: [{
          name: 'http-scale'
          http: { metadata: { concurrentRequests: '20' } }
        }]
      }
    }
  }
}

// ── Frontend Container App ────────────────────────────────────────────────────
resource frontendApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'zen-frontend-${environment}'
  location: location
  properties: {
    managedEnvironmentId: caEnvironment.id
    configuration: {
      registries: [{
        server: acrLoginServer
        username: acrUsername
        passwordSecretRef: 'acr-password'
      }]
      secrets: [{ name: 'acr-password', value: acrPassword }]
      ingress: {
        external: true
        targetPort: 3000
        transport: 'http'
      }
    }
    template: {
      containers: [{
        name: 'frontend'
        image: '${acrLoginServer}/zen-frontend:${frontendImageTag}'
        resources: { cpu: json('0.5'), memory: '1Gi' }
        env: [{
          name: 'NEXT_PUBLIC_API_URL'
          value: 'https://${backendApp.properties.configuration.ingress.fqdn}'
        }]
      }]
      scale: {
        minReplicas: 1
        maxReplicas: 3
        rules: [{
          name: 'http-scale'
          http: { metadata: { concurrentRequests: '30' } }
        }]
      }
    }
  }
}

output frontendUrl string = 'https://${frontendApp.properties.configuration.ingress.fqdn}'
output backendUrl string = 'https://${backendApp.properties.configuration.ingress.fqdn}'
output backendDocsUrl string = 'https://${backendApp.properties.configuration.ingress.fqdn}/docs'
