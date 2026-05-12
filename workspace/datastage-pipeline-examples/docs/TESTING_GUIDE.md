# Testing Guide

Comprehensive guide for testing DataStage pipeline jobs using the included test framework.

## Table of Contents

- [Overview](#overview)
- [Test Framework](#test-framework)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Categories](#test-categories)
- [Test Reports](#test-reports)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

This repository includes a comprehensive Python-based test framework for validating DataStage jobs. The framework provides:

- Automated job execution and validation
- Data quality checks
- Performance testing
- Integration testing
- Detailed reporting

### Test Framework Architecture

```
tests/
├── test_framework.py       # Core testing framework
├── test_customer_etl.py    # Customer ETL tests
├── test_all_jobs.py        # Comprehensive test suite
└── test_results/           # Test output directory
```

## Test Framework

### Core Components

The test framework ([`test_framework.py`](../tests/test_framework.py)) provides:

#### DataStageTestFramework Class

Main class for test execution:

```python
from tests.test_framework import DataStageTestFramework

framework = DataStageTestFramework(config_file='config/test_config.json')
```

#### Key Methods

| Method | Description |
|--------|-------------|
| `run_job()` | Execute a DataStage job |
| `validate_row_count()` | Validate row counts |
| `validate_data_quality()` | Run data quality checks |
| `compare_datasets()` | Compare source and target data |
| `check_job_dependencies()` | Verify job prerequisites |
| `run_test()` | Execute a single test |
| `generate_report()` | Generate test report |
| `export_results_json()` | Export results as JSON |

### Configuration

Create a test configuration file ([`config/test_config.json`](../config/test_config.json)):

```json
{
  "project": "TEST_PROJECT",
  "server": "localhost",
  "username": "dsadm",
  "timeout": 300,
  "database_connections": {
    "source": "postgresql://localhost:5432/source_db",
    "target": "postgresql://localhost:5432/target_db"
  }
}
```

## Running Tests

### Prerequisites

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
```bash
export DSHOME=/opt/IBM/InformationServer/Server/DSEngine
export DS_PROJECT=YOUR_PROJECT
export DS_SERVER=your-server
export DS_USER=your-username
```

### Run All Tests

Execute the comprehensive test suite:

```bash
cd tests
python test_all_jobs.py
```

### Run Specific Job Tests

Test individual jobs:

```bash
# Test Customer ETL job
python test_customer_etl.py

# Test with custom configuration
python test_customer_etl.py --config ../config/test_config.json

# Test with verbose output
python test_customer_etl.py --verbose
```

### Run Individual Test Cases

Execute specific test functions:

```python
from tests.test_customer_etl import TestCustomerDataETL

test_suite = TestCustomerDataETL()
test_suite.test_job_execution_success()
test_suite.test_data_transformation()
```

### Command Line Options

```bash
python test_customer_etl.py [OPTIONS]

Options:
  --config PATH       Path to configuration file
  --verbose          Enable verbose output
  --output PATH      Output directory for reports
  --parallel         Run tests in parallel
  --fail-fast        Stop on first failure
```

## Writing Tests

### Test Structure

Create a test class for your job:

```python
#!/usr/bin/env python3
"""
Test Suite for My Custom Job
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_framework import DataStageTestFramework, TestStatus


class TestMyCustomJob:
    """Test cases for My Custom Job"""
    
    def __init__(self):
        self.framework = DataStageTestFramework()
        self.job_name = 'MY_CUSTOM_JOB'
    
    def test_job_execution(self):
        """Test successful job execution"""
        print("\n" + "="*80)
        print("TEST: Job Execution")
        print("="*80)
        
        def test_func(job_name):
            parameters = {
                'PARAM1': 'value1',
                'PARAM2': 'value2'
            }
            
            result = self.framework.run_job(job_name, parameters)
            
            passed = result['status'] == 'FINISHED'
            
            return {
                'passed': passed,
                'message': f"Job completed with status: {result['status']}",
                'details': result
            }
        
        return self.framework.run_test(
            'My Custom Job - Execution',
            test_func,
            job_name=self.job_name
        )
    
    def run_all_tests(self):
        """Run all test cases"""
        self.test_job_execution()
        # Add more tests...
        
        # Generate report
        report = self.framework.generate_report(
            f'test_results_{self.job_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
        print(report)
        
        return self.framework.test_results


def main():
    """Main function to run tests"""
    test_suite = TestMyCustomJob()
    results = test_suite.run_all_tests()
    
    failed_tests = sum(1 for r in results if r.status == TestStatus.FAILED or r.status == TestStatus.ERROR)
    sys.exit(0 if failed_tests == 0 else 1)


if __name__ == '__main__':
    main()
```

### Test Function Pattern

Each test function should follow this pattern:

```python
def test_something(self):
    """Test description"""
    print("\n" + "="*80)
    print("TEST: Test Name")
    print("="*80)
    
    def test_func(job_name):
        # Test logic here
        
        # Determine if test passed
        passed = True  # or False based on validation
        
        return {
            'passed': passed,
            'message': 'Test result message',
            'details': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
    
    return self.framework.run_test(
        'Test Name',
        test_func,
        job_name=self.job_name
    )
```

## Test Categories

### 1. Functional Tests

Validate job functionality and business logic:

```python
def test_data_transformation(self):
    """Test data transformation logic"""
    def test_func(job_name):
        # Run job
        result = self.framework.run_job(job_name, parameters)
        
        # Validate transformations
        transformations = [
            {'name': 'Name Concatenation', 'expected': True},
            {'name': 'Email Validation', 'expected': True},
            {'name': 'Age Calculation', 'expected': True}
        ]
        
        passed = all(t['expected'] for t in transformations)
        
        return {
            'passed': passed,
            'message': f"Transformations validated",
            'details': {'transformations': transformations}
        }
    
    return self.framework.run_test(
        'Data Transformation Test',
        test_func,
        job_name=self.job_name
    )
```

### 2. Data Quality Tests

Validate data quality and integrity:

```python
def test_data_quality(self):
    """Test data quality checks"""
    def test_func(job_name):
        quality_rules = [
            {
                'name': 'Not Null Check',
                'description': 'Primary key must not be null',
                'sql': 'SELECT COUNT(*) FROM table WHERE id IS NULL'
            },
            {
                'name': 'Format Validation',
                'description': 'Email must be valid format',
                'sql': "SELECT COUNT(*) FROM table WHERE email NOT LIKE '%@%'"
            }
        ]
        
        result = self.framework.validate_data_quality(
            'target_table',
            quality_rules,
            'TARGET_DB_CONN'
        )
        
        passed = result['failed'] == 0
        
        return {
            'passed': passed,
            'message': f"Quality: {result['passed']}/{result['total_rules']} passed",
            'details': result
        }
    
    return self.framework.run_test(
        'Data Quality Test',
        test_func,
        job_name=self.job_name
    )
```

### 3. Performance Tests

Validate job performance metrics:

```python
def test_performance(self):
    """Test job performance"""
    def test_func(job_name):
        result = self.framework.run_job(job_name, parameters)
        
        # Performance thresholds
        max_execution_time = 300  # 5 minutes
        min_throughput = 100  # rows per second
        
        execution_time = result['execution_time']
        rows_processed = result['rows_processed']
        throughput = rows_processed / execution_time if execution_time > 0 else 0
        
        passed = execution_time < max_execution_time and throughput >= min_throughput
        
        return {
            'passed': passed,
            'message': f"Performance: {execution_time:.2f}s, {throughput:.2f} rows/sec",
            'details': {
                'execution_time': execution_time,
                'throughput': throughput,
                'thresholds': {
                    'max_time': max_execution_time,
                    'min_throughput': min_throughput
                }
            }
        }
    
    return self.framework.run_test(
        'Performance Test',
        test_func,
        job_name=self.job_name
    )
```

### 4. Integration Tests

Test end-to-end workflows:

```python
def test_end_to_end_workflow(self):
    """Test complete workflow"""
    def test_func(job_name):
        workflow_steps = [
            ('JOB1', 'Extract data'),
            ('JOB2', 'Transform data'),
            ('JOB3', 'Load data')
        ]
        
        all_passed = True
        step_results = []
        
        for step_job, description in workflow_steps:
            result = self.framework.run_job(step_job, {})
            step_passed = result['status'] == 'FINISHED'
            
            step_results.append({
                'job': step_job,
                'description': description,
                'status': result['status'],
                'passed': step_passed
            })
            
            if not step_passed:
                all_passed = False
                break
        
        return {
            'passed': all_passed,
            'message': f"Workflow: {'Success' if all_passed else 'Failed'}",
            'details': {'steps': step_results}
        }
    
    return self.framework.run_test(
        'End-to-End Workflow Test',
        test_func,
        job_name='WORKFLOW'
    )
```

### 5. Error Handling Tests

Test error scenarios:

```python
def test_error_handling(self):
    """Test error handling"""
    def test_func(job_name):
        error_scenarios = [
            {
                'scenario': 'Invalid connection',
                'parameters': {'SOURCE_DB_CONN': 'INVALID'},
                'expected_behavior': 'Job fails gracefully'
            },
            {
                'scenario': 'Missing parameter',
                'parameters': {},
                'expected_behavior': 'Validation error'
            }
        ]
        
        all_handled = True
        
        for scenario in error_scenarios:
            try:
                result = self.framework.run_job(job_name, scenario['parameters'])
                # Verify error was handled properly
                scenario['handled'] = result['status'] == 'ERROR'
            except Exception as e:
                scenario['handled'] = True
                scenario['error'] = str(e)
            
            if not scenario['handled']:
                all_handled = False
        
        return {
            'passed': all_handled,
            'message': f"Error handling validated",
            'details': {'scenarios': error_scenarios}
        }
    
    return self.framework.run_test(
        'Error Handling Test',
        test_func,
        job_name=self.job_name
    )
```

## Test Reports

### Text Reports

Generated automatically after test execution:

```
================================================================================
DataStage Job Test Report
================================================================================
Generated: 2026-04-16T12:00:00

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

### JSON Reports

Structured output for integration with CI/CD:

```json
{
  "timestamp": "2026-04-16T12:00:00",
  "total_tests": 7,
  "results": [
    {
      "test_name": "Customer ETL - Job Execution",
      "job_name": "CUSTOMER_DATA_ETL",
      "status": "PASSED",
      "execution_time": 10.5,
      "message": "Job completed with status: FINISHED",
      "details": {
        "rows_processed": 1000,
        "rows_rejected": 5
      },
      "timestamp": "2026-04-16T12:00:00"
    }
  ]
}
```

### Accessing Reports

Reports are saved to:
- Text: `test_results_<job>_<timestamp>.txt`
- JSON: `test_results_<job>_<timestamp>.json`

## Best Practices

### 1. Test Organization

- Group related tests in test classes
- Use descriptive test names
- Keep tests independent
- Clean up test data after execution

### 2. Test Data

- Use dedicated test databases
- Create realistic test datasets
- Include edge cases and boundary conditions
- Test with production-like volumes

### 3. Assertions

- Validate all critical outputs
- Check row counts
- Verify data transformations
- Validate business rules

### 4. Error Handling

- Test both success and failure scenarios
- Verify error messages
- Check reject file generation
- Validate rollback behavior

### 5. Performance Testing

- Set realistic performance thresholds
- Test with various data volumes
- Monitor resource utilization
- Document performance baselines

### 6. Continuous Integration

Integrate tests with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: DataStage Tests

on: [push, pull_request]

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
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          cd tests
          python test_all_jobs.py
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: tests/test_results_*.json
```

## Troubleshooting

### Common Issues

#### 1. Connection Failures

**Problem**: Cannot connect to DataStage server

**Solution**:
```bash
# Verify DSHOME is set
echo $DSHOME

# Check dsjob command availability
which dsjob

# Test connection
dsjob -lprojects -server your-server -user your-username
```

#### 2. Import Errors

**Problem**: Cannot import test framework

**Solution**:
```python
# Add parent directory to path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### 3. Database Connection Issues

**Problem**: Cannot connect to test databases

**Solution**:
- Verify connection strings in [`config/test_config.json`](../config/test_config.json)
- Check database credentials
- Ensure network connectivity
- Verify firewall rules

#### 4. Test Timeouts

**Problem**: Tests timing out

**Solution**:
```python
# Increase timeout in configuration
{
  "timeout": 600  # 10 minutes
}
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

framework = DataStageTestFramework()
```

### Verbose Output

Run tests with verbose output:

```bash
python test_customer_etl.py --verbose
```

## Advanced Testing

### Parallel Test Execution

Run tests in parallel for faster execution:

```python
from concurrent.futures import ThreadPoolExecutor

def run_tests_parallel(test_suite):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(test_suite.test_job_execution),
            executor.submit(test_suite.test_data_quality),
            executor.submit(test_suite.test_performance)
        ]
        results = [f.result() for f in futures]
    return results
```

### Data-Driven Testing

Use parameterized tests:

```python
import pytest

@pytest.mark.parametrize("batch_date,expected_rows", [
    ("2026-04-15", 1000),
    ("2026-04-16", 1500),
    ("2026-04-17", 2000)
])
def test_batch_processing(batch_date, expected_rows):
    parameters = {'BATCH_DATE': batch_date}
    result = framework.run_job('CUSTOMER_DATA_ETL', parameters)
    assert result['rows_processed'] == expected_rows
```

### Mock Testing

Mock external dependencies:

```python
from unittest.mock import Mock, patch

def test_with_mock():
    with patch('test_framework.DataStageTestFramework.run_job') as mock_run:
        mock_run.return_value = {
            'status': 'FINISHED',
            'rows_processed': 1000
        }
        
        # Run test with mocked job execution
        result = test_func('CUSTOMER_DATA_ETL')
        assert result['passed'] == True
```

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)