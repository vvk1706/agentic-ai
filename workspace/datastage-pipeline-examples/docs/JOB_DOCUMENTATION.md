# DataStage Job Documentation

Comprehensive documentation for all DataStage pipeline jobs in this repository.

## Table of Contents

- [Customer Data ETL](#customer-data-etl)
- [Sales Data Aggregation](#sales-data-aggregation)
- [Data Quality Validation](#data-quality-validation)
- [Incremental Load](#incremental-load)
- [Master Data Management](#master-data-management)

---

## Customer Data ETL

**Job Name**: `CUSTOMER_DATA_ETL`  
**File**: [`jobs/customer_data_etl.dsx`](../jobs/customer_data_etl.dsx)  
**Version**: 1.0.0

### Purpose

Extracts customer data from source database, performs data cleansing and transformation, and loads into the target data warehouse with comprehensive validation and reject handling.

### Job Flow

```
SOURCE_CUSTOMERS (ODBC)
    ↓
TRANSFORM_CUSTOMERS (Transformer)
    ↓
    ├─→ VALID_OUTPUT → TARGET_CUSTOMER_DW (ODBC)
    └─→ REJECT_OUTPUT → REJECT_FILE (Sequential File)
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `SOURCE_DB_CONN` | String | Yes | CUSTOMER_SOURCE_DB | Source database connection name |
| `TARGET_DB_CONN` | String | Yes | CUSTOMER_DW | Target database connection name |
| `BATCH_DATE` | Date | Yes | CurrentDate() | Processing batch date |
| `COMMIT_INTERVAL` | Integer | No | 1000 | Number of rows per commit |

### Source Stage: SOURCE_CUSTOMERS

**Type**: ODBC Connector  
**Table**: CUSTOMERS

#### Source Columns

| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| CUSTOMER_ID | INTEGER | No | Unique customer identifier |
| FIRST_NAME | VARCHAR(50) | Yes | Customer first name |
| LAST_NAME | VARCHAR(50) | Yes | Customer last name |
| EMAIL | VARCHAR(100) | Yes | Email address |
| PHONE | VARCHAR(20) | Yes | Phone number |
| ADDRESS | VARCHAR(200) | Yes | Street address |
| CITY | VARCHAR(50) | Yes | City |
| STATE | VARCHAR(50) | Yes | State/Province |
| ZIP_CODE | VARCHAR(10) | Yes | Postal code |
| COUNTRY | VARCHAR(50) | Yes | Country |
| DATE_OF_BIRTH | DATE | Yes | Date of birth |
| REGISTRATION_DATE | TIMESTAMP | Yes | Account registration date |
| CUSTOMER_STATUS | VARCHAR(20) | Yes | Customer status (ACTIVE/INACTIVE) |
| LAST_UPDATED | TIMESTAMP | Yes | Last update timestamp |

#### Source Query

```sql
SELECT 
  CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE,
  ADDRESS, CITY, STATE, ZIP_CODE, COUNTRY,
  DATE_OF_BIRTH, REGISTRATION_DATE, CUSTOMER_STATUS, LAST_UPDATED
FROM CUSTOMERS
WHERE LAST_UPDATED >= CURRENT_DATE - 1
```

### Transformation Stage: TRANSFORM_CUSTOMERS

**Type**: Transformer

#### Derivations

| Derived Column | Expression | Description |
|----------------|------------|-------------|
| `FULL_NAME` | `Trim(FIRST_NAME) : " " : Trim(LAST_NAME)` | Concatenate first and last name |
| `EMAIL_CLEAN` | `Trim(Upcase(EMAIL))` | Standardize email to uppercase |
| `PHONE_CLEAN` | `Convert("[^0-9]", "", PHONE)` | Remove non-numeric characters |
| `AGE` | `YearFromDate(CurrentDate()) - YearFromDate(DATE_OF_BIRTH)` | Calculate age from DOB |
| `CUSTOMER_SEGMENT` | See below | Segment customers by age |
| `IS_ACTIVE` | `If CUSTOMER_STATUS = "ACTIVE" Then 1 Else 0` | Convert status to flag |
| `ETL_TIMESTAMP` | `CurrentTimestamp()` | Record processing timestamp |
| `ETL_BATCH_ID` | `#BATCH_DATE#` | Batch identifier |

#### Customer Segmentation Logic

```
If AGE < 25 Then "YOUNG_ADULT"
Else If AGE < 45 Then "MIDDLE_AGE"
Else If AGE < 65 Then "SENIOR"
Else "ELDERLY"
```

#### Constraints

**VALID_RECORDS** (Output: VALID_OUTPUT):
```
Not(IsNull(CUSTOMER_ID)) And Not(IsNull(EMAIL)) And Len(EMAIL_CLEAN) > 0
```

**INVALID_RECORDS** (Output: REJECT_OUTPUT):
```
Otherwise
```

### Target Stage: TARGET_CUSTOMER_DW

**Type**: ODBC Connector  
**Table**: DW_CUSTOMERS  
**Write Mode**: Insert  
**Update Action**: Update  
**Commit Interval**: Parameter-driven

#### Before SQL

```sql
TRUNCATE TABLE DW_CUSTOMERS_STAGING
```

#### After SQL

```sql
MERGE INTO DW_CUSTOMERS tgt
USING DW_CUSTOMERS_STAGING src
ON tgt.CUSTOMER_ID = src.CUSTOMER_ID
WHEN MATCHED THEN UPDATE SET
  tgt.FULL_NAME = src.FULL_NAME,
  tgt.EMAIL = src.EMAIL_CLEAN,
  tgt.PHONE = src.PHONE_CLEAN,
  tgt.AGE = src.AGE,
  tgt.CUSTOMER_SEGMENT = src.CUSTOMER_SEGMENT,
  tgt.IS_ACTIVE = src.IS_ACTIVE,
  tgt.LAST_UPDATED = src.ETL_TIMESTAMP
WHEN NOT MATCHED THEN INSERT VALUES (
  src.CUSTOMER_ID, src.FULL_NAME, src.EMAIL_CLEAN, 
  src.PHONE_CLEAN, src.AGE, src.CUSTOMER_SEGMENT, 
  src.IS_ACTIVE, src.ETL_TIMESTAMP
)
```

### Reject Stage: REJECT_FILE

**Type**: Sequential File  
**Format**: Delimited (CSV)  
**Path**: `/data/rejects/customer_rejects_#BATCH_DATE#.csv`  
**Include Header**: Yes

### Usage Examples

#### Command Line Execution

```bash
dsjob -run -wait \
  -param SOURCE_DB_CONN=CUSTOMER_SOURCE_DB \
  -param TARGET_DB_CONN=CUSTOMER_DW \
  -param BATCH_DATE=2026-04-16 \
  -param COMMIT_INTERVAL=1000 \
  -server your-server \
  -user your-username \
  YOUR_PROJECT CUSTOMER_DATA_ETL
```

#### Scheduled Execution (Cron)

```bash
# Daily at 2 AM
0 2 * * * /opt/IBM/InformationServer/Server/DSEngine/bin/dsjob -run -wait \
  -param BATCH_DATE=$(date +\%Y-\%m-\%d) \
  -server prod-server -user etl_user \
  PROD_PROJECT CUSTOMER_DATA_ETL
```

### Performance Considerations

- **Commit Interval**: Adjust based on data volume (1000-5000 recommended)
- **Parallel Processing**: Enable partitioning for large datasets
- **Indexing**: Ensure CUSTOMER_ID is indexed in target table
- **Expected Throughput**: ~10,000 rows/minute on standard hardware

### Monitoring

#### Key Metrics

- Rows read from source
- Rows written to target
- Rows rejected
- Execution time
- Throughput (rows/second)

#### Log Messages

- `Job started with batch date: YYYY-MM-DD`
- `Source extraction complete: N rows`
- `Transformation complete: N valid, M rejected`
- `Target load complete: N rows inserted/updated`
- `Job completed successfully`

---

## Sales Data Aggregation

**Job Name**: `SALES_DATA_AGGREGATION`  
**File**: [`jobs/sales_data_aggregation.dsx`](../jobs/sales_data_aggregation.dsx)  
**Version**: 1.0.0

### Purpose

Aggregates daily sales transactions by product, region, and time period to generate summary reports for business intelligence and analytics.

### Job Flow

```
SOURCE_SALES_TRANSACTIONS (ODBC)
    ↓
TRANSFORM_SALES_METRICS (Transformer)
    ↓
    ├─→ AGG_DAILY_PRODUCT_SALES (Aggregator) → TARGET_PRODUCT_SALES (ODBC)
    └─→ AGG_REGIONAL_SALES (Aggregator) → TARGET_REGIONAL_SALES (ODBC)
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `SOURCE_DB_CONN` | String | Yes | SALES_TRANSACTIONAL_DB | Source database connection |
| `TARGET_DB_CONN` | String | Yes | SALES_DW | Target database connection |
| `START_DATE` | Date | Yes | CurrentDate() - 1 | Start date for processing |
| `END_DATE` | Date | Yes | CurrentDate() | End date for processing |
| `AGGREGATION_LEVEL` | String | Yes | DAILY | Aggregation level (DAILY/WEEKLY/MONTHLY) |

### Source Stage: SOURCE_SALES_TRANSACTIONS

**Type**: ODBC Connector  
**Table**: SALES_TRANSACTIONS

#### Source Query

```sql
SELECT 
  TRANSACTION_ID, TRANSACTION_DATE, TRANSACTION_TIME,
  PRODUCT_ID, PRODUCT_NAME, PRODUCT_CATEGORY,
  QUANTITY, UNIT_PRICE, DISCOUNT_AMOUNT, TAX_AMOUNT, TOTAL_AMOUNT,
  CUSTOMER_ID, STORE_ID, STORE_NAME, REGION, COUNTRY,
  PAYMENT_METHOD, SALES_CHANNEL
FROM SALES_TRANSACTIONS
WHERE TRANSACTION_DATE BETWEEN #START_DATE# AND #END_DATE#
  AND TRANSACTION_STATUS = 'COMPLETED'
```

### Transformation Stage: TRANSFORM_SALES_METRICS

**Type**: Transformer

#### Calculated Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| `NET_AMOUNT` | `TOTAL_AMOUNT - DISCOUNT_AMOUNT` | Net sales amount |
| `GROSS_PROFIT` | `NET_AMOUNT - TAX_AMOUNT` | Gross profit |
| `REVENUE` | `QUANTITY * UNIT_PRICE` | Gross revenue |
| `DISCOUNT_PERCENTAGE` | `(DISCOUNT_AMOUNT / REVENUE) * 100` | Discount rate |
| `YEAR` | `YearFromDate(TRANSACTION_DATE)` | Transaction year |
| `MONTH` | `MonthFromDate(TRANSACTION_DATE)` | Transaction month |
| `QUARTER` | `QuarterFromDate(TRANSACTION_DATE)` | Transaction quarter |
| `DAY_OF_WEEK` | `WeekdayFromDate(TRANSACTION_DATE)` | Day of week |
| `HOUR_OF_DAY` | `HourFromTime(TRANSACTION_TIME)` | Hour of day |

### Aggregator Stage: AGG_DAILY_PRODUCT_SALES

**Type**: Aggregator (Hash)

#### Grouping Keys

- TRANSACTION_DATE
- PRODUCT_ID
- PRODUCT_NAME
- PRODUCT_CATEGORY

#### Aggregations

| Aggregation | Function | Source Column | Description |
|-------------|----------|---------------|-------------|
| `TOTAL_QUANTITY` | Sum | QUANTITY | Total units sold |
| `TOTAL_REVENUE` | Sum | REVENUE | Total revenue |
| `TOTAL_DISCOUNT` | Sum | DISCOUNT_AMOUNT | Total discounts |
| `TOTAL_TAX` | Sum | TAX_AMOUNT | Total tax |
| `TOTAL_NET_AMOUNT` | Sum | NET_AMOUNT | Total net amount |
| `TRANSACTION_COUNT` | Count | TRANSACTION_ID | Number of transactions |
| `UNIQUE_CUSTOMERS` | CountDistinct | CUSTOMER_ID | Unique customer count |
| `AVG_TRANSACTION_VALUE` | Avg | TOTAL_AMOUNT | Average transaction value |
| `MAX_TRANSACTION_VALUE` | Max | TOTAL_AMOUNT | Maximum transaction value |
| `MIN_TRANSACTION_VALUE` | Min | TOTAL_AMOUNT | Minimum transaction value |

### Aggregator Stage: AGG_REGIONAL_SALES

**Type**: Aggregator (Hash)

#### Grouping Keys

- TRANSACTION_DATE
- REGION
- COUNTRY
- STORE_ID
- STORE_NAME

#### Aggregations

| Aggregation | Function | Source Column | Description |
|-------------|----------|---------------|-------------|
| `TOTAL_SALES` | Sum | TOTAL_AMOUNT | Total sales amount |
| `TOTAL_TRANSACTIONS` | Count | TRANSACTION_ID | Transaction count |
| `TOTAL_CUSTOMERS` | CountDistinct | CUSTOMER_ID | Unique customers |
| `AVG_BASKET_SIZE` | Avg | QUANTITY | Average basket size |

### Target Stages

#### TARGET_PRODUCT_SALES

**Table**: DW_PRODUCT_SALES_DAILY  
**Write Mode**: Append  
**Update Action**: Replace  
**Update Key**: TRANSACTION_DATE, PRODUCT_ID

#### TARGET_REGIONAL_SALES

**Table**: DW_REGIONAL_SALES_DAILY  
**Write Mode**: Append  
**Update Action**: Replace  
**Update Key**: TRANSACTION_DATE, REGION, STORE_ID

### Usage Examples

```bash
# Daily aggregation
dsjob -run -wait \
  -param START_DATE=2026-04-15 \
  -param END_DATE=2026-04-16 \
  -param AGGREGATION_LEVEL=DAILY \
  -server your-server -user your-username \
  YOUR_PROJECT SALES_DATA_AGGREGATION

# Weekly aggregation
dsjob -run -wait \
  -param START_DATE=2026-04-09 \
  -param END_DATE=2026-04-16 \
  -param AGGREGATION_LEVEL=WEEKLY \
  -server your-server -user your-username \
  YOUR_PROJECT SALES_DATA_AGGREGATION
```

### Performance Considerations

- **Hash Partitioning**: Enable for large datasets
- **Aggregation Buffer**: Increase for better performance
- **Expected Throughput**: ~50,000 transactions/minute
- **Memory Requirements**: 2-4 GB for typical daily volumes

---

## Data Quality Validation

**Job Name**: `DATA_QUALITY_VALIDATION`  
**File**: [`jobs/data_quality_validation.dsx`](../jobs/data_quality_validation.dsx)  
**Version**: 1.0.0

### Purpose

Validates data against business rules and quality standards, generating comprehensive quality reports and metrics.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `SOURCE_DB_CONN` | String | Yes | - | Source database connection |
| `DQ_RULES_DB_CONN` | String | Yes | - | Data quality rules database |
| `TABLE_NAME` | String | Yes | - | Table to validate |
| `VALIDATION_DATE` | Date | Yes | CurrentDate() | Validation date |
| `QUALITY_THRESHOLD` | Integer | Yes | 95 | Quality score threshold (%) |
| `FAIL_ON_THRESHOLD` | Integer | No | 0 | Fail job if below threshold (0/1) |

### Quality Checks

#### Completeness Checks

- Null value validation
- Required field validation
- Empty string detection

#### Validity Checks

- Email format validation
- Phone number format validation
- Date range validation
- Numeric range validation

#### Consistency Checks

- Cross-field validation
- Referential integrity
- Business rule validation

#### Accuracy Checks

- Domain validation
- Lookup validation
- Pattern matching

### Quality Scoring

Quality score calculated as:
```
Quality Score = (Passed Rules / Total Rules) * 100
```

### Usage Example

```bash
dsjob -run -wait \
  -param SOURCE_DB_CONN=STAGING_DB \
  -param DQ_RULES_DB_CONN=DQ_METADATA_DB \
  -param TABLE_NAME=CUSTOMER_STAGING \
  -param VALIDATION_DATE=2026-04-16 \
  -param QUALITY_THRESHOLD=95 \
  -param FAIL_ON_THRESHOLD=1 \
  -server your-server -user your-username \
  YOUR_PROJECT DATA_QUALITY_VALIDATION
```

---

## Incremental Load

**Job Name**: `INCREMENTAL_LOAD`  
**File**: [`jobs/incremental_load.dsx`](../jobs/incremental_load.dsx)  
**Version**: 1.0.0

### Purpose

Performs incremental data loading using Change Data Capture (CDC) approach with SCD Type 2 implementation for historical tracking.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `SOURCE_DB_CONN` | String | Yes | - | Source database connection |
| `TARGET_DB_CONN` | String | Yes | - | Target database connection |
| `CONTROL_DB_CONN` | String | Yes | - | Control database connection |
| `TABLE_NAME` | String | Yes | - | Source table name |
| `LAST_LOAD_TIMESTAMP` | Timestamp | Yes | - | Last load timestamp |
| `CURRENT_LOAD_TIMESTAMP` | Timestamp | Yes | CurrentTimestamp() | Current load timestamp |
| `SCD_TYPE` | Integer | Yes | 2 | SCD Type (1 or 2) |

### CDC Operations

| Operation | Description | Action |
|-----------|-------------|--------|
| INSERT | New records | Insert into target |
| UPDATE | Changed records | SCD Type 2: Insert new version, expire old |
| NO_CHANGE | Unchanged records | Skip processing |

### SCD Type 2 Implementation

#### Target Table Structure

```sql
CREATE TABLE target_table (
  surrogate_key INTEGER PRIMARY KEY,
  business_key VARCHAR(50),
  -- data columns --
  effective_date TIMESTAMP,
  expiry_date TIMESTAMP,
  is_current INTEGER,
  record_hash VARCHAR(64)
);
```

### Usage Example

```bash
dsjob -run -wait \
  -param SOURCE_DB_CONN=OPERATIONAL_DB \
  -param TARGET_DB_CONN=DATA_WAREHOUSE \
  -param CONTROL_DB_CONN=ETL_CONTROL_DB \
  -param TABLE_NAME=PRODUCTS \
  -param LAST_LOAD_TIMESTAMP="2026-04-15 00:00:00" \
  -param CURRENT_LOAD_TIMESTAMP="2026-04-16 00:00:00" \
  -param SCD_TYPE=2 \
  -server your-server -user your-username \
  YOUR_PROJECT INCREMENTAL_LOAD
```

---

## Master Data Management

**Job Name**: `MASTER_DATA_MANAGEMENT`  
**File**: [`jobs/master_data_management.dsx`](../jobs/master_data_management.dsx)  
**Version**: 1.0.0

### Purpose

Consolidates and manages master data from multiple sources with deduplication, fuzzy matching, and golden record creation.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `SOURCE1_DB_CONN` | String | Yes | - | CRM database connection |
| `SOURCE2_DB_CONN` | String | Yes | - | ERP database connection |
| `SOURCE3_DB_CONN` | String | Yes | - | E-commerce database connection |
| `MDM_DB_CONN` | String | Yes | - | MDM database connection |
| `MATCH_THRESHOLD` | Integer | Yes | 85 | Match threshold score (0-100) |
| `AUTO_MERGE` | Integer | Yes | 1 | Auto merge high confidence matches (0/1) |
| `PROCESSING_DATE` | Date | Yes | CurrentDate() | Processing date |

### Matching Algorithms

| Algorithm | Description | Weight |
|-----------|-------------|--------|
| Name Matching | Soundex algorithm | 30% |
| Email Matching | Exact match | 40% |
| Phone Matching | Normalized comparison | 20% |
| Address Matching | Fuzzy comparison | 10% |

### Match Confidence Levels

- **Exact Match** (100%): All key fields match exactly
- **High Confidence** (85-99%): Strong match, auto-merge eligible
- **Medium Confidence** (70-84%): Possible match, manual review
- **Low Confidence** (<70%): Unlikely match, separate records

### Survivorship Rules

When merging records, the following rules determine which values survive:

1. **Most Recent**: Use most recently updated value
2. **Most Complete**: Use value with most data
3. **Most Trusted**: Use value from most trusted source
4. **Most Frequent**: Use most common value across sources

### Usage Example

```bash
dsjob -run -wait \
  -param SOURCE1_DB_CONN=CRM_DB \
  -param SOURCE2_DB_CONN=ERP_DB \
  -param SOURCE3_DB_CONN=ECOMMERCE_DB \
  -param MDM_DB_CONN=MDM_MASTER_DB \
  -param MATCH_THRESHOLD=85 \
  -param AUTO_MERGE=1 \
  -param PROCESSING_DATE=2026-04-16 \
  -server your-server -user your-username \
  YOUR_PROJECT MASTER_DATA_MANAGEMENT
```

---

## Common Job Patterns

### Error Handling

All jobs implement standard error handling:

- Reject links for invalid data
- Error logging to control tables
- Email notifications on failure
- Automatic retry logic

### Audit Columns

Standard audit columns added to all targets:

- `ETL_INSERT_DATE`: Record creation timestamp
- `ETL_UPDATE_DATE`: Last update timestamp
- `ETL_BATCH_ID`: Batch identifier
- `ETL_SOURCE_SYSTEM`: Source system identifier

### Logging

All jobs log to standard locations:

- Job logs: `$DSHOME/Logs`
- Reject files: `/data/rejects/`
- Audit tables: ETL_CONTROL_DB

---

**Related Documentation**:
- [Getting Started](GETTING_STARTED.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)