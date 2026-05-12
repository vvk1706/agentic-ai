# Architecture Overview

Comprehensive overview of the DataStage pipeline architecture, design patterns, and system components.

## Table of Contents

- [System Architecture](#system-architecture)
- [Component Overview](#component-overview)
- [Data Flow Architecture](#data-flow-architecture)
- [Design Patterns](#design-patterns)
- [Integration Architecture](#integration-architecture)
- [Scalability and High Availability](#scalability-and-high-availability)
- [Security Architecture](#security-architecture)
- [Monitoring and Observability](#monitoring-and-observability)

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   CRM    │  │   ERP    │  │E-Commerce│  │  Legacy  │       │
│  │ Database │  │ Database │  │ Database │  │  Systems │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
        ┌─────────────▼──────────────────────────────────────────┐
        │           DataStage ETL Layer                          │
        │  ┌──────────────────────────────────────────────────┐ │
        │  │         Job Orchestration                        │ │
        │  │  ┌────────┐  ┌────────┐  ┌────────┐            │ │
        │  │  │Extract │→ │Transform│→ │  Load  │            │ │
        │  │  └────────┘  └────────┘  └────────┘            │ │
        │  └──────────────────────────────────────────────────┘ │
        │  ┌──────────────────────────────────────────────────┐ │
        │  │         Data Quality & Validation                │ │
        │  └──────────────────────────────────────────────────┘ │
        │  ┌──────────────────────────────────────────────────┐ │
        │  │         Error Handling & Logging                 │ │
        │  └──────────────────────────────────────────────────┘ │
        └────────────────────┬───────────────────────────────────┘
                             │
        ┌────────────────────▼───────────────────────────────────┐
        │              Target Systems                            │
        │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
        │  │   Data   │  │Analytics │  │   MDM    │            │
        │  │Warehouse │  │ Platform │  │  System  │            │
        │  └──────────┘  └──────────┘  └──────────┘            │
        └────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **ETL Engine** | IBM DataStage 11.7+ | Core ETL processing |
| **Orchestration** | DataStage Sequences | Job scheduling and workflow |
| **Testing** | Python 3.8+ | Automated testing framework |
| **Source Databases** | PostgreSQL, Oracle, SQL Server | Operational data sources |
| **Target Databases** | PostgreSQL, Snowflake, Redshift | Data warehouse targets |
| **Control Database** | PostgreSQL | ETL metadata and control |
| **Version Control** | Git | Code versioning |
| **CI/CD** | GitHub Actions, Jenkins | Automated deployment |
| **Monitoring** | Prometheus, Grafana | Performance monitoring |
| **Logging** | ELK Stack | Centralized logging |

## Component Overview

### 1. DataStage Jobs

Core ETL processing components:

```
jobs/
├── customer_data_etl.dsx           # Customer data pipeline
├── sales_data_aggregation.dsx      # Sales aggregation
├── data_quality_validation.dsx     # Data quality checks
├── incremental_load.dsx            # CDC processing
└── master_data_management.dsx      # MDM consolidation
```

**Characteristics**:
- Modular design
- Parameterized for flexibility
- Comprehensive error handling
- Performance optimized

### 2. Test Framework

Python-based testing infrastructure:

```
tests/
├── test_framework.py               # Core framework
├── test_customer_etl.py           # Job-specific tests
└── test_all_jobs.py               # Integration tests
```

**Features**:
- Automated job execution
- Data validation
- Performance testing
- Report generation

### 3. Configuration Management

Centralized configuration:

```
config/
├── connections.json                # Database connections
├── parameters.json                 # Job parameters
├── test_config.json               # Test settings
└── environments/                   # Environment configs
    ├── dev.json
    ├── test.json
    └── prod.json
```

### 4. Control Database

Metadata and control tables:

```sql
-- Job execution tracking
CREATE TABLE etl_job_log (
    log_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100),
    run_id VARCHAR(50),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    rows_processed INTEGER,
    rows_rejected INTEGER,
    execution_time DECIMAL(10,2)
);

-- Error logging
CREATE TABLE etl_error_log (
    error_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100),
    run_id VARCHAR(50),
    error_timestamp TIMESTAMP,
    error_type VARCHAR(50),
    error_message TEXT,
    source_row TEXT
);

-- Data quality metrics
CREATE TABLE etl_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100),
    run_id VARCHAR(50),
    metric_name VARCHAR(100),
    metric_value DECIMAL(10,2),
    threshold DECIMAL(10,2),
    status VARCHAR(20),
    measured_at TIMESTAMP
);

-- Incremental load control
CREATE TABLE etl_load_control (
    control_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    last_load_timestamp TIMESTAMP,
    last_load_key VARCHAR(100),
    rows_loaded INTEGER,
    load_status VARCHAR(20)
);
```

## Data Flow Architecture

### Extract-Transform-Load (ETL) Pattern

#### 1. Extract Phase

```
Source Systems
    ↓
[Connection Pool]
    ↓
[Data Extraction]
    ├─ Full Extract
    ├─ Incremental Extract (CDC)
    └─ Filtered Extract
    ↓
[Staging Area]
```

**Key Features**:
- Connection pooling for efficiency
- Parallel extraction for performance
- Change Data Capture (CDC) support
- Error handling and retry logic

#### 2. Transform Phase

```
[Staging Data]
    ↓
[Data Cleansing]
    ├─ Null handling
    ├─ Format standardization
    ├─ Duplicate removal
    └─ Outlier detection
    ↓
[Business Rules]
    ├─ Calculations
    ├─ Derivations
    ├─ Aggregations
    └─ Enrichment
    ↓
[Data Quality Checks]
    ├─ Completeness
    ├─ Validity
    ├─ Consistency
    └─ Accuracy
    ↓
[Transformed Data]
```

**Key Features**:
- Modular transformation logic
- Reusable shared containers
- Comprehensive validation
- Reject handling

#### 3. Load Phase

```
[Transformed Data]
    ↓
[Pre-Load Validation]
    ↓
[Load Strategy]
    ├─ Full Load
    ├─ Incremental Load
    ├─ Upsert (Merge)
    └─ SCD Type 2
    ↓
[Target Systems]
    ↓
[Post-Load Validation]
```

**Key Features**:
- Multiple load strategies
- Bulk loading for performance
- Transaction management
- Referential integrity checks

### Data Flow Example: Customer ETL

```
┌─────────────────────────────────────────────────────────────┐
│ 1. EXTRACT                                                  │
│    Source: CUSTOMERS table                                  │
│    Filter: LAST_UPDATED >= CURRENT_DATE - 1                │
│    Columns: 14 columns                                      │
│    Expected: ~1000 rows/day                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ 2. TRANSFORM                                                │
│    ┌──────────────────────────────────────────────────┐    │
│    │ Data Cleansing                                   │    │
│    │ - Trim whitespace                                │    │
│    │ - Standardize email (uppercase)                  │    │
│    │ - Clean phone (digits only)                      │    │
│    └──────────────────┬───────────────────────────────┘    │
│    ┌──────────────────▼───────────────────────────────┐    │
│    │ Business Logic                                   │    │
│    │ - Concatenate full name                          │    │
│    │ - Calculate age from DOB                         │    │
│    │ - Determine customer segment                     │    │
│    │ - Convert status to flag                         │    │
│    └──────────────────┬───────────────────────────────┘    │
│    ┌──────────────────▼───────────────────────────────┐    │
│    │ Validation                                       │    │
│    │ - Customer ID not null                           │    │
│    │ - Email not null and valid format                │    │
│    │ - Age between 18 and 120                         │    │
│    └──────────────────┬───────────────────────────────┘    │
│                       │                                     │
│         ┌─────────────┴─────────────┐                      │
│         │                           │                      │
│    ┌────▼─────┐              ┌─────▼──────┐              │
│    │  Valid   │              │  Rejected  │              │
│    │ Records  │              │  Records   │              │
│    │ (~995)   │              │   (~5)     │              │
│    └────┬─────┘              └─────┬──────┘              │
└─────────┼──────────────────────────┼──────────────────────┘
          │                          │
┌─────────▼──────────────┐  ┌────────▼──────────────────────┐
│ 3. LOAD                │  │ REJECT HANDLING               │
│    Target: DW_CUSTOMERS│  │    File: customer_rejects.csv │
│    Mode: Upsert        │  │    Include: All columns +     │
│    Key: CUSTOMER_ID    │  │             REJECT_REASON     │
│    Commit: 1000 rows   │  │    Action: Log and notify     │
└────────────────────────┘  └───────────────────────────────┘
```

## Design Patterns

### 1. Slowly Changing Dimension (SCD) Type 2

Track historical changes with versioning:

```sql
CREATE TABLE dim_customer (
    surrogate_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    -- other attributes --
    effective_date TIMESTAMP NOT NULL,
    expiry_date TIMESTAMP,
    is_current INTEGER DEFAULT 1,
    record_hash VARCHAR(64),
    etl_insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example: Customer email changes
-- Old record:
-- surrogate_key=1, customer_id=100, email='old@example.com', 
-- effective_date='2026-01-01', expiry_date='2026-04-15', is_current=0

-- New record:
-- surrogate_key=2, customer_id=100, email='new@example.com',
-- effective_date='2026-04-16', expiry_date=NULL, is_current=1
```

**Implementation**:
```datastage
1. Calculate hash of current record
2. Lookup existing record by business key
3. Compare hashes
4. If different:
   - Expire old record (set expiry_date, is_current=0)
   - Insert new record (new surrogate_key, is_current=1)
5. If same:
   - No action (record unchanged)
```

### 2. Change Data Capture (CDC)

Capture only changed data:

```datastage
Source Query:
  SELECT *
  FROM source_table
  WHERE last_updated >= :LAST_LOAD_TIMESTAMP
    AND last_updated < :CURRENT_LOAD_TIMESTAMP

CDC Logic:
  - INSERT: Records not in target
  - UPDATE: Records with different hash
  - DELETE: Records in target but not in source (optional)
```

### 3. Staging Layer Pattern

Use staging for data validation:

```
Source → Staging → Validation → Target

Staging Benefits:
- Isolate source from target
- Enable data quality checks
- Support rollback
- Facilitate debugging
```

### 4. Audit Trail Pattern

Track all data changes:

```sql
-- Add audit columns to all tables
ALTER TABLE target_table ADD COLUMN etl_insert_date TIMESTAMP;
ALTER TABLE target_table ADD COLUMN etl_update_date TIMESTAMP;
ALTER TABLE target_table ADD COLUMN etl_batch_id VARCHAR(50);
ALTER TABLE target_table ADD COLUMN etl_source_system VARCHAR(50);

-- Populate in DataStage
ETL_INSERT_DATE = CurrentTimestamp()
ETL_UPDATE_DATE = CurrentTimestamp()
ETL_BATCH_ID = #BATCH_DATE#
ETL_SOURCE_SYSTEM = "CRM"
```

### 5. Error Handling Pattern

Comprehensive error management:

```
┌─────────────┐
│   Process   │
└──────┬──────┘
       │
   ┌───▼────┐
   │Success?│
   └───┬────┘
       │
   ┌───▼────────────────┐
   │ Yes          No    │
   │  │            │    │
   │  ▼            ▼    │
   │Target    Reject    │
   │          File      │
   │            │       │
   │            ▼       │
   │        Error Log   │
   │            │       │
   │            ▼       │
   │      Notification  │
   └────────────────────┘
```

## Integration Architecture

### Source System Integration

```
┌──────────────────────────────────────────────────────────┐
│                  Source Systems                          │
├──────────────────────────────────────────────────────────┤
│  Database Systems:                                       │
│  - ODBC/JDBC connections                                 │
│  - Connection pooling                                    │
│  - Read replicas for minimal impact                     │
│                                                          │
│  File Systems:                                           │
│  - CSV, JSON, XML, Parquet                              │
│  - FTP/SFTP for file transfer                           │
│  - File watching for automation                          │
│                                                          │
│  APIs:                                                   │
│  - REST API integration                                  │
│  - SOAP web services                                     │
│  - Message queues (Kafka, RabbitMQ)                     │
└──────────────────────────────────────────────────────────┘
```

### Target System Integration

```
┌──────────────────────────────────────────────────────────┐
│                  Target Systems                          │
├──────────────────────────────────────────────────────────┤
│  Data Warehouses:                                        │
│  - Bulk loading for performance                          │
│  - Partitioning for scalability                          │
│  - Indexing for query performance                        │
│                                                          │
│  Analytics Platforms:                                    │
│  - Snowflake, Redshift, BigQuery                        │
│  - Optimized data formats                                │
│  - Incremental updates                                   │
│                                                          │
│  Operational Systems:                                    │
│  - Real-time or near-real-time updates                  │
│  - Transaction management                                │
│  - Referential integrity                                 │
└──────────────────────────────────────────────────────────┘
```

## Scalability and High Availability

### Horizontal Scaling

```
┌─────────────────────────────────────────────────────────┐
│              DataStage Cluster                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Node 1  │  │  Node 2  │  │  Node 3  │            │
│  │          │  │          │  │          │            │
│  │ Partition│  │ Partition│  │ Partition│            │
│  │   1-3    │  │   4-6    │  │   7-9    │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────┘

Benefits:
- Process large datasets in parallel
- Distribute load across nodes
- Linear scalability
- Fault tolerance
```

### High Availability

```
┌─────────────────────────────────────────────────────────┐
│           Active-Passive Configuration                  │
│                                                         │
│  ┌──────────────┐              ┌──────────────┐       │
│  │   Primary    │              │   Standby    │       │
│  │  DataStage   │─────────────▶│  DataStage   │       │
│  │   Server     │  Replication │   Server     │       │
│  └──────────────┘              └──────────────┘       │
│         │                              │               │
│         │        Failover              │               │
│         └──────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘

Features:
- Automatic failover
- Shared storage for jobs
- Load balancer for distribution
- Health monitoring
```

## Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                              │
│  - Firewall rules                                       │
│  - VPN for remote access                                │
│  - Network segmentation                                 │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Authentication & Authorization                 │
│  - LDAP/Active Directory integration                    │
│  - Role-based access control (RBAC)                     │
│  - Multi-factor authentication (MFA)                    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Data Security                                  │
│  - Encryption at rest                                   │
│  - Encryption in transit (TLS/SSL)                      │
│  - Data masking for sensitive fields                    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Application Security                           │
│  - Secure credential management                         │
│  - Input validation                                     │
│  - SQL injection prevention                             │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Audit & Monitoring                            │
│  - Comprehensive audit logging                          │
│  - Security event monitoring                            │
│  - Compliance reporting                                 │
└─────────────────────────────────────────────────────────┘
```

## Monitoring and Observability

### Monitoring Stack

```
┌─────────────────────────────────────────────────────────┐
│                  Metrics Collection                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Prometheus                                       │  │
│  │ - Job execution metrics                          │  │
│  │ - System resource metrics                        │  │
│  │ - Database performance metrics                   │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Visualization                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Grafana Dashboards                               │  │
│  │ - Real-time job status                           │  │
│  │ - Performance trends                             │  │
│  │ - Resource utilization                           │  │
│  │ - Data quality metrics                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                  Alerting                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Alert Manager                                    │  │
│  │ - Job failures                                   │  │
│  │ - Performance degradation                        │  │
│  │ - Data quality issues                            │  │
│  │ - Resource exhaustion                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Key Metrics

| Metric | Description | Threshold |
|--------|-------------|-----------|
| Job Success Rate | % of successful job executions | > 99% |
| Execution Time | Average job execution time | < baseline + 20% |
| Throughput | Rows processed per second | > 100 rows/sec |
| Error Rate | % of rejected records | < 5% |
| Resource Utilization | CPU, Memory, Disk usage | < 80% |
| Data Quality Score | Overall data quality | > 95% |

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)