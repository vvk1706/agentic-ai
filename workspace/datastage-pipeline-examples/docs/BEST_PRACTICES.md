# DataStage Best Practices

Comprehensive guide to best practices for developing, testing, and maintaining DataStage ETL pipelines.

## Table of Contents

- [Job Design](#job-design)
- [Data Quality](#data-quality)
- [Performance Optimization](#performance-optimization)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Documentation](#documentation)
- [Security](#security)
- [Maintenance](#maintenance)
- [Deployment](#deployment)

## Job Design

### 1. Naming Conventions

#### Job Names

Use clear, descriptive names following a consistent pattern:

```
<Domain>_<Process>_<Type>
```

Examples:
- `CUSTOMER_DATA_ETL`
- `SALES_DATA_AGGREGATION`
- `PRODUCT_INCREMENTAL_LOAD`

#### Stage Names

Use descriptive stage names that indicate purpose:

```
<Action>_<Entity>
```

Examples:
- `SOURCE_CUSTOMERS`
- `TRANSFORM_SALES_DATA`
- `TARGET_CUSTOMER_DW`
- `REJECT_INVALID_RECORDS`

#### Column Names

Follow database naming conventions:
- Use UPPERCASE for database columns
- Use snake_case for derived columns
- Prefix audit columns: `ETL_INSERT_DATE`, `ETL_UPDATE_DATE`

### 2. Modular Design

**DO**: Break complex jobs into smaller, reusable components

```
Extract Job → Transform Job → Load Job
```

**DON'T**: Create monolithic jobs that do everything

#### Shared Containers

Create shared containers for common logic:
- Date formatting
- Address standardization
- Email validation
- Phone number cleaning

```datastage
SharedContainer: FORMAT_DATE
Input: DATE_STRING
Output: FORMATTED_DATE
Logic: DateFromString(DATE_STRING, "%Y-%m-%d")
```

### 3. Parameterization

**DO**: Use parameters for all configurable values

```xml
<Parameter Name="SOURCE_DB_CONN" Type="String" Default="CUSTOMER_SOURCE_DB"/>
<Parameter Name="BATCH_DATE" Type="Date" Default="CurrentDate()"/>
<Parameter Name="COMMIT_INTERVAL" Type="Integer" Default="1000"/>
```

**DON'T**: Hard-code values in jobs

```xml
<!-- BAD -->
<ConnectionString>Server=prod-db;Database=customers</ConnectionString>

<!-- GOOD -->
<ConnectionString>#SOURCE_DB_CONN#</ConnectionString>
```

### 4. Stage Organization

Organize stages logically:

```
1. Source Stages (left)
2. Transformation Stages (middle)
3. Target Stages (right)
4. Reject/Error Stages (bottom)
```

Use annotations to document complex logic:

```
Annotation: "This transformer applies business rule BR-001:
Customer age must be calculated from DOB and segmented
into YOUNG_ADULT, MIDDLE_AGE, SENIOR, ELDERLY"
```

### 5. Link Naming

Name links descriptively:

```
SOURCE_TO_TRANSFORM
TRANSFORM_TO_TARGET
TRANSFORM_TO_REJECT
```

## Data Quality

### 1. Input Validation

Validate all input data:

```datastage
Constraint: VALID_RECORDS
Expression: Not(IsNull(CUSTOMER_ID)) 
           And Not(IsNull(EMAIL)) 
           And Len(Trim(EMAIL)) > 0
           And EMAIL Like '%@%'
```

### 2. Data Cleansing

Implement standard cleansing rules:

```datastage
# Trim whitespace
CLEAN_NAME = Trim(FIRST_NAME)

# Standardize case
EMAIL_CLEAN = Upcase(Trim(EMAIL))

# Remove special characters
PHONE_CLEAN = Convert("[^0-9]", "", PHONE)

# Handle nulls
CITY_CLEAN = If IsNull(CITY) Then "UNKNOWN" Else Trim(City)
```

### 3. Business Rule Validation

Document and implement business rules:

```datastage
# BR-001: Customer age must be between 18 and 120
AGE = YearFromDate(CurrentDate()) - YearFromDate(DATE_OF_BIRTH)
Constraint: VALID_AGE
Expression: AGE >= 18 And AGE <= 120

# BR-002: Email must be unique per customer
# Implement in lookup or database constraint

# BR-003: Phone number must be 10-15 digits
Constraint: VALID_PHONE
Expression: Len(PHONE_CLEAN) >= 10 And Len(PHONE_CLEAN) <= 15
```

### 4. Reject Handling

Always implement reject handling:

```datastage
Transformer:
  Constraints:
    - VALID_OUTPUT → Target
    - REJECT_OUTPUT → Reject File
    
Reject File:
  Path: /data/rejects/customer_rejects_#BATCH_DATE#.csv
  Include: All source columns + REJECT_REASON
  Format: CSV with header
```

Add reject reason column:

```datastage
REJECT_REASON = 
  If IsNull(CUSTOMER_ID) Then "Missing Customer ID"
  Else If IsNull(EMAIL) Then "Missing Email"
  Else If Not(EMAIL Like '%@%') Then "Invalid Email Format"
  Else "Unknown Error"
```

### 5. Data Profiling

Profile data regularly:

```sql
-- Row counts
SELECT COUNT(*) FROM source_table;
SELECT COUNT(*) FROM target_table;

-- Null analysis
SELECT 
  COUNT(*) as total_rows,
  COUNT(column1) as column1_non_null,
  COUNT(column2) as column2_non_null,
  COUNT(*) - COUNT(column1) as column1_nulls
FROM table_name;

-- Duplicate analysis
SELECT column1, COUNT(*) as count
FROM table_name
GROUP BY column1
HAVING COUNT(*) > 1;

-- Value distribution
SELECT column1, COUNT(*) as frequency
FROM table_name
GROUP BY column1
ORDER BY frequency DESC
LIMIT 10;
```

## Performance Optimization

### 1. Parallel Processing

Enable partitioning for large datasets:

```datastage
Partitioning:
  Method: Hash
  Key: CUSTOMER_ID
  Nodes: 8
  
Sort:
  Perform in Parallel: Yes
  Stable Sort: No (if order doesn't matter)
```

### 2. Commit Intervals

Optimize commit intervals:

```
Small datasets (<10K rows): 1000
Medium datasets (10K-1M rows): 5000
Large datasets (>1M rows): 10000
```

```datastage
<Parameter Name="COMMIT_INTERVAL" Type="Integer" Default="5000"/>
```

### 3. Buffer Settings

Configure appropriate buffer sizes:

```datastage
Buffer Settings:
  Buffer Size: 10000 rows
  Buffer Free Run: 50%
  Max Memory: 2048 MB
```

### 4. Database Optimization

#### Use Bulk Loading

```datastage
Target Stage:
  Write Mode: Bulk Load
  Use Direct Path: Yes (Oracle)
  Use COPY: Yes (PostgreSQL)
```

#### Optimize SQL

```sql
-- BAD: Select all columns
SELECT * FROM large_table WHERE date_column = '2026-04-16';

-- GOOD: Select only needed columns
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE last_updated >= CURRENT_DATE - 1
  AND customer_status = 'ACTIVE';

-- Use indexes
CREATE INDEX idx_customers_last_updated ON customers(last_updated);
CREATE INDEX idx_customers_status ON customers(customer_status);
```

#### Minimize Lookups

```datastage
-- Cache small lookup tables
Lookup Stage:
  Cache: Yes
  Cache Size: 10000 rows
  
-- Use database joins for large lookups
-- Instead of DataStage lookup, use SQL JOIN in source query
```

### 5. Aggregation Optimization

```datastage
Aggregator:
  Type: Hash (for unsorted data)
  Type: Sort (for pre-sorted data)
  
  Hash Aggregator:
    Hash Table Size: 10000
    Partition: Yes
    
  Sort Aggregator:
    Input Must Be Sorted: Yes
    Perform Sort: No
```

### 6. Avoid Common Pitfalls

**DON'T**:
- Use `SELECT *` in source queries
- Perform lookups on large tables without caching
- Sort data multiple times
- Use sequential processing for large datasets
- Ignore database indexes

**DO**:
- Select only required columns
- Use database joins when possible
- Sort once and maintain sort order
- Enable parallel processing
- Create appropriate indexes

## Error Handling

### 1. Comprehensive Error Handling

Implement error handling at multiple levels:

```datastage
Job Level:
  - Abort After Rows: 1000 (reject threshold)
  - Warning Limit: 50
  - Email on Failure: Yes
  
Stage Level:
  - Reject Links: Yes
  - Error Handling: Continue
  
Row Level:
  - Constraints for validation
  - Reject reason tracking
```

### 2. Error Logging

Log all errors to control tables:

```sql
CREATE TABLE etl_error_log (
  error_id SERIAL PRIMARY KEY,
  job_name VARCHAR(100),
  run_id VARCHAR(50),
  error_timestamp TIMESTAMP,
  error_type VARCHAR(50),
  error_message TEXT,
  source_row TEXT,
  stack_trace TEXT
);
```

```datastage
Target: ERROR_LOG_TABLE
Columns:
  - JOB_NAME: #JOB_NAME#
  - RUN_ID: #RUN_ID#
  - ERROR_TIMESTAMP: CurrentTimestamp()
  - ERROR_TYPE: REJECT_REASON
  - ERROR_MESSAGE: Error details
  - SOURCE_ROW: Concatenated source columns
```

### 3. Retry Logic

Implement retry for transient failures:

```bash
#!/bin/bash
MAX_RETRIES=3
RETRY_DELAY=60

for i in $(seq 1 $MAX_RETRIES); do
  dsjob -run -wait -param BATCH_DATE=$(date +%Y-%m-%d) \
    PROJECT JOB_NAME
  
  if [ $? -eq 0 ]; then
    echo "Job succeeded"
    exit 0
  else
    echo "Attempt $i failed, retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
  fi
done

echo "Job failed after $MAX_RETRIES attempts"
exit 1
```

### 4. Graceful Degradation

Handle partial failures gracefully:

```datastage
# Continue processing even if some records fail
Transformer:
  Constraints:
    VALID_RECORDS → Continue to target
    INVALID_RECORDS → Log and continue
    
# Don't fail entire job for data quality issues below threshold
If REJECT_PERCENTAGE < 5% Then
  Continue
Else
  Abort with error
```

## Testing

### 1. Test Coverage

Test all aspects of your jobs:

```python
# Functional tests
- Job execution success
- Data transformation logic
- Business rule validation
- Error handling

# Data quality tests
- Row count validation
- Data completeness
- Format validation
- Referential integrity

# Performance tests
- Execution time
- Throughput
- Resource utilization
- Scalability

# Integration tests
- End-to-end workflows
- Job dependencies
- Cross-job consistency
```

### 2. Test Data

Use realistic test data:

```python
# Small dataset (unit tests)
test_data_small = 1000 rows

# Medium dataset (integration tests)
test_data_medium = 100000 rows

# Large dataset (performance tests)
test_data_large = 10000000 rows

# Edge cases
- Null values
- Empty strings
- Special characters
- Boundary values
- Duplicate records
```

### 3. Automated Testing

Automate test execution:

```bash
# Run tests in CI/CD pipeline
cd tests
python test_all_jobs.py

# Check exit code
if [ $? -ne 0 ]; then
  echo "Tests failed"
  exit 1
fi
```

### 4. Test Environments

Maintain separate test environments:

```
Development → Test → UAT → Production
```

Each environment should have:
- Separate databases
- Separate DataStage projects
- Environment-specific configurations
- Isolated test data

## Documentation

### 1. Job Documentation

Document every job:

```xml
<Job>
  <Description>
    Purpose: Extract customer data from source, transform, and load to warehouse
    Author: ETL Team
    Created: 2026-04-01
    Last Modified: 2026-04-16
    Version: 1.0.0
    
    Dependencies:
    - Source: CUSTOMER_SOURCE_DB
    - Target: CUSTOMER_DW
    - Prerequisites: None
    
    Business Rules:
    - BR-001: Customer age calculated from DOB
    - BR-002: Email must be valid format
    - BR-003: Phone numbers standardized to digits only
    
    Performance:
    - Expected throughput: 10,000 rows/minute
    - Typical runtime: 5-10 minutes
    - Resource requirements: 2GB RAM, 4 CPU cores
  </Description>
</Job>
```

### 2. Inline Comments

Add comments for complex logic:

```datastage
# Calculate customer lifetime value
# Formula: (Average Order Value × Purchase Frequency × Customer Lifespan)
CUSTOMER_LTV = AVG_ORDER_VALUE * PURCHASE_FREQUENCY * CUSTOMER_LIFESPAN

# Apply discount tier based on LTV
# Tier 1: LTV > $10,000 → 15% discount
# Tier 2: LTV > $5,000 → 10% discount
# Tier 3: LTV > $1,000 → 5% discount
# Tier 4: LTV <= $1,000 → 0% discount
DISCOUNT_TIER = 
  If CUSTOMER_LTV > 10000 Then "TIER1"
  Else If CUSTOMER_LTV > 5000 Then "TIER2"
  Else If CUSTOMER_LTV > 1000 Then "TIER3"
  Else "TIER4"
```

### 3. Change Log

Maintain a change log:

```markdown
# Change Log

## [1.0.1] - 2026-04-16
### Changed
- Increased commit interval from 1000 to 5000 for better performance
- Updated email validation regex

### Fixed
- Fixed null handling in phone number cleaning
- Corrected age calculation for leap years

## [1.0.0] - 2026-04-01
### Added
- Initial release
- Customer data ETL pipeline
- Data quality validation
- Reject handling
```

### 4. README Files

Create README files for each component:

```markdown
# Customer Data ETL

## Overview
Extracts customer data from operational database and loads into data warehouse.

## Usage
```bash
dsjob -run -wait -param BATCH_DATE=2026-04-16 PROJECT CUSTOMER_DATA_ETL
```

## Parameters
- SOURCE_DB_CONN: Source database connection
- TARGET_DB_CONN: Target database connection
- BATCH_DATE: Processing date
- COMMIT_INTERVAL: Rows per commit (default: 1000)

## Dependencies
- Source table: CUSTOMERS
- Target table: DW_CUSTOMERS
- Lookup table: CUSTOMER_SEGMENTS

## Monitoring
- Check reject file: /data/rejects/customer_rejects_YYYY-MM-DD.csv
- Review job log: $DSHOME/Logs/CUSTOMER_DATA_ETL.log
```

## Security

### 1. Credential Management

**DON'T**: Hard-code passwords

```xml
<!-- BAD -->
<Password>mypassword123</Password>
```

**DO**: Use environment variables or secrets management

```xml
<!-- GOOD -->
<Password>${DB_PASSWORD}</Password>
```

### 2. Data Masking

Mask sensitive data in non-production environments:

```datastage
# Mask email addresses
EMAIL_MASKED = 
  If ETL_ENV = "PRODUCTION" Then EMAIL
  Else "masked_" : CUSTOMER_ID : "@example.com"

# Mask credit card numbers
CC_MASKED = 
  If ETL_ENV = "PRODUCTION" Then CREDIT_CARD
  Else "XXXX-XXXX-XXXX-" : Right(CREDIT_CARD, 4)

# Mask SSN
SSN_MASKED = 
  If ETL_ENV = "PRODUCTION" Then SSN
  Else "XXX-XX-" : Right(SSN, 4)
```

### 3. Access Control

Implement role-based access:

```
Developers: Read/Write in DEV, Read in TEST
Operators: Execute in PROD, Read logs
Admins: Full access to all environments
```

### 4. Audit Logging

Log all data access:

```sql
CREATE TABLE etl_audit_log (
  audit_id SERIAL PRIMARY KEY,
  job_name VARCHAR(100),
  user_name VARCHAR(50),
  action VARCHAR(50),
  timestamp TIMESTAMP,
  rows_affected INTEGER,
  details TEXT
);
```

## Maintenance

### 1. Regular Reviews

Schedule regular reviews:

```
Weekly: Review job failures and performance
Monthly: Review and optimize slow jobs
Quarterly: Review and update documentation
Annually: Review and refactor legacy jobs
```

### 2. Performance Monitoring

Monitor key metrics:

```sql
-- Job execution times
SELECT 
  job_name,
  AVG(execution_time) as avg_time,
  MAX(execution_time) as max_time,
  MIN(execution_time) as min_time
FROM etl_job_log
WHERE run_date >= CURRENT_DATE - 30
GROUP BY job_name
ORDER BY avg_time DESC;

-- Row counts and throughput
SELECT 
  job_name,
  AVG(rows_processed) as avg_rows,
  AVG(rows_processed / execution_time) as avg_throughput
FROM etl_job_log
WHERE run_date >= CURRENT_DATE - 30
GROUP BY job_name;
```

### 3. Cleanup

Regular cleanup tasks:

```bash
# Clean old log files
find $DSHOME/Logs -name "*.log" -mtime +30 -delete

# Clean old reject files
find /data/rejects -name "*.csv" -mtime +90 -delete

# Archive old audit logs
psql -c "DELETE FROM etl_audit_log WHERE timestamp < CURRENT_DATE - 365"
```

### 4. Version Control

Use version control for all artifacts:

```bash
# Initialize git repository
git init

# Add files
git add jobs/*.dsx
git add config/*.json
git add tests/*.py
git add docs/*.md

# Commit changes
git commit -m "Initial commit"

# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
```

## Deployment

### 1. Deployment Process

Follow a structured deployment process:

```
1. Development → Code and test in DEV
2. Code Review → Peer review changes
3. Testing → Deploy to TEST environment
4. UAT → User acceptance testing
5. Production → Deploy to PROD with approval
```

### 2. Deployment Checklist

```markdown
- [ ] Code reviewed and approved
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Configuration verified
- [ ] Backup created
- [ ] Rollback plan prepared
- [ ] Stakeholders notified
- [ ] Deployment window scheduled
```

### 3. Rollback Plan

Always have a rollback plan:

```bash
# Backup current version
dsjob -export -server prod-server -user admin \
  -project PROD_PROJECT CUSTOMER_DATA_ETL \
  > backup/CUSTOMER_DATA_ETL_$(date +%Y%m%d).dsx

# If deployment fails, restore backup
dsjob -import -server prod-server -user admin \
  -project PROD_PROJECT \
  backup/CUSTOMER_DATA_ETL_20260415.dsx
```

### 4. Post-Deployment Validation

Validate after deployment:

```bash
# Run smoke tests
python tests/smoke_tests.py

# Check job execution
dsjob -run -wait PROJECT JOB_NAME

# Verify data quality
python tests/data_quality_checks.py

# Monitor for errors
tail -f $DSHOME/Logs/JOB_NAME.log
```

## Summary Checklist

### Job Design
- [ ] Descriptive naming conventions
- [ ] Modular, reusable design
- [ ] Fully parameterized
- [ ] Well-organized stages
- [ ] Documented with annotations

### Data Quality
- [ ] Input validation implemented
- [ ] Data cleansing rules applied
- [ ] Business rules validated
- [ ] Reject handling configured
- [ ] Regular data profiling

### Performance
- [ ] Parallel processing enabled
- [ ] Optimal commit intervals
- [ ] Appropriate buffer sizes
- [ ] Bulk loading used
- [ ] SQL optimized

### Error Handling
- [ ] Comprehensive error handling
- [ ] Error logging implemented
- [ ] Retry logic for transient failures
- [ ] Graceful degradation

### Testing
- [ ] Comprehensive test coverage
- [ ] Realistic test data
- [ ] Automated testing
- [ ] Separate test environments

### Documentation
- [ ] Job documentation complete
- [ ] Inline comments for complex logic
- [ ] Change log maintained
- [ ] README files created

### Security
- [ ] No hard-coded credentials
- [ ] Sensitive data masked
- [ ] Access control implemented
- [ ] Audit logging enabled

### Maintenance
- [ ] Regular reviews scheduled
- [ ] Performance monitoring
- [ ] Cleanup tasks automated
- [ ] Version control used

### Deployment
- [ ] Structured deployment process
- [ ] Deployment checklist followed
- [ ] Rollback plan prepared
- [ ] Post-deployment validation

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)