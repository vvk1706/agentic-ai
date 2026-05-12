# Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues with DataStage pipeline jobs.

## Table of Contents

- [Common Issues](#common-issues)
- [Job Execution Problems](#job-execution-problems)
- [Connection Issues](#connection-issues)
- [Performance Problems](#performance-problems)
- [Data Quality Issues](#data-quality-issues)
- [Test Framework Issues](#test-framework-issues)
- [Debugging Techniques](#debugging-techniques)
- [Log Analysis](#log-analysis)
- [Getting Help](#getting-help)

## Common Issues

### Quick Diagnosis Checklist

When encountering issues, check these first:

```bash
# 1. Check DataStage environment
echo $DSHOME
which dsjob

# 2. Check job status
dsjob -jobinfo -server your-server -user your-username PROJECT JOB_NAME

# 3. Check recent logs
tail -100 $DSHOME/Logs/JOB_NAME.log

# 4. Check database connectivity
psql -h db-server -U username -d database -c "SELECT 1"

# 5. Check disk space
df -h

# 6. Check memory
free -h

# 7. Check running processes
ps aux | grep dsrpcd
```

## Job Execution Problems

### Issue: Job Won't Start

**Symptoms**:
- Job status shows "Not Running"
- No log entries created
- Error: "Failed to start job"

**Possible Causes & Solutions**:

#### 1. DataStage Engine Not Running

```bash
# Check if engine is running
ps aux | grep dsrpcd

# Start DataStage engine
cd $DSHOME
./bin/uv -admin -start

# Verify
./bin/uv -admin -status
```

#### 2. Project Not Available

```bash
# List available projects
dsjob -lprojects -server your-server -user your-username

# If project missing, restore from backup
dsjob -import -server your-server -user your-username \
  -project PROJECT backup/project_backup.dsx
```

#### 3. Insufficient Permissions

```bash
# Check file permissions
ls -la $DSHOME/Projects/PROJECT

# Fix permissions
chmod 755 $DSHOME/Projects/PROJECT
chown dsadm:dstage $DSHOME/Projects/PROJECT/*
```

#### 4. License Issues

```bash
# Check license status
cd $DSHOME
./bin/LicenseManager -status

# If expired, contact IBM support
```

### Issue: Job Fails Immediately

**Symptoms**:
- Job starts but fails within seconds
- Status: "Aborted" or "Failed"
- Minimal rows processed

**Possible Causes & Solutions**:

#### 1. Missing Parameters

```bash
# Check required parameters
dsjob -paraminfo -server your-server -user your-username \
  PROJECT JOB_NAME

# Run with all required parameters
dsjob -run -wait \
  -param SOURCE_DB_CONN=CUSTOMER_SOURCE_DB \
  -param TARGET_DB_CONN=CUSTOMER_DW \
  -param BATCH_DATE=2026-04-16 \
  -server your-server -user your-username \
  PROJECT JOB_NAME
```

#### 2. Invalid Parameter Values

```bash
# Check parameter validation
# Review job log for parameter errors
grep "Parameter" $DSHOME/Logs/JOB_NAME.log

# Common issues:
# - Date format mismatch
# - Invalid connection name
# - Out of range numeric values
```

#### 3. Compilation Errors

```bash
# Recompile job
dsjob -compile -server your-server -user your-username \
  PROJECT JOB_NAME

# Check compilation log
cat $DSHOME/Projects/PROJECT/RT_LOG*/JOB_NAME.log
```

### Issue: Job Hangs or Runs Forever

**Symptoms**:
- Job status: "Running"
- No progress for extended period
- High CPU or memory usage

**Possible Causes & Solutions**:

#### 1. Database Lock or Deadlock

```sql
-- PostgreSQL: Check for locks
SELECT 
  pid, usename, application_name, state, query
FROM pg_stat_activity
WHERE state = 'active' AND query NOT LIKE '%pg_stat_activity%';

-- Kill blocking query
SELECT pg_terminate_backend(pid);

-- Oracle: Check for locks
SELECT 
  s.sid, s.serial#, s.username, s.program, l.type, l.lmode
FROM v$session s, v$lock l
WHERE s.sid = l.sid;

-- Kill session
ALTER SYSTEM KILL SESSION 'sid,serial#';
```

#### 2. Infinite Loop in Transformer

```datastage
# Check for infinite loops in derivations
# Look for recursive references or circular dependencies

# Example problematic code:
COLUMN_A = If COLUMN_B > 0 Then COLUMN_A + 1 Else 0
# COLUMN_A references itself!

# Fix:
COLUMN_A = If COLUMN_B > 0 Then INPUT.COLUMN_A + 1 Else 0
```

#### 3. Large Dataset Without Commit

```datastage
# Ensure commit interval is set
<Parameter Name="COMMIT_INTERVAL" Value="5000"/>

# Check target stage settings
Target Stage:
  Commit Interval: #COMMIT_INTERVAL#
  Commit on EOF: Yes
```

#### 4. Network Issues

```bash
# Test network connectivity
ping db-server
telnet db-server 5432

# Check network latency
time psql -h db-server -U username -d database -c "SELECT 1"

# If slow, consider:
# - Moving data closer to processing
# - Increasing network bandwidth
# - Using compression
```

### Issue: Job Completes with Warnings

**Symptoms**:
- Job status: "Finished (with warnings)"
- Some rows rejected
- Warning messages in log

**Diagnosis**:

```bash
# Check job log for warnings
grep "WARNING" $DSHOME/Logs/JOB_NAME.log

# Check reject file
cat /data/rejects/customer_rejects_2026-04-16.csv

# Analyze reject reasons
cut -d',' -f1 /data/rejects/customer_rejects_2026-04-16.csv | \
  sort | uniq -c | sort -rn
```

**Common Warnings**:

1. **Data Type Conversion**
   ```
   WARNING: Implicit conversion from source type 'VARCHAR' to result type 'INTEGER'
   ```
   Solution: Add explicit conversion in transformer

2. **Null Value Handling**
   ```
   WARNING: Null value encountered in non-nullable column
   ```
   Solution: Add null handling logic

3. **Truncation**
   ```
   WARNING: String truncated to fit target column length
   ```
   Solution: Increase target column size or trim source data

## Connection Issues

### Issue: Cannot Connect to Database

**Symptoms**:
- Error: "Connection refused"
- Error: "Timeout connecting to database"
- Error: "Authentication failed"

**Diagnosis Steps**:

```bash
# 1. Test basic connectivity
ping db-server
telnet db-server 5432

# 2. Test database connection
psql -h db-server -U username -d database

# 3. Check DataStage connection
dsjob -testconnection -server your-server -user your-username \
  PROJECT CONNECTION_NAME

# 4. Check ODBC configuration
cat /etc/odbc.ini
cat ~/.odbc.ini
```

**Solutions**:

#### 1. Firewall Blocking Connection

```bash
# Check firewall rules
sudo iptables -L -n | grep 5432

# Add rule to allow connection
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT

# Or disable firewall temporarily for testing
sudo systemctl stop firewalld
```

#### 2. Wrong Connection Parameters

```json
{
  "server": "correct-server.example.com",  // Not "localhost"
  "port": 5432,  // Correct port
  "database": "correct_database",  // Exact name
  "username": "correct_user"  // Case-sensitive
}
```

#### 3. SSL/TLS Issues

```json
{
  "options": {
    "sslmode": "require",  // Try "disable" for testing
    "sslcert": "/path/to/client-cert.pem",
    "sslkey": "/path/to/client-key.pem",
    "sslrootcert": "/path/to/ca-cert.pem"
  }
}
```

#### 4. Connection Pool Exhausted

```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check max connections
SHOW max_connections;

-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle' AND state_change < NOW() - INTERVAL '1 hour';
```

### Issue: Connection Drops During Job

**Symptoms**:
- Job fails mid-execution
- Error: "Connection lost"
- Error: "Broken pipe"

**Solutions**:

#### 1. Increase Timeout Settings

```json
{
  "options": {
    "connect_timeout": 60,
    "statement_timeout": 600000,
    "tcp_keepalives_idle": 60,
    "tcp_keepalives_interval": 10,
    "tcp_keepalives_count": 5
  }
}
```

#### 2. Enable Connection Retry

```datastage
# Add retry logic in job sequence
Loop:
  Max Iterations: 3
  Delay: 60 seconds
  
  Try:
    Run Job
  Catch:
    If connection error Then
      Wait and retry
    Else
      Abort
```

## Performance Problems

### Issue: Job Running Slowly

**Symptoms**:
- Execution time much longer than expected
- Low throughput (rows/second)
- High resource utilization

**Diagnosis**:

```bash
# 1. Check job performance metrics
dsjob -jobinfo -server your-server -user your-username \
  PROJECT JOB_NAME | grep "Elapsed time"

# 2. Monitor system resources
top
iostat -x 1
vmstat 1

# 3. Check database performance
# PostgreSQL
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

# 4. Profile job execution
# Enable performance monitoring in DataStage Director
```

**Common Causes & Solutions**:

#### 1. Sequential Processing

```datastage
# Problem: No partitioning
Partitioning: None

# Solution: Enable partitioning
Partitioning:
  Method: Hash
  Key: CUSTOMER_ID
  Nodes: 8
```

#### 2. Inefficient SQL

```sql
-- Problem: Full table scan
SELECT * FROM large_table WHERE UPPER(name) = 'JOHN';

-- Solution: Use index and avoid functions
CREATE INDEX idx_name ON large_table(name);
SELECT * FROM large_table WHERE name = 'JOHN';
```

#### 3. Small Commit Interval

```datastage
# Problem: Too frequent commits
COMMIT_INTERVAL = 100

# Solution: Increase commit interval
COMMIT_INTERVAL = 5000
```

#### 4. Excessive Lookups

```datastage
# Problem: Lookup on large table for each row
Lookup Stage:
  Table: large_reference_table (10M rows)
  Cache: No

# Solution: Cache lookup or use database join
Lookup Stage:
  Cache: Yes
  Cache Size: 100000
  
# Or use SQL JOIN in source query instead
```

#### 5. Sorting Large Datasets

```datastage
# Problem: Sorting unsorted data
Sort Stage:
  Input Sorted: No
  Sort Keys: CUSTOMER_ID, ORDER_DATE

# Solution: Sort in database
Source Query:
  SELECT * FROM orders ORDER BY customer_id, order_date
  
Sort Stage:
  Input Sorted: Yes
  Perform Sort: No
```

### Issue: High Memory Usage

**Symptoms**:
- Job fails with "Out of memory" error
- System becomes unresponsive
- Swap usage increases

**Solutions**:

#### 1. Reduce Buffer Sizes

```datastage
# Reduce buffer settings
Buffer Size: 5000  # Instead of 10000
Max Memory: 1024 MB  # Instead of 2048 MB
```

#### 2. Enable Disk-Based Operations

```datastage
# Use disk for sorting large datasets
Sort Stage:
  Sort Mode: Disk
  Scratch Disk: /tmp/datastage_sort
```

#### 3. Process in Batches

```sql
-- Instead of processing all data at once
SELECT * FROM large_table;

-- Process in batches
SELECT * FROM large_table 
WHERE id BETWEEN 1 AND 100000;

SELECT * FROM large_table 
WHERE id BETWEEN 100001 AND 200000;
```

## Data Quality Issues

### Issue: Unexpected Reject Counts

**Symptoms**:
- High number of rejected records
- Reject percentage above threshold
- Job aborts due to reject limit

**Diagnosis**:

```bash
# Analyze reject file
cat /data/rejects/customer_rejects_2026-04-16.csv

# Count reject reasons
awk -F',' '{print $NF}' /data/rejects/customer_rejects_2026-04-16.csv | \
  sort | uniq -c | sort -rn

# Sample rejected records
head -20 /data/rejects/customer_rejects_2026-04-16.csv
```

**Common Issues**:

#### 1. Data Format Mismatch

```datastage
# Problem: Date format doesn't match
Source: "04/16/2026"
Expected: "2026-04-16"

# Solution: Add format conversion
DATE_FORMATTED = DateFromString(DATE_STRING, "%m/%d/%Y")
```

#### 2. Missing Required Fields

```datastage
# Problem: Null values in required fields
Constraint: Not(IsNull(EMAIL))

# Solution: Provide default or skip
EMAIL_CLEAN = If IsNull(EMAIL) Then "unknown@example.com" Else EMAIL
```

#### 3. Invalid Data Values

```datastage
# Problem: Values outside valid range
AGE = -5  # Invalid

# Solution: Add validation and correction
AGE_VALID = If AGE < 0 Or AGE > 120 Then Null Else AGE
```

### Issue: Data Mismatch Between Source and Target

**Symptoms**:
- Row counts don't match
- Data values different
- Missing or extra records

**Diagnosis**:

```sql
-- Compare row counts
SELECT 'Source' as location, COUNT(*) as row_count FROM source_table
UNION ALL
SELECT 'Target' as location, COUNT(*) as row_count FROM target_table;

-- Find missing records
SELECT source_id FROM source_table
EXCEPT
SELECT source_id FROM target_table;

-- Find extra records
SELECT target_id FROM target_table
EXCEPT
SELECT source_id FROM source_table;

-- Compare data values
SELECT 
  s.id,
  s.column1 as source_value,
  t.column1 as target_value
FROM source_table s
JOIN target_table t ON s.id = t.id
WHERE s.column1 != t.column1;
```

## Test Framework Issues

### Issue: Tests Failing

**Symptoms**:
- Test execution fails
- Import errors
- Connection failures

**Solutions**:

#### 1. Python Environment Issues

```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check imports
python -c "from tests.test_framework import DataStageTestFramework"
```

#### 2. Configuration Issues

```bash
# Verify test configuration
cat config/test_config.json

# Check environment variables
echo $DSHOME
echo $DS_PROJECT

# Set missing variables
export DSHOME=/opt/IBM/InformationServer/Server/DSEngine
export DS_PROJECT=TEST_PROJECT
```

#### 3. Database Connection Issues

```python
# Test database connectivity
import psycopg2
conn = psycopg2.connect(
    host="test-db-server",
    database="test_database",
    user="test_user",
    password="test_password"
)
print("Connection successful")
conn.close()
```

## Debugging Techniques

### 1. Enable Debug Logging

```bash
# Set log level to DEBUG
export DS_LOG_LEVEL=DEBUG

# Run job with verbose output
dsjob -run -wait -verbose PROJECT JOB_NAME
```

### 2. Use Peek Stages

```datastage
# Insert Peek stages to inspect data
Source → Peek → Transformer → Peek → Target

Peek Stage:
  Show First: 10 rows
  Show Last: 10 rows
  Output to: Log file
```

### 3. Row Count Stages

```datastage
# Add row count stages to track data flow
Source → Row Count → Transformer → Row Count → Target

# Check counts in log
grep "Row count" $DSHOME/Logs/JOB_NAME.log
```

### 4. Breakpoints

```datastage
# Use constraints as breakpoints
Transformer:
  Constraint: DEBUG_BREAK
  Expression: CUSTOMER_ID = 12345
  Action: Abort job
```

### 5. Sample Data

```datastage
# Process only sample of data for testing
Source Query:
  SELECT * FROM customers LIMIT 1000
  
# Or use sampling stage
Sample Stage:
  Sample Size: 1000
  Sample Method: First N rows
```

## Log Analysis

### Finding Errors in Logs

```bash
# Search for errors
grep -i "error" $DSHOME/Logs/JOB_NAME.log

# Search for warnings
grep -i "warning" $DSHOME/Logs/JOB_NAME.log

# Search for specific patterns
grep "ORA-" $DSHOME/Logs/JOB_NAME.log  # Oracle errors
grep "SQLSTATE" $DSHOME/Logs/JOB_NAME.log  # SQL errors

# Get context around errors
grep -A 5 -B 5 "error" $DSHOME/Logs/JOB_NAME.log
```

### Analyzing Performance

```bash
# Extract timing information
grep "Elapsed time" $DSHOME/Logs/JOB_NAME.log

# Extract row counts
grep "rows" $DSHOME/Logs/JOB_NAME.log

# Calculate throughput
# rows_processed / elapsed_time_seconds
```

### Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `ORA-01017: invalid username/password` | Wrong credentials | Check connection settings |
| `SQLSTATE=08001` | Connection failure | Check network/firewall |
| `Insufficient memory` | Out of memory | Reduce buffer sizes |
| `Deadlock detected` | Database deadlock | Retry or reorder operations |
| `File not found` | Missing file | Check file path |
| `Permission denied` | Insufficient permissions | Check file/directory permissions |

## Getting Help

### 1. Check Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)

### 2. Search Existing Issues

```bash
# Search GitHub issues
# https://github.com/your-org/datastage-pipeline-examples/issues

# Search Stack Overflow
# Tag: ibm-datastage
```

### 3. Collect Diagnostic Information

When reporting issues, include:

```bash
# System information
uname -a
cat /etc/os-release

# DataStage version
cat $DSHOME/Version

# Job information
dsjob -jobinfo -server your-server -user your-username \
  PROJECT JOB_NAME

# Recent logs
tail -100 $DSHOME/Logs/JOB_NAME.log

# Configuration
cat config/connections.json
cat config/parameters.json
```

### 4. Create Support Ticket

Include:
- Detailed problem description
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs
- System and version information
- Recent changes

### 5. Contact Team

- Email: etl-team@example.com
- Slack: #datastage-support
- Phone: +1-555-0123 (for critical issues)

## Prevention

### Regular Maintenance

```bash
# Weekly
- Review job failures
- Check disk space
- Monitor performance metrics

# Monthly
- Update documentation
- Review and optimize slow jobs
- Clean up old logs

# Quarterly
- Review security settings
- Update dependencies
- Conduct training
```

### Monitoring

Set up proactive monitoring:

```bash
# Monitor job execution
*/5 * * * * /scripts/check_job_status.sh

# Monitor disk space
0 * * * * /scripts/check_disk_space.sh

# Monitor database connections
*/15 * * * * /scripts/check_db_connections.sh

# Send alerts
if [ $ERROR_COUNT -gt 0 ]; then
  echo "Errors detected" | mail -s "DataStage Alert" team@example.com
fi
```

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Job Documentation](JOB_DOCUMENTATION.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)