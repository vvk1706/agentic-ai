# Deployment Guide

Comprehensive guide for deploying DataStage pipeline jobs across different environments.

## Table of Contents

- [Overview](#overview)
- [Environment Setup](#environment-setup)
- [Deployment Process](#deployment-process)
- [CI/CD Integration](#cicd-integration)
- [Rollback Procedures](#rollback-procedures)
- [Post-Deployment Validation](#post-deployment-validation)
- [Production Considerations](#production-considerations)
- [Troubleshooting Deployment](#troubleshooting-deployment)

## Overview

This guide covers the complete deployment lifecycle for DataStage pipeline jobs, from development through production.

### Deployment Environments

```
Development → Test → UAT → Production
```

| Environment | Purpose | Characteristics |
|-------------|---------|-----------------|
| **Development** | Active development | Frequent changes, small datasets |
| **Test** | Automated testing | Stable, realistic test data |
| **UAT** | User acceptance | Production-like, business validation |
| **Production** | Live operations | High availability, full datasets |

### Deployment Artifacts

```
Deployment Package:
├── jobs/                    # DataStage job definitions (.dsx)
├── config/                  # Configuration files
│   ├── connections.json
│   ├── parameters.json
│   └── environments/
├── scripts/                 # Deployment scripts
│   ├── deploy.sh
│   ├── rollback.sh
│   └── validate.sh
├── tests/                   # Test suite
├── docs/                    # Documentation
└── CHANGELOG.md            # Version history
```

## Environment Setup

### Prerequisites

#### 1. DataStage Environment

```bash
# Verify DataStage installation
echo $DSHOME
ls -la $DSHOME/bin/dsjob

# Check DataStage version
cat $DSHOME/Version

# Verify engine is running
ps aux | grep dsrpcd
```

#### 2. Database Access

```bash
# Test source database connectivity
psql -h source-db-server -U etl_user -d customers -c "SELECT 1"

# Test target database connectivity
psql -h target-db-server -U dw_user -d warehouse -c "SELECT 1"

# Test control database connectivity
psql -h control-db-server -U etl_admin -d etl_control -c "SELECT 1"
```

#### 3. File System Permissions

```bash
# Create required directories
mkdir -p /data/rejects
mkdir -p /data/staging
mkdir -p /data/archive
mkdir -p /var/log/datastage

# Set permissions
chmod 755 /data/rejects /data/staging /data/archive
chmod 755 /var/log/datastage

# Set ownership
chown -R dsadm:dstage /data/*
chown -R dsadm:dstage /var/log/datastage
```

### Environment Configuration

#### Development Environment

```bash
# Set environment variables
export ETL_ENV=development
export DS_PROJECT=DEV_PROJECT
export DS_SERVER=dev-datastage-server
export LOG_LEVEL=DEBUG

# Load development configuration
source config/environments/dev.env
```

**dev.env**:
```bash
# Database connections
export DB_SOURCE_HOST=dev-source-db
export DB_TARGET_HOST=dev-target-db

# Job parameters
export COMMIT_INTERVAL=100
export PARALLEL_NODES=2
export BATCH_SIZE=1000

# Notification
export EMAIL_RECIPIENTS=dev-team@example.com
```

#### Test Environment

```bash
# Set environment variables
export ETL_ENV=test
export DS_PROJECT=TEST_PROJECT
export DS_SERVER=test-datastage-server
export LOG_LEVEL=INFO

# Load test configuration
source config/environments/test.env
```

#### Production Environment

```bash
# Set environment variables
export ETL_ENV=production
export DS_PROJECT=PROD_PROJECT
export DS_SERVER=prod-datastage-server
export LOG_LEVEL=WARN

# Load production configuration
source config/environments/prod.env
```

**prod.env**:
```bash
# Database connections
export DB_SOURCE_HOST=prod-source-db
export DB_TARGET_HOST=prod-target-db

# Job parameters
export COMMIT_INTERVAL=5000
export PARALLEL_NODES=16
export BATCH_SIZE=10000

# Notification
export EMAIL_RECIPIENTS=prod-alerts@example.com,etl-team@example.com
```

## Deployment Process

### Manual Deployment

#### Step 1: Pre-Deployment Checklist

```markdown
- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Configuration verified
- [ ] Backup created
- [ ] Rollback plan prepared
- [ ] Stakeholders notified
- [ ] Deployment window scheduled
- [ ] Change ticket approved
```

#### Step 2: Create Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/datastage/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup jobs
for job in CUSTOMER_DATA_ETL SALES_DATA_AGGREGATION DATA_QUALITY_VALIDATION \
           INCREMENTAL_LOAD MASTER_DATA_MANAGEMENT; do
  echo "Backing up $job..."
  dsjob -export -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job > $BACKUP_DIR/${job}.dsx
done

# Backup configuration
cp -r config/ $BACKUP_DIR/

# Create backup manifest
cat > $BACKUP_DIR/manifest.txt <<EOF
Backup Date: $(date)
Environment: $ETL_ENV
Project: $DS_PROJECT
Server: $DS_SERVER
Jobs Backed Up:
$(ls -1 $BACKUP_DIR/*.dsx)
EOF

echo "Backup completed: $BACKUP_DIR"
```

#### Step 3: Deploy Jobs

```bash
#!/bin/bash
# deploy.sh

set -e  # Exit on error

DEPLOY_ENV=$1
if [ -z "$DEPLOY_ENV" ]; then
  echo "Usage: $0 <environment>"
  echo "Example: $0 production"
  exit 1
fi

# Load environment configuration
source config/environments/${DEPLOY_ENV}.env

echo "Deploying to $DEPLOY_ENV environment..."
echo "Project: $DS_PROJECT"
echo "Server: $DS_SERVER"

# Import jobs
for job_file in jobs/*.dsx; do
  job_name=$(basename $job_file .dsx)
  echo "Importing $job_name..."
  
  dsjob -import -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job_file
  
  if [ $? -eq 0 ]; then
    echo "✓ $job_name imported successfully"
  else
    echo "✗ Failed to import $job_name"
    exit 1
  fi
done

# Compile jobs
for job_file in jobs/*.dsx; do
  job_name=$(basename $job_file .dsx)
  echo "Compiling $job_name..."
  
  dsjob -compile -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job_name
  
  if [ $? -eq 0 ]; then
    echo "✓ $job_name compiled successfully"
  else
    echo "✗ Failed to compile $job_name"
    exit 1
  fi
done

echo "Deployment completed successfully!"
```

#### Step 4: Validate Deployment

```bash
#!/bin/bash
# validate.sh

echo "Validating deployment..."

# Check job status
for job in CUSTOMER_DATA_ETL SALES_DATA_AGGREGATION DATA_QUALITY_VALIDATION \
           INCREMENTAL_LOAD MASTER_DATA_MANAGEMENT; do
  echo "Checking $job..."
  
  dsjob -jobinfo -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job > /dev/null 2>&1
  
  if [ $? -eq 0 ]; then
    echo "✓ $job exists"
  else
    echo "✗ $job not found"
    exit 1
  fi
done

# Run smoke tests
echo "Running smoke tests..."
cd tests
python smoke_tests.py

if [ $? -eq 0 ]; then
  echo "✓ Smoke tests passed"
else
  echo "✗ Smoke tests failed"
  exit 1
fi

echo "Validation completed successfully!"
```

### Automated Deployment

#### Deployment Script

```bash
#!/bin/bash
# automated_deploy.sh

set -e

ENVIRONMENT=$1
VERSION=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$VERSION" ]; then
  echo "Usage: $0 <environment> <version>"
  echo "Example: $0 production v1.2.0"
  exit 1
fi

echo "========================================="
echo "DataStage Deployment"
echo "========================================="
echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"
echo "Date: $(date)"
echo "========================================="

# Step 1: Pre-deployment checks
echo "Step 1: Pre-deployment checks..."
./scripts/pre_deploy_check.sh $ENVIRONMENT
if [ $? -ne 0 ]; then
  echo "Pre-deployment checks failed"
  exit 1
fi

# Step 2: Create backup
echo "Step 2: Creating backup..."
./scripts/backup.sh $ENVIRONMENT
if [ $? -ne 0 ]; then
  echo "Backup failed"
  exit 1
fi

# Step 3: Deploy jobs
echo "Step 3: Deploying jobs..."
./scripts/deploy.sh $ENVIRONMENT
if [ $? -ne 0 ]; then
  echo "Deployment failed"
  echo "Initiating rollback..."
  ./scripts/rollback.sh $ENVIRONMENT
  exit 1
fi

# Step 4: Validate deployment
echo "Step 4: Validating deployment..."
./scripts/validate.sh $ENVIRONMENT
if [ $? -ne 0 ]; then
  echo "Validation failed"
  echo "Initiating rollback..."
  ./scripts/rollback.sh $ENVIRONMENT
  exit 1
fi

# Step 5: Run post-deployment tests
echo "Step 5: Running post-deployment tests..."
./scripts/post_deploy_test.sh $ENVIRONMENT
if [ $? -ne 0 ]; then
  echo "Post-deployment tests failed"
  echo "Initiating rollback..."
  ./scripts/rollback.sh $ENVIRONMENT
  exit 1
fi

# Step 6: Update deployment log
echo "Step 6: Updating deployment log..."
cat >> /var/log/datastage/deployment.log <<EOF
$(date +"%Y-%m-%d %H:%M:%S") - Deployment successful
Environment: $ENVIRONMENT
Version: $VERSION
User: $(whoami)
---
EOF

echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: DataStage Deployment

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd tests
          python test_all_jobs.py
      
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: tests/test_results_*.json

  deploy-dev:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Development
        env:
          DS_SERVER: ${{ secrets.DEV_DS_SERVER }}
          DS_USER: ${{ secrets.DEV_DS_USER }}
          DS_PASSWORD: ${{ secrets.DEV_DS_PASSWORD }}
        run: |
          ./scripts/automated_deploy.sh development ${{ github.sha }}

  deploy-prod:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Production
        env:
          DS_SERVER: ${{ secrets.PROD_DS_SERVER }}
          DS_USER: ${{ secrets.PROD_DS_USER }}
          DS_PASSWORD: ${{ secrets.PROD_DS_PASSWORD }}
        run: |
          ./scripts/automated_deploy.sh production ${{ github.sha }}
      
      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'DataStage deployment to production completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'test', 'uat', 'prod'], description: 'Target environment')
        string(name: 'VERSION', defaultValue: '', description: 'Version to deploy')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    cd tests
                    python test_all_jobs.py
                '''
            }
        }
        
        stage('Backup') {
            steps {
                sh '''
                    ./scripts/backup.sh ${ENVIRONMENT}
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    ./scripts/automated_deploy.sh ${ENVIRONMENT} ${VERSION}
                '''
            }
        }
        
        stage('Validate') {
            steps {
                sh '''
                    ./scripts/validate.sh ${ENVIRONMENT}
                '''
            }
        }
    }
    
    post {
        success {
            emailext (
                subject: "DataStage Deployment Successful: ${ENVIRONMENT}",
                body: "Deployment to ${ENVIRONMENT} completed successfully.\nVersion: ${VERSION}",
                to: "etl-team@example.com"
            )
        }
        failure {
            emailext (
                subject: "DataStage Deployment Failed: ${ENVIRONMENT}",
                body: "Deployment to ${ENVIRONMENT} failed.\nCheck Jenkins logs for details.",
                to: "etl-team@example.com"
            )
        }
    }
}
```

## Rollback Procedures

### Automatic Rollback

```bash
#!/bin/bash
# rollback.sh

set -e

ENVIRONMENT=$1
BACKUP_DIR=$2

if [ -z "$ENVIRONMENT" ]; then
  echo "Usage: $0 <environment> [backup_directory]"
  exit 1
fi

# If no backup directory specified, use latest
if [ -z "$BACKUP_DIR" ]; then
  BACKUP_DIR=$(ls -td /backup/datastage/* | head -1)
fi

echo "========================================="
echo "DataStage Rollback"
echo "========================================="
echo "Environment: $ENVIRONMENT"
echo "Backup: $BACKUP_DIR"
echo "Date: $(date)"
echo "========================================="

# Load environment configuration
source config/environments/${ENVIRONMENT}.env

# Restore jobs from backup
for job_file in $BACKUP_DIR/*.dsx; do
  job_name=$(basename $job_file .dsx)
  echo "Restoring $job_name..."
  
  dsjob -import -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job_file
  
  if [ $? -eq 0 ]; then
    echo "✓ $job_name restored successfully"
  else
    echo "✗ Failed to restore $job_name"
    exit 1
  fi
done

# Compile restored jobs
for job_file in $BACKUP_DIR/*.dsx; do
  job_name=$(basename $job_file .dsx)
  echo "Compiling $job_name..."
  
  dsjob -compile -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job_name
  
  if [ $? -eq 0 ]; then
    echo "✓ $job_name compiled successfully"
  else
    echo "✗ Failed to compile $job_name"
    exit 1
  fi
done

# Validate rollback
echo "Validating rollback..."
./scripts/validate.sh $ENVIRONMENT

if [ $? -eq 0 ]; then
  echo "========================================="
  echo "Rollback completed successfully!"
  echo "========================================="
else
  echo "Rollback validation failed!"
  exit 1
fi

# Log rollback
cat >> /var/log/datastage/deployment.log <<EOF
$(date +"%Y-%m-%d %H:%M:%S") - Rollback performed
Environment: $ENVIRONMENT
Backup: $BACKUP_DIR
User: $(whoami)
---
EOF
```

## Post-Deployment Validation

### Validation Checklist

```bash
#!/bin/bash
# post_deploy_validation.sh

echo "Post-Deployment Validation"
echo "=========================="

# 1. Job existence check
echo "1. Checking job existence..."
for job in CUSTOMER_DATA_ETL SALES_DATA_AGGREGATION DATA_QUALITY_VALIDATION \
           INCREMENTAL_LOAD MASTER_DATA_MANAGEMENT; do
  dsjob -jobinfo -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "  ✓ $job exists"
  else
    echo "  ✗ $job not found"
    exit 1
  fi
done

# 2. Job compilation check
echo "2. Checking job compilation..."
for job in CUSTOMER_DATA_ETL SALES_DATA_AGGREGATION DATA_QUALITY_VALIDATION \
           INCREMENTAL_LOAD MASTER_DATA_MANAGEMENT; do
  status=$(dsjob -jobinfo -server $DS_SERVER -user $DS_USER \
    -project $DS_PROJECT $job | grep "Job Status")
  if [[ $status == *"Compiled"* ]]; then
    echo "  ✓ $job compiled"
  else
    echo "  ✗ $job not compiled"
    exit 1
  fi
done

# 3. Database connectivity check
echo "3. Checking database connectivity..."
psql -h $DB_SOURCE_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "  ✓ Source database accessible"
else
  echo "  ✗ Source database not accessible"
  exit 1
fi

# 4. Run smoke tests
echo "4. Running smoke tests..."
cd tests
python smoke_tests.py
if [ $? -eq 0 ]; then
  echo "  ✓ Smoke tests passed"
else
  echo "  ✗ Smoke tests failed"
  exit 1
fi

# 5. Test job execution
echo "5. Testing job execution..."
dsjob -run -wait -param BATCH_DATE=$(date +%Y-%m-%d) \
  -server $DS_SERVER -user $DS_USER \
  $DS_PROJECT CUSTOMER_DATA_ETL
if [ $? -eq 0 ]; then
  echo "  ✓ Test job execution successful"
else
  echo "  ✗ Test job execution failed"
  exit 1
fi

echo "=========================="
echo "All validation checks passed!"
```

## Production Considerations

### 1. Deployment Windows

Schedule deployments during low-traffic periods:

```
Recommended Windows:
- Weekends: Saturday 2:00 AM - 6:00 AM
- Weekdays: Tuesday/Wednesday 2:00 AM - 4:00 AM

Avoid:
- Monday mornings
- Friday afternoons
- End of month/quarter
- Holiday periods
```

### 2. Communication Plan

```markdown
**Pre-Deployment (T-24 hours)**:
- Send notification to stakeholders
- Confirm deployment window
- Verify backup procedures

**During Deployment (T-0)**:
- Update status page
- Monitor deployment progress
- Be ready for rollback

**Post-Deployment (T+1 hour)**:
- Confirm successful deployment
- Run validation tests
- Send completion notification
- Monitor for issues
```

### 3. Monitoring

```bash
# Monitor job execution
watch -n 5 'dsjob -jobinfo -server $DS_SERVER -user $DS_USER \
  -project $DS_PROJECT CUSTOMER_DATA_ETL | grep "Job Status"'

# Monitor system resources
watch -n 5 'top -b -n 1 | head -20'

# Monitor logs
tail -f $DSHOME/Logs/CUSTOMER_DATA_ETL.log
```

### 4. Emergency Contacts

```
Primary Contact: ETL Team Lead
  Email: etl-lead@example.com
  Phone: +1-555-0100

Secondary Contact: DataStage Admin
  Email: ds-admin@example.com
  Phone: +1-555-0101

Escalation: IT Director
  Email: it-director@example.com
  Phone: +1-555-0102
```

## Troubleshooting Deployment

### Common Issues

#### 1. Import Fails

```bash
# Check file permissions
ls -la jobs/*.dsx

# Verify file format
file jobs/CUSTOMER_DATA_ETL.dsx

# Check project exists
dsjob -lprojects -server $DS_SERVER -user $DS_USER
```

#### 2. Compilation Fails

```bash
# Check compilation log
cat $DSHOME/Projects/$DS_PROJECT/RT_LOG*/CUSTOMER_DATA_ETL.log

# Recompile with force
dsjob -compile -force -server $DS_SERVER -user $DS_USER \
  -project $DS_PROJECT CUSTOMER_DATA_ETL
```

#### 3. Connection Issues

```bash
# Test database connection
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# Check DataStage connection
dsjob -testconnection -server $DS_SERVER -user $DS_USER \
  -project $DS_PROJECT CONNECTION_NAME
```

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Architecture Overview](ARCHITECTURE.md)