# Configuration Guide

Comprehensive guide for configuring DataStage pipeline jobs and the test framework.

## Table of Contents

- [Overview](#overview)
- [Connection Configuration](#connection-configuration)
- [Job Parameters](#job-parameters)
- [Test Configuration](#test-configuration)
- [Environment Variables](#environment-variables)
- [Security Configuration](#security-configuration)
- [Performance Tuning](#performance-tuning)
- [Logging Configuration](#logging-configuration)

## Overview

This guide covers all configuration aspects for the DataStage pipeline examples, including:

- Database connections
- Job parameters
- Test framework settings
- Environment-specific configurations
- Security and credentials management

### Configuration Files

```
config/
├── connections.json        # Database connection definitions
├── parameters.json         # Default job parameters
├── test_config.json       # Test framework configuration
├── logging.conf           # Logging configuration
└── environments/          # Environment-specific configs
    ├── dev.json
    ├── test.json
    └── prod.json
```

## Connection Configuration

### connections.json

Define all database connections in [`config/connections.json`](../config/connections.json):

```json
{
  "CUSTOMER_SOURCE_DB": {
    "type": "ODBC",
    "driver": "PostgreSQL",
    "server": "source-db-server.example.com",
    "database": "customers",
    "username": "etl_user",
    "password": "${DB_PASSWORD}",
    "port": 5432,
    "options": {
      "sslmode": "require",
      "connect_timeout": 30
    }
  },
  "CUSTOMER_DW": {
    "type": "ODBC",
    "driver": "PostgreSQL",
    "server": "dw-server.example.com",
    "database": "warehouse",
    "username": "dw_user",
    "password": "${DW_PASSWORD}",
    "port": 5432,
    "schema": "customer_data",
    "options": {
      "sslmode": "require",
      "application_name": "DataStage_ETL"
    }
  },
  "SALES_TRANSACTIONAL_DB": {
    "type": "ODBC",
    "driver": "Oracle",
    "server": "sales-db.example.com",
    "database": "SALES",
    "username": "sales_reader",
    "password": "${SALES_DB_PASSWORD}",
    "port": 1521,
    "service_name": "SALESPROD"
  },
  "SALES_DW": {
    "type": "ODBC",
    "driver": "Snowflake",
    "server": "account.snowflakecomputing.com",
    "database": "SALES_WAREHOUSE",
    "username": "etl_service",
    "password": "${SNOWFLAKE_PASSWORD}",
    "warehouse": "ETL_WH",
    "schema": "SALES_MART",
    "role": "ETL_ROLE"
  },
  "ETL_CONTROL_DB": {
    "type": "ODBC",
    "driver": "PostgreSQL",
    "server": "control-db.example.com",
    "database": "etl_control",
    "username": "etl_admin",
    "password": "${CONTROL_DB_PASSWORD}",
    "port": 5432,
    "schema": "control"
  }
}
```

### Connection Properties

#### Common Properties

| Property | Required | Description | Example |
|----------|----------|-------------|---------|
| `type` | Yes | Connection type | ODBC, JDBC, File |
| `driver` | Yes | Database driver | PostgreSQL, Oracle, MySQL |
| `server` | Yes | Server hostname/IP | db.example.com |
| `database` | Yes | Database name | customers |
| `username` | Yes | Database username | etl_user |
| `password` | Yes | Database password | Use ${VAR} for env vars |
| `port` | No | Port number | 5432, 1521, 3306 |

#### Database-Specific Properties

**PostgreSQL**:
```json
{
  "options": {
    "sslmode": "require",
    "connect_timeout": 30,
    "application_name": "DataStage_ETL",
    "statement_timeout": 300000
  }
}
```

**Oracle**:
```json
{
  "service_name": "PRODDB",
  "options": {
    "arraysize": 1000,
    "prefetch_rows": 1000
  }
}
```

**SQL Server**:
```json
{
  "options": {
    "TrustServerCertificate": "yes",
    "Encrypt": "yes",
    "ApplicationIntent": "ReadOnly"
  }
}
```

**Snowflake**:
```json
{
  "warehouse": "ETL_WH",
  "schema": "PUBLIC",
  "role": "ETL_ROLE",
  "options": {
    "authenticator": "snowflake",
    "ocsp_response_cache_filename": "/tmp/ocsp_cache"
  }
}
```

### Creating Connections in DataStage

#### Using DataStage Designer

1. Open **DataStage Designer**
2. Go to **Tools** → **Import** → **Table Definitions**
3. Select **ODBC** as connection type
4. Configure connection properties
5. Test connection
6. Save connection

#### Using Command Line

```bash
# Create ODBC connection
dsjob -server your-server -user your-username \
  -domain your-domain \
  -createconnection CUSTOMER_SOURCE_DB \
  -type ODBC \
  -server source-db-server.example.com \
  -database customers \
  -username etl_user \
  -password ${DB_PASSWORD}
```

### Connection Pooling

Configure connection pooling for better performance:

```json
{
  "connection_pool": {
    "enabled": true,
    "min_connections": 2,
    "max_connections": 10,
    "connection_timeout": 30,
    "idle_timeout": 300,
    "max_lifetime": 1800
  }
}
```

## Job Parameters

### parameters.json

Define default job parameters in [`config/parameters.json`](../config/parameters.json):

```json
{
  "CUSTOMER_DATA_ETL": {
    "SOURCE_DB_CONN": "CUSTOMER_SOURCE_DB",
    "TARGET_DB_CONN": "CUSTOMER_DW",
    "BATCH_DATE": "CurrentDate()",
    "COMMIT_INTERVAL": 1000,
    "PARALLEL_NODES": 4,
    "REJECT_THRESHOLD": 5,
    "EMAIL_ON_FAILURE": "etl-team@example.com"
  },
  "SALES_DATA_AGGREGATION": {
    "SOURCE_DB_CONN": "SALES_TRANSACTIONAL_DB",
    "TARGET_DB_CONN": "SALES_DW",
    "START_DATE": "CurrentDate() - 1",
    "END_DATE": "CurrentDate()",
    "AGGREGATION_LEVEL": "DAILY",
    "PARTITION_COUNT": 8,
    "BUFFER_SIZE": 10000
  },
  "DATA_QUALITY_VALIDATION": {
    "SOURCE_DB_CONN": "STAGING_DB",
    "DQ_RULES_DB_CONN": "DQ_METADATA_DB",
    "TABLE_NAME": "",
    "VALIDATION_DATE": "CurrentDate()",
    "QUALITY_THRESHOLD": 95,
    "FAIL_ON_THRESHOLD": 0,
    "GENERATE_REPORT": 1
  },
  "INCREMENTAL_LOAD": {
    "SOURCE_DB_CONN": "OPERATIONAL_DB",
    "TARGET_DB_CONN": "DATA_WAREHOUSE",
    "CONTROL_DB_CONN": "ETL_CONTROL_DB",
    "TABLE_NAME": "",
    "LAST_LOAD_TIMESTAMP": "",
    "CURRENT_LOAD_TIMESTAMP": "CurrentTimestamp()",
    "SCD_TYPE": 2,
    "HASH_ALGORITHM": "MD5"
  },
  "MASTER_DATA_MANAGEMENT": {
    "SOURCE1_DB_CONN": "CRM_DB",
    "SOURCE2_DB_CONN": "ERP_DB",
    "SOURCE3_DB_CONN": "ECOMMERCE_DB",
    "MDM_DB_CONN": "MDM_MASTER_DB",
    "MATCH_THRESHOLD": 85,
    "AUTO_MERGE": 1,
    "PROCESSING_DATE": "CurrentDate()",
    "SURVIVORSHIP_RULES": "MOST_RECENT"
  }
}
```

### Parameter Types

| Type | Description | Example |
|------|-------------|---------|
| String | Text value | "CUSTOMER_SOURCE_DB" |
| Integer | Numeric value | 1000 |
| Date | Date value | "2026-04-16" |
| Timestamp | Date and time | "2026-04-16 12:00:00" |
| Boolean | True/False (1/0) | 1 |
| Expression | DataStage expression | "CurrentDate()" |

### Parameter Validation

Add validation rules for parameters:

```json
{
  "parameter_validation": {
    "COMMIT_INTERVAL": {
      "type": "integer",
      "min": 100,
      "max": 10000,
      "default": 1000
    },
    "QUALITY_THRESHOLD": {
      "type": "integer",
      "min": 0,
      "max": 100,
      "default": 95
    },
    "AGGREGATION_LEVEL": {
      "type": "string",
      "allowed_values": ["DAILY", "WEEKLY", "MONTHLY"],
      "default": "DAILY"
    }
  }
}
```

### Environment-Specific Parameters

Override parameters per environment:

**dev.json**:
```json
{
  "CUSTOMER_DATA_ETL": {
    "SOURCE_DB_CONN": "CUSTOMER_SOURCE_DB_DEV",
    "TARGET_DB_CONN": "CUSTOMER_DW_DEV",
    "COMMIT_INTERVAL": 100,
    "EMAIL_ON_FAILURE": "dev-team@example.com"
  }
}
```

**prod.json**:
```json
{
  "CUSTOMER_DATA_ETL": {
    "SOURCE_DB_CONN": "CUSTOMER_SOURCE_DB_PROD",
    "TARGET_DB_CONN": "CUSTOMER_DW_PROD",
    "COMMIT_INTERVAL": 5000,
    "EMAIL_ON_FAILURE": "prod-alerts@example.com",
    "PARALLEL_NODES": 16
  }
}
```

## Test Configuration

### test_config.json

Configure the test framework in [`config/test_config.json`](../config/test_config.json):

```json
{
  "datastage": {
    "project": "TEST_PROJECT",
    "server": "test-datastage-server",
    "username": "test_user",
    "domain": "test_domain",
    "timeout": 300
  },
  "database_connections": {
    "source": {
      "type": "postgresql",
      "host": "test-source-db",
      "port": 5432,
      "database": "test_customers",
      "username": "test_user",
      "password": "${TEST_DB_PASSWORD}"
    },
    "target": {
      "type": "postgresql",
      "host": "test-target-db",
      "port": 5432,
      "database": "test_warehouse",
      "username": "test_user",
      "password": "${TEST_DB_PASSWORD}"
    }
  },
  "test_data": {
    "sample_size": 1000,
    "data_directory": "../data",
    "cleanup_after_test": true
  },
  "reporting": {
    "output_directory": "./test_results",
    "generate_html": true,
    "generate_json": true,
    "email_results": false,
    "email_recipients": ["test-team@example.com"]
  },
  "performance": {
    "max_execution_time": 300,
    "min_throughput": 100,
    "memory_limit_mb": 2048
  },
  "quality_thresholds": {
    "min_quality_score": 95,
    "max_reject_percentage": 5,
    "max_null_percentage": 1
  }
}
```

### Test Data Configuration

Configure test data generation:

```json
{
  "test_data_generation": {
    "customers": {
      "row_count": 1000,
      "columns": {
        "customer_id": {"type": "sequence", "start": 1},
        "first_name": {"type": "random", "source": "first_names.txt"},
        "last_name": {"type": "random", "source": "last_names.txt"},
        "email": {"type": "pattern", "pattern": "{first}.{last}@example.com"},
        "phone": {"type": "pattern", "pattern": "+1-###-###-####"},
        "date_of_birth": {"type": "date_range", "start": "1950-01-01", "end": "2005-12-31"}
      }
    }
  }
}
```

## Environment Variables

### Required Environment Variables

Set these environment variables before running jobs:

```bash
# DataStage Environment
export DSHOME=/opt/IBM/InformationServer/Server/DSEngine
export DS_PROJECT=YOUR_PROJECT
export DS_SERVER=your-datastage-server
export DS_USER=your-username
export DS_DOMAIN=your-domain

# Database Passwords (use secure methods in production)
export DB_PASSWORD='your-source-db-password'
export DW_PASSWORD='your-warehouse-password'
export CONTROL_DB_PASSWORD='your-control-db-password'

# Application Settings
export ETL_ENV=production
export LOG_LEVEL=INFO
export EMAIL_SMTP_SERVER=smtp.example.com
export EMAIL_FROM=etl-system@example.com
```

### Environment-Specific Variables

**Development**:
```bash
export ETL_ENV=development
export LOG_LEVEL=DEBUG
export COMMIT_INTERVAL=100
export PARALLEL_NODES=2
```

**Testing**:
```bash
export ETL_ENV=test
export LOG_LEVEL=INFO
export COMMIT_INTERVAL=500
export PARALLEL_NODES=4
```

**Production**:
```bash
export ETL_ENV=production
export LOG_LEVEL=WARN
export COMMIT_INTERVAL=5000
export PARALLEL_NODES=16
```

### Loading Environment Variables

Create environment-specific files:

**.env.dev**:
```bash
ETL_ENV=development
DS_PROJECT=DEV_PROJECT
DS_SERVER=dev-datastage-server
LOG_LEVEL=DEBUG
```

**.env.prod**:
```bash
ETL_ENV=production
DS_PROJECT=PROD_PROJECT
DS_SERVER=prod-datastage-server
LOG_LEVEL=WARN
```

Load with:
```bash
source .env.dev  # or .env.prod
```

## Security Configuration

### Credential Management

#### Using Environment Variables

```json
{
  "password": "${DB_PASSWORD}"
}
```

#### Using Encrypted Files

```bash
# Encrypt password file
openssl enc -aes-256-cbc -salt -in passwords.txt -out passwords.enc

# Decrypt at runtime
openssl enc -aes-256-cbc -d -in passwords.enc -out passwords.txt
```

#### Using HashiCorp Vault

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.approle.login(role_id='...', secret_id='...')

secret = client.secrets.kv.v2.read_secret_version(path='datastage/db_passwords')
db_password = secret['data']['data']['customer_db']
```

#### Using AWS Secrets Manager

```python
import boto3

client = boto3.client('secretsmanager', region_name='us-east-1')
response = client.get_secret_value(SecretId='datastage/db_passwords')
secrets = json.loads(response['SecretString'])
db_password = secrets['customer_db']
```

### Access Control

Configure role-based access:

```json
{
  "access_control": {
    "roles": {
      "etl_developer": {
        "permissions": ["read", "write", "execute"],
        "projects": ["DEV_PROJECT", "TEST_PROJECT"]
      },
      "etl_operator": {
        "permissions": ["execute", "monitor"],
        "projects": ["PROD_PROJECT"]
      },
      "etl_admin": {
        "permissions": ["read", "write", "execute", "admin"],
        "projects": ["*"]
      }
    }
  }
}
```

### Audit Logging

Enable audit logging:

```json
{
  "audit": {
    "enabled": true,
    "log_file": "/var/log/datastage/audit.log",
    "log_level": "INFO",
    "events": [
      "job_start",
      "job_end",
      "job_failure",
      "parameter_change",
      "connection_change"
    ]
  }
}
```

## Performance Tuning

### Job-Level Configuration

```json
{
  "performance": {
    "parallel_processing": {
      "enabled": true,
      "partition_count": 8,
      "partition_method": "HASH",
      "partition_key": "CUSTOMER_ID"
    },
    "buffer_settings": {
      "buffer_size": 10000,
      "buffer_free_run": 50,
      "max_memory_mb": 2048
    },
    "commit_settings": {
      "commit_interval": 5000,
      "commit_on_eof": true
    },
    "optimization": {
      "enable_row_buffer": true,
      "enable_parallel_read": true,
      "enable_parallel_write": true,
      "use_bulk_load": true
    }
  }
}
```

### Database-Specific Tuning

**PostgreSQL**:
```json
{
  "tuning": {
    "fetch_size": 1000,
    "batch_size": 1000,
    "use_copy": true,
    "work_mem": "256MB"
  }
}
```

**Oracle**:
```json
{
  "tuning": {
    "arraysize": 1000,
    "prefetch_rows": 1000,
    "use_direct_path": true,
    "parallel_degree": 4
  }
}
```

### Resource Limits

```json
{
  "resource_limits": {
    "max_memory_mb": 4096,
    "max_cpu_percent": 80,
    "max_disk_io_mbps": 500,
    "max_network_mbps": 1000
  }
}
```

## Logging Configuration

### logging.conf

Configure logging in [`config/logging.conf`](../config/logging.conf):

```ini
[loggers]
keys=root,datastage,test

[handlers]
keys=consoleHandler,fileHandler,errorHandler

[formatters]
keys=detailed,simple

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_datastage]
level=INFO
handlers=fileHandler
qualname=datastage
propagate=0

[logger_test]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=test
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simple
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=INFO
formatter=detailed
args=('/var/log/datastage/etl.log', 'a', 10485760, 5)

[handler_errorHandler]
class=handlers.RotatingFileHandler
level=ERROR
formatter=detailed
args=('/var/log/datastage/error.log', 'a', 10485760, 5)

[formatter_detailed]
format=%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_simple]
format=%(levelname)s - %(message)s
```

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| DEBUG | Detailed information | Development, troubleshooting |
| INFO | General information | Normal operations |
| WARNING | Warning messages | Potential issues |
| ERROR | Error messages | Failures, exceptions |
| CRITICAL | Critical errors | System failures |

### Log Rotation

Configure log rotation:

```json
{
  "log_rotation": {
    "max_size_mb": 100,
    "max_files": 10,
    "compress_old_logs": true,
    "retention_days": 30
  }
}
```

## Configuration Best Practices

### 1. Separation of Concerns

- Keep connections separate from parameters
- Use environment-specific configuration files
- Never commit passwords to version control

### 2. Use Environment Variables

- Store sensitive data in environment variables
- Use `.env` files for local development
- Use secrets management in production

### 3. Configuration Validation

- Validate configuration on startup
- Provide clear error messages
- Use schema validation

### 4. Documentation

- Document all configuration options
- Provide examples for each setting
- Keep documentation up to date

### 5. Version Control

- Version control all configuration files
- Use `.gitignore` for sensitive files
- Track configuration changes

### 6. Testing

- Test with different configurations
- Validate configuration in CI/CD
- Use configuration templates

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)