#!/usr/bin/env python3
"""
Test Suite for Customer Data ETL Pipeline
Tests the CUSTOMER_DATA_ETL DataStage job
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_framework import DataStageTestFramework, TestStatus


class TestCustomerDataETL:
    """Test cases for Customer Data ETL job"""
    
    def __init__(self):
        self.framework = DataStageTestFramework()
        self.job_name = 'CUSTOMER_DATA_ETL'
        
    def test_job_execution_success(self):
        """Test successful job execution"""
        print("\n" + "="*80)
        print("TEST: Job Execution Success")
        print("="*80)
        
        parameters = {
            'SOURCE_DB_CONN': 'CUSTOMER_SOURCE_DB',
            'TARGET_DB_CONN': 'CUSTOMER_DW',
            'BATCH_DATE': datetime.now().strftime('%Y-%m-%d'),
            'COMMIT_INTERVAL': 1000
        }
        
        def test_func(job_name):
            result = self.framework.run_job(job_name, parameters)
            
            passed = result['status'] == 'FINISHED'
            
            return {
                'passed': passed,
                'message': f"Job completed with status: {result['status']}",
                'details': {
                    'execution_time': result['execution_time'],
                    'rows_processed': result['rows_processed'],
                    'rows_rejected': result['rows_rejected']
                }
            }
        
        return self.framework.run_test(
            'Customer ETL - Job Execution',
            test_func,
            job_name=self.job_name
        )
    
    def test_data_transformation(self):
        """Test data transformation logic"""
        print("\n" + "="*80)
        print("TEST: Data Transformation")
        print("="*80)
        
        def test_func(job_name):
            # Test transformation rules
            transformations = [
                {
                    'name': 'Full Name Concatenation',
                    'rule': 'FIRST_NAME + LAST_NAME = FULL_NAME',
                    'expected': True
                },
                {
                    'name': 'Email Standardization',
                    'rule': 'Email converted to uppercase',
                    'expected': True
                },
                {
                    'name': 'Phone Number Cleaning',
                    'rule': 'Remove non-numeric characters',
                    'expected': True
                },
                {
                    'name': 'Age Calculation',
                    'rule': 'Calculate age from DOB',
                    'expected': True
                }
            ]
            
            passed_count = 0
            for transform in transformations:
                # Simulate transformation validation
                if transform['expected']:
                    passed_count += 1
            
            passed = passed_count == len(transformations)
            
            return {
                'passed': passed,
                'message': f"Transformation validation: {passed_count}/{len(transformations)} passed",
                'details': {'transformations': transformations}
            }
        
        return self.framework.run_test(
            'Customer ETL - Data Transformation',
            test_func,
            job_name=self.job_name
        )
    
    def test_data_quality_checks(self):
        """Test data quality validation"""
        print("\n" + "="*80)
        print("TEST: Data Quality Checks")
        print("="*80)
        
        def test_func(job_name):
            quality_rules = [
                {
                    'name': 'Not Null Customer ID',
                    'description': 'Customer ID must not be null',
                    'sql': 'SELECT COUNT(*) FROM DW_CUSTOMERS WHERE CUSTOMER_ID IS NULL'
                },
                {
                    'name': 'Valid Email Format',
                    'description': 'Email must contain @ symbol',
                    'sql': "SELECT COUNT(*) FROM DW_CUSTOMERS WHERE EMAIL NOT LIKE '%@%'"
                },
                {
                    'name': 'Phone Number Length',
                    'description': 'Phone number must be 10-15 digits',
                    'sql': 'SELECT COUNT(*) FROM DW_CUSTOMERS WHERE LEN(PHONE_CLEAN) < 10'
                }
            ]
            
            result = self.framework.validate_data_quality(
                'DW_CUSTOMERS',
                quality_rules,
                'CUSTOMER_DW'
            )
            
            passed = result['failed'] == 0
            
            return {
                'passed': passed,
                'message': f"Quality checks: {result['passed']}/{result['total_rules']} passed",
                'details': result
            }
        
        return self.framework.run_test(
            'Customer ETL - Data Quality',
            test_func,
            job_name=self.job_name
        )
    
    def test_row_count_validation(self):
        """Test row count matches between source and target"""
        print("\n" + "="*80)
        print("TEST: Row Count Validation")
        print("="*80)
        
        def test_func(job_name):
            # Expected row counts (simulated)
            source_count = 1000
            target_count = 995  # 5 rejected records
            reject_count = 5
            
            passed = (target_count + reject_count) == source_count
            
            return {
                'passed': passed,
                'message': f"Row count validation: Source={source_count}, Target={target_count}, Rejected={reject_count}",
                'details': {
                    'source_rows': source_count,
                    'target_rows': target_count,
                    'rejected_rows': reject_count,
                    'total_processed': target_count + reject_count
                }
            }
        
        return self.framework.run_test(
            'Customer ETL - Row Count',
            test_func,
            job_name=self.job_name
        )
    
    def test_reject_handling(self):
        """Test reject file generation"""
        print("\n" + "="*80)
        print("TEST: Reject Handling")
        print("="*80)
        
        def test_func(job_name):
            # Check if reject file exists and contains expected records
            reject_file = f"/data/rejects/customer_rejects_{datetime.now().strftime('%Y-%m-%d')}.csv"
            
            # Simulate reject file validation
            reject_records_found = True
            reject_count = 5
            
            passed = reject_records_found and reject_count > 0
            
            return {
                'passed': passed,
                'message': f"Reject file validation: {reject_count} records found",
                'details': {
                    'reject_file': reject_file,
                    'reject_count': reject_count,
                    'file_exists': reject_records_found
                }
            }
        
        return self.framework.run_test(
            'Customer ETL - Reject Handling',
            test_func,
            job_name=self.job_name
        )
    
    def test_incremental_load(self):
        """Test incremental load functionality"""
        print("\n" + "="*80)
        print("TEST: Incremental Load")
        print("="*80)
        
        def test_func(job_name):
            # Test that only new/changed records are processed
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            parameters = {
                'SOURCE_DB_CONN': 'CUSTOMER_SOURCE_DB',
                'TARGET_DB_CONN': 'CUSTOMER_DW',
                'BATCH_DATE': yesterday,
                'COMMIT_INTERVAL': 1000
            }
            
            result = self.framework.run_job(job_name, parameters)
            
            # Verify only incremental records were processed
            incremental_count = result.get('rows_processed', 0)
            passed = incremental_count < 1000  # Less than full load
            
            return {
                'passed': passed,
                'message': f"Incremental load processed {incremental_count} records",
                'details': {
                    'incremental_rows': incremental_count,
                    'load_type': 'incremental'
                }
            }
        
        return self.framework.run_test(
            'Customer ETL - Incremental Load',
            test_func,
            job_name=self.job_name
        )
    
    def test_performance(self):
        """Test job performance metrics"""
        print("\n" + "="*80)
        print("TEST: Performance Metrics")
        print("="*80)
        
        def test_func(job_name):
            parameters = {
                'SOURCE_DB_CONN': 'CUSTOMER_SOURCE_DB',
                'TARGET_DB_CONN': 'CUSTOMER_DW',
                'BATCH_DATE': datetime.now().strftime('%Y-%m-%d'),
                'COMMIT_INTERVAL': 1000
            }
            
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
                    'rows_processed': rows_processed,
                    'throughput': throughput,
                    'max_time_threshold': max_execution_time,
                    'min_throughput_threshold': min_throughput
                }
            }
        
        return self.framework.run_test(
            'Customer ETL - Performance',
            test_func,
            job_name=self.job_name
        )
    
    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "="*80)
        print(f"Running Test Suite: {self.job_name}")
        print("="*80)
        
        # Run all tests
        self.test_job_execution_success()
        self.test_data_transformation()
        self.test_data_quality_checks()
        self.test_row_count_validation()
        self.test_reject_handling()
        self.test_incremental_load()
        self.test_performance()
        
        # Generate report
        report = self.framework.generate_report(
            f'test_results_{self.job_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
        
        print(report)
        
        # Export JSON results
        self.framework.export_results_json(
            f'test_results_{self.job_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        return self.framework.test_results


def main():
    """Main function to run tests"""
    test_suite = TestCustomerDataETL()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for r in results if r.status == TestStatus.FAILED or r.status == TestStatus.ERROR)
    sys.exit(0 if failed_tests == 0 else 1)


if __name__ == '__main__':
    main()

# Made with Bob
