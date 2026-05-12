# IBM DataStage Pipeline Examples

A comprehensive repository of IBM DataStage pipeline job examples with complete test suites. This repository demonstrates best practices for building, testing, and maintaining DataStage ETL pipelines.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Pipeline Jobs](#pipeline-jobs)
- [Test Suite](#test-suite)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains 5 production-ready DataStage pipeline examples covering common ETL patterns:

1. **Customer Data ETL** - Full ETL pipeline with data cleansing and transformation
2. **Sales Data Aggregation** - Multi-level aggregation with performance optimization
3. **Data Quality Validation** - Comprehensive data quality checks and reporting
4. **Incremental Load** - CDC-based incremental loading with SCD Type 2
5. **Master Data Management** - Multi-source data consolidation with deduplication

Each job includes:
- Complete DataStage job definition (.dsx files)
- Comprehensive test suite
- Documentation and usage examples
- Sample data and configurations

## 📁 Repository Structure

```
datastage-pipeline-examples/
├── jobs/                           # DataStage job definitions
│   ├── customer_data_etl.dsx
│   ├── sales_data_aggregation.dsx
│   ├── data_quality_validation.dsx
│   ├── incremental_load.dsx
│   └── master_data_management.dsx
├── tests/                          # Test suite
│   ├── test_framework.py          # Core testing framework
│   ├── test_customer_etl.py       # Customer ETL tests
│   └── test_all_jobs.py           # Comprehensive test suite
├── data/                           # Sample data files
│   ├── sample_customers.csv
│   ├── sample_sales.csv
│   └── sample_products.csv
├── config/                         # Configuration files
│   ├── connections.json
│   ├── parameters.json
│   └── test_config.json
├── docs/                           # Additional documentation
│   ├── job_specifications.md
│   ├── testing_guide.md
│   └── deployment_guide.md
└── README.md                       # This file
```

## 🔧 Pipeline Jobs

### 1. Customer Data ETL (`customer_data_etl.dsx`)

**Purpose**: Extract customer data from source database, transform and cleanse it, then load into data warehouse.

**Key Features**:
- Data extraction from ODBC source
- Name standardization and concatenation
- Email and phone number validation
- Age calculation and customer segmentation
- Reject handling for invalid records
- Incremental loading support

**Parameters**:
- `SOURCE_DB_CONN`: Source database connection
- `TARGET_DB_CONN`: Target database connection
- `BATCH_DATE`: Processing date
- `COMMIT_INTERVAL`: Commit interval (default: 1000)

**Stages**:
1. Source: ODBC Connector (SOURCE_CUSTOMERS)
2. Transformer: Data cleansing and enrichment
3. Target: Data warehouse (TARGET_CUSTOMER_DW)
4. Reject: Invalid records file

### 2. Sales Data Aggregation (`sales_data_aggregation.dsx`)

**Purpose**: Aggregate daily sales transactions by product, region, and time period.

**Key Features**:
- Multi-source transaction processing
- Product-level aggregation
- Regional sales summaries
- Time-based aggregations (daily/weekly/monthly)
- Performance metrics calculation
- Parallel processing support

**Parameters**:
- `SOURCE_DB_CONN`: Source database connection
- `TARGET_DB_CONN`: Target database connection
- `START_DATE`: Start date for processing
- `END_DATE`: End date for processing
- `AGGREGATION_LEVEL`: DAILY/WEEKLY/MONTHLY

**Aggregations**:
- Total quantity, revenue, discounts, tax
- Transaction counts
- Unique customer counts
- Average/min/max transaction values

### 3. Data Quality Validation (`data_quality_validation.dsx`)

**Purpose**: Validate data against business rules and quality standards.

**Key Features**:
- Completeness checks (null validation)
- Validity checks (format validation)
- Consistency checks (cross-field validation)
- Accuracy checks (domain validation)
- Quality scoring (0-100 scale)
- Automated reporting

**Parameters**:
- `SOURCE_DB_CONN`: Source database connection
- `DQ_RULES_DB_CONN`: Data quality rules database
- `TABLE_NAME`: Table to validate
- `VALIDATION_DATE`: Validation date
- `QUALITY_THRESHOLD`: Quality score threshold (%)
- `FAIL_ON_THRESHOLD`: Fail job if below threshold

**Quality Checks**:
- Email format validation
- Phone number validation
- Date range validation
- Address completeness
- Name consistency

### 4. Incremental Load (`incremental_load.dsx`)

**Purpose**: Perform incremental data loading using CDC (Change Data Capture) approach.

**Key Features**:
- Change Data Capture (CDC)
- SCD Type 2 implementation
- Hash-based change detection
- Automatic versioning
- Audit trail maintenance
- Load statistics tracking

**Parameters**:
- `SOURCE_DB_CONN`: Source database connection
- `TARGET_DB_CONN`: Target database connection
- `CONTROL_DB_CONN`: Control database connection
- `TABLE_NAME`: Source table name
- `LAST_LOAD_TIMESTAMP`: Last load timestamp
- `CURRENT_LOAD_TIMESTAMP`: Current load timestamp
- `SCD_TYPE`: SCD Type (1 or 2)

**CDC Operations**:
- INSERT: New records
- UPDATE: Changed records (SCD Type 2)
- NO_CHANGE: Unchanged records

### 5. Master Data Management (`master_data_management.dsx`)

**Purpose**: Consolidate and manage master data from multiple sources with deduplication.

**Key Features**:
- Multi-source data integration (CRM, ERP, E-commerce)
- Data standardization
- Fuzzy matching algorithms
- Confidence scoring
- Automatic and manual merge workflows
- Survivorship rules
- Golden record creation

**Parameters**:
- `SOURCE1_DB_CONN`: CRM database connection
- `SOURCE2_DB_CONN`: ERP database connection
- `SOURCE3_DB_CONN`: E-commerce database connection
- `MDM_DB_CONN`: MDM database connection
- `MATCH_THRESHOLD`: Match threshold score (0-100)
- `AUTO_MERGE`: Auto merge high confidence matches
- `PROCESSING_DATE`: Processing date

**Matching Algorithms**:
- Name matching (Soundex)
- Email exact matching
- Phone number matching
- Address matching
- Composite key matching

## 🧪 Test Suite

### Test Framework (`test_framework.py`)

Core testing framework providing:
- Job execution utilities
- Data validation functions
- Quality checks
- Performance metrics
- Test result reporting
- JSON export capabilities

### Test Categories

1. **Functional Tests**
   - Job execution success
   - Data transformation logic
   - Business rule validation
   - Error handling

2. **Data Quality Tests**
   - Row count validation
   - Data completeness
   - Format validation
   - Referential integrity

3. **Performance Tests**
   - Execution time
   - Throughput (rows/second)
   - Resource utilization
   - Scalability

4. **Integration Tests**
   - End-to-end workflows
   - Job dependencies
   - Cross-job data consistency

## 🚀 Getting Started

### Prerequisites

- IBM InfoSphere DataStage 11.7 or higher
- Python 3.8 or higher (for test suite)
- Database connections configured
- Appropriate permissions for source and target systems

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-org/datastage-pipeline-examples.git
cd datastage-pipeline-examples
```

2. **Import DataStage jobs**:
```bash
# Using dsjob command
dsjob -import -server <server> -user <username> -project <project> jobs/customer_data_etl.dsx
dsjob -import -server <server> -user <username> -project <project> jobs/sales_data_aggregation.dsx
dsjob -import -server <server> -user <username> -project <project> jobs/data_quality_validation.dsx
dsjob -import -server <server> -user <username> -project <project> jobs/incremental_load.dsx
dsjob -import -server <server> -user <username> -project <project> jobs/master_data_management.dsx
```

3. **Install Python dependencies** (for testing):
```bash
pip install -r requirements.txt
```

4. **Configure connections**:
Edit `config/connections.json` with your database connection details.

## 💻 Usage

### Running Jobs

#### Using DataStage Director:
1. Open DataStage Director
2. Select the project
3. Right-click on the job
4. Select "Run"
5. Set parameters
6. Click "Run"

#### Using Command Line:
```bash
# Run Customer ETL job
dsjob -run -wait \
  -param SOURCE_DB_CONN=CUSTOMER_SOURCE_DB \
  -param TARGET_DB_CONN=CUSTOMER_DW \
  -param BATCH_DATE=2026-04-09 \
  -param COMMIT_INTERVAL=1000 \
  <project> CUSTOMER_DATA_ETL

# Run Sales Aggregation job
dsjob -run -wait \
  -param SOURCE_DB_CONN=SALES_TRANSACTIONAL_DB \
  -param TARGET_DB_CONN=SALES_DW \
  -param START_DATE=2026-04-08 \
  -param END_DATE=2026-04-09 \
  -param AGGREGATION_LEVEL=DAILY \
  <project> SALES_DATA_AGGREGATION
```

### Job Scheduling

Use DataStage Scheduler or external schedulers (Control-M, Autosys, etc.):

```bash
# Example cron entry for daily execution
0 2 * * * /opt/IBM/InformationServer/Server/DSEngine/bin/dsjob -run -wait -param BATCH_DATE=$(date +\%Y-\%m-\%d) PROJECT CUSTOMER_DATA_ETL
```

## 🧪 Testing

### Run All Tests

```bash
cd tests
python test_all_jobs.py
```

### Run Specific Job Tests

```bash
# Test Customer ETL job
python test_customer_etl.py

# Test with custom configuration
python test_customer_etl.py --config ../config/test_config.json
```

### Test Output

Tests generate:
- Console output with real-time results
- Text report: `test_results_<job>_<timestamp>.txt`
- JSON report: `test_results_<job>_<timestamp>.json`

### Example Test Report

```
================================================================================
DataStage Job Test Report
================================================================================
Generated: 2026-04-09T22:00:00

Summary:
--------
Total Tests: 7
Passed: 7
Failed: 0
Errors: 0
Success Rate: 100.00%

Test Results:
-------------
Test: Customer ETL - Job Execution
Job: CUSTOMER_DATA_ETL
Status: PASSED
Execution Time: 10.50s
Message: Job completed with status: FINISHED
================================================================================
```

## ⚙️ Configuration

### Connection Configuration (`config/connections.json`)

```json
{
  "CUSTOMER_SOURCE_DB": {
    "type": "ODBC",
    "server": "source-db-server",
    "database": "customers",
    "username": "etl_user",
    "port": 5432
  },
  "CUSTOMER_DW": {
    "type": "ODBC",
    "server": "dw-server",
    "database": "warehouse",
    "username": "dw_user",
    "port": 5432
  }
}
```

### Job Parameters (`config/parameters.json`)

```json
{
  "CUSTOMER_DATA_ETL": {
    "COMMIT_INTERVAL": 1000,
    "BATCH_DATE": "CurrentDate()",
    "SOURCE_DB_CONN": "CUSTOMER_SOURCE_DB",
    "TARGET_DB_CONN": "CUSTOMER_DW"
  }
}
```

## 📚 Best Practices

### Job Design
- Use parameterized connections for flexibility
- Implement proper error handling
- Add audit columns (ETL_INSERT_DATE, ETL_UPDATE_DATE)
- Use reject links for invalid data
- Optimize commit intervals for performance

### Data Quality
- Validate data at source
- Implement comprehensive quality checks
- Generate quality metrics and reports
- Maintain data lineage
- Document business rules

### Performance
- Use parallel processing where applicable
- Optimize SQL queries
- Implement incremental loading
- Monitor job execution times
- Use appropriate commit intervals

### Testing
- Test with production-like data volumes
- Validate all transformation logic
- Test error scenarios
- Perform regression testing
- Automate test execution

### Documentation
- Document job purpose and logic
- Maintain parameter descriptions
- Document data transformations
- Keep test cases updated
- Version control all artifacts

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-job`)
3. Commit your changes (`git commit -am 'Add new job example'`)
4. Push to the branch (`git push origin feature/new-job`)
5. Create a Pull Request

### Contribution Guidelines
- Follow existing code structure
- Include comprehensive tests
- Update documentation
- Add sample data if applicable
- Follow DataStage naming conventions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Contact the maintainers
- Check the documentation in the `docs/` folder

## 🙏 Acknowledgments

- IBM DataStage documentation and best practices
- Community contributions and feedback
- ETL design patterns and methodologies

## 📊 Project Status

- ✅ 5 production-ready job examples
- ✅ Comprehensive test suite
- ✅ Complete documentation
- ✅ Sample data and configurations
- 🔄 Continuous improvements and updates

---

**Last Updated**: April 9, 2026  
**Version**: 1.0.0  
**Maintainers**: DataStage Examples Team