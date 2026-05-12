# Getting Started with DataStage Pipeline Examples

This guide will help you get up and running with the DataStage pipeline examples in this repository.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [First Job Execution](#first-job-execution)
- [Understanding the Repository](#understanding-the-repository)
- [Next Steps](#next-steps)

## Prerequisites

Before you begin, ensure you have the following:

### Software Requirements

- **IBM InfoSphere DataStage** 11.7 or higher
- **Python** 3.8 or higher (for test suite)
- **Database Access**: Appropriate permissions for source and target systems
- **Git**: For cloning the repository

### Knowledge Requirements

- Basic understanding of ETL concepts
- Familiarity with DataStage Designer and Director
- SQL knowledge for database operations
- Basic Python knowledge (for running tests)

### System Access

- DataStage server access with appropriate credentials
- Database connection credentials for:
  - Source databases
  - Target data warehouse
  - Control/metadata databases

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/datastage-pipeline-examples.git
cd datastage-pipeline-examples
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure DataStage Environment

Set the DataStage home directory environment variable:

```bash
# Linux/Mac
export DSHOME=/opt/IBM/InformationServer/Server/DSEngine

# Windows
set DSHOME=C:\IBM\InformationServer\Server\DSEngine
```

### Step 4: Configure Database Connections

Edit [`config/connections.json`](../config/connections.json) with your database connection details:

```json
{
  "CUSTOMER_SOURCE_DB": {
    "type": "ODBC",
    "server": "your-source-server",
    "database": "customers",
    "username": "etl_user",
    "port": 5432
  },
  "CUSTOMER_DW": {
    "type": "ODBC",
    "server": "your-dw-server",
    "database": "warehouse",
    "username": "dw_user",
    "port": 5432
  }
}
```

### Step 5: Import DataStage Jobs

Import the job definitions into your DataStage project:

```bash
# Set your DataStage credentials
DS_SERVER="your-datastage-server"
DS_USER="your-username"
DS_PROJECT="your-project"

# Import all jobs
for job in jobs/*.dsx; do
  dsjob -import -server $DS_SERVER -user $DS_USER -project $DS_PROJECT "$job"
done
```

Or import individual jobs:

```bash
dsjob -import -server $DS_SERVER -user $DS_USER -project $DS_PROJECT jobs/customer_data_etl.dsx
```

## Quick Start

### Verify Installation

Run the test framework to verify everything is set up correctly:

```bash
cd tests
python test_framework.py
```

### Load Sample Data

Load the sample data files into your source databases:

```bash
# Example using psql for PostgreSQL
psql -h your-source-server -U etl_user -d customers -f data/sample_customers.csv
```

### Run Your First Job

#### Using DataStage Director

1. Open **DataStage Director**
2. Connect to your project
3. Select **CUSTOMER_DATA_ETL** job
4. Right-click and select **Run**
5. Set the following parameters:
   - `SOURCE_DB_CONN`: CUSTOMER_SOURCE_DB
   - `TARGET_DB_CONN`: CUSTOMER_DW
   - `BATCH_DATE`: 2026-04-16
   - `COMMIT_INTERVAL`: 1000
6. Click **Run**
7. Monitor the job execution in the log

#### Using Command Line

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

### Check Job Status

```bash
dsjob -jobinfo -server your-server -user your-username YOUR_PROJECT CUSTOMER_DATA_ETL
```

## First Job Execution

Let's walk through executing the Customer Data ETL job step by step:

### 1. Prepare Source Data

Ensure your source database has customer data:

```sql
SELECT COUNT(*) FROM CUSTOMERS;
SELECT * FROM CUSTOMERS LIMIT 5;
```

### 2. Verify Target Schema

Ensure the target table exists:

```sql
CREATE TABLE IF NOT EXISTS DW_CUSTOMERS (
  CUSTOMER_ID INTEGER PRIMARY KEY,
  FULL_NAME VARCHAR(100),
  EMAIL VARCHAR(100),
  PHONE VARCHAR(20),
  AGE INTEGER,
  CUSTOMER_SEGMENT VARCHAR(20),
  IS_ACTIVE INTEGER,
  ETL_TIMESTAMP TIMESTAMP
);
```

### 3. Run the Job

Execute the job using one of the methods above.

### 4. Validate Results

Check the target table:

```sql
SELECT COUNT(*) FROM DW_CUSTOMERS;
SELECT * FROM DW_CUSTOMERS LIMIT 5;
```

Check reject file (if any):

```bash
cat /data/rejects/customer_rejects_2026-04-16.csv
```

### 5. Run Tests

Validate the job execution with automated tests:

```bash
cd tests
python test_customer_etl.py
```

## Understanding the Repository

### Directory Structure

```
datastage-pipeline-examples/
├── jobs/           # DataStage job definitions (.dsx files)
├── tests/          # Python test suite
├── data/           # Sample data files
├── config/         # Configuration files
├── docs/           # Documentation (you are here!)
└── README.md       # Main repository documentation
```

### Available Jobs

1. **[`customer_data_etl.dsx`](../jobs/customer_data_etl.dsx)** - Customer data ETL pipeline
2. **[`sales_data_aggregation.dsx`](../jobs/sales_data_aggregation.dsx)** - Sales aggregation
3. **[`data_quality_validation.dsx`](../jobs/data_quality_validation.dsx)** - Data quality checks
4. **[`incremental_load.dsx`](../jobs/incremental_load.dsx)** - CDC-based incremental loading
5. **[`master_data_management.dsx`](../jobs/master_data_management.dsx)** - MDM consolidation

### Key Configuration Files

- **[`config/connections.json`](../config/connections.json)** - Database connection definitions
- **[`config/parameters.json`](../config/parameters.json)** - Default job parameters
- **[`config/test_config.json`](../config/test_config.json)** - Test configuration

## Next Steps

Now that you have the basics set up, explore these resources:

### Documentation

- **[Job Documentation](JOB_DOCUMENTATION.md)** - Detailed documentation for each job
- **[Testing Guide](TESTING_GUIDE.md)** - How to run and write tests
- **[Configuration Guide](CONFIGURATION_GUIDE.md)** - Advanced configuration options
- **[Best Practices](BEST_PRACTICES.md)** - DataStage development best practices
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions

### Tutorials

1. **Customize a Job** - Modify the Customer ETL job for your needs
2. **Create a New Job** - Build a new pipeline using the examples as templates
3. **Set Up Scheduling** - Automate job execution with schedulers
4. **Performance Tuning** - Optimize job performance for large datasets

### Advanced Topics

- **[Architecture Overview](ARCHITECTURE.md)** - System architecture and design patterns
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy to production environments
- **[API Integration](API_INTEGRATION.md)** - Integrate with external systems

## Getting Help

If you encounter issues:

1. Check the **[Troubleshooting Guide](TROUBLESHOOTING.md)**
2. Review the **[FAQ](FAQ.md)**
3. Search existing issues in the repository
4. Create a new issue with detailed information

## Contributing

We welcome contributions! See the main [README.md](../README.md#contributing) for contribution guidelines.

---

**Next**: [Job Documentation](JOB_DOCUMENTATION.md) | [Testing Guide](TESTING_GUIDE.md)