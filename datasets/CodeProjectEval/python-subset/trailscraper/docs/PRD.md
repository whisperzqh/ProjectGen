# PRD Document for simpy

## Introduction

TrailScraper is a command-line tool designed to extract valuable information from AWS CloudTrail and serve as a general-purpose toolbox for working with IAM policies. The tool is available for installation via Homebrew on macOS, pip for Python environments, or can be run directly using Docker containers. It is classified as a utility tool for developers and system administrators, specifically targeting code generation, system administration, and security use cases.

## Goals

The primary goal of trailscraper is to enable users to generate IAM policies based on actual CloudTrail event data, bridging the gap between observed AWS API usage and proper IAM permission definitions. The tool accomplishes this by allowing users to download CloudTrail logs from S3 buckets, filter events based on various criteria (such as assumed role ARNs and time ranges), and automatically generate IAM policy statements from the recorded actions. Additionally, trailscraper aims to enhance policy management by providing intelligent features such as guessing related IAM actions that might not appear in CloudTrail logs—for example, suggesting Delete and Update permissions when only Create actions are present in the logs, helping users create more complete and practical IAM policies.

## Features and Functionalities

The following features and functionalities are expected in the project:

### CloudTrail Log Acquisition

- Ability to download CloudTrail logs from S3 buckets to local storage  
- Ability to specify multiple AWS account IDs for log downloads  
- Ability to specify multiple AWS regions for log downloads (including us-east-1 for global services)  
- Ability to download logs for organizational trails using organization IDs  
- Ability to customize S3 key prefix for log downloads  
- Ability to specify custom local directory for storing downloaded logs  
- Ability to wait until CloudTrail events for specified timeframe are available  
- Ability to configure parallel download concurrency (default: 10 parallel downloads)  

### Event Filtering and Selection

- Ability to filter CloudTrail events from local downloaded logs  
- Ability to filter CloudTrail events directly from CloudTrail API using lookup_events  
- Ability to filter events by assumed role ARN (supports multiple role ARNs)  
- Ability to filter events by time range using human-readable formats  
- Ability to output filtered CloudTrail records as JSON  

### Time Range Management

- Ability to specify time ranges using absolute dates (e.g., "2017-01-01")  
- Ability to specify time ranges using relative times (e.g., "one hour ago", "two days ago", "now")  
- Ability to filter downloads by date range (default: "one day ago" to "now")  
- Ability to check the timestamp of the most recent CloudTrail event in local logs  

### IAM Policy Generation

- Ability to generate IAM policy documents from CloudTrail records  
- Ability to read CloudTrail records from STDIN for policy generation  
- Ability to map CloudTrail event sources to IAM service prefixes  
- Ability to map CloudTrail event names to IAM action names  
- Ability to extract resource ARNs from CloudTrail events for IAM policy Resource fields  
- Ability to combine IAM statements with identical resources  
- Ability to combine IAM statements with identical actions  
- Ability to output IAM policies in standard JSON format  

### Policy Enhancement

- Ability to extend existing IAM policies by guessing related actions  
- Ability to infer related actions based on resource name patterns (e.g., from PutObject, guess GetObject, DeleteObject, ListObjects)  
- Ability to filter guessed actions by prefix (e.g., only Get actions)  
- Ability to validate guessed actions against known IAM actions  

### Data Source Options

- Ability to load CloudTrail records from local directory of downloaded logs  
- Ability to load CloudTrail records directly from CloudTrail API without local storage  
- Ability to process CloudTrail logs in organizational trail format  

### Command Pipeline Support

- Ability to chain commands using Unix pipes for composable workflows  
- Ability to combine download, select, generate, and guess commands in pipelines  

### Performance Optimization

- Ability to download multiple CloudTrail log files in parallel using thread pools  
- Ability to skip re-downloading CloudTrail logs that already exist locally  
- Ability to use smart directory listing for improved performance with large date ranges  

### Global Options

- Ability to enable verbose debug logging for troubleshooting  
- Ability to display version information  

### Output Compatibility

- Ability to convert generated IAM policies to CloudFormation YAML format using external tools  
- Ability to convert generated IAM policies to Terraform HCL format using external tools  










## Technical Constraints

- The repository must use Python as the primary programming language with a minimum version of Python 3.9  

- The repository must support Python versions 3.9, 3.10, 3.11, 3.12, and 3.13  

- The repository must provide a command-line interface using the Click library  

- The repository must use boto3 for AWS SDK functionality  

- The repository must use toolz for functional programming utilities  

- The repository must use dateparser and pytz for date/time parsing and timezone handling  

- The repository must use ruamel.yaml for YAML processing  

- The repository must use pylint for code style checking with a minimum score of 10  

- The repository must use pytest for testing  

- The repository must use setuptools for packaging and distribution  

## Requirements

### Python Version

- **Python >=3.9** - Minimum required Python version  

### Dependencies  

- `boto3==1.40.50` - AWS SDK for Python to interact with AWS services
- `click==8.1.8` - Command-line interface creation framework
- `toolz==1.0.0` - Functional programming utilities
- `dateparser==1.2.2` - Date parsing library for handling various date formats
- `pytz==2025.2` - Timezone definitions for Python
- `ruamel.yaml==0.18.15` - YAML parsing and formatting library

### Development Dependencies  

- `bumpversion==0.6.0` - Version bumping tool for releases
- `pylint==3.3.9` - Python code static analysis tool
- `pip==25.2` - Package installer for Python
- `pytest==8.4.2` - Testing framework
- `pytest-runner==6.0.1` - Plugin to run pytest from setup.py
- `setuptools==80.9.0` - Build system for Python packages
- `freezegun==1.5.5` - Library to mock/freeze time in tests
- `moto==4.2.14` - Library to mock AWS services for testing
- `wheel==0.45.1` - Built-package format for Python
- `twine==6.2.0` - Utility for publishing packages to PyPI

## Usage

TrailScraper is a command-line tool to get valuable information out of AWS CloudTrail and work with IAM policies.  

### Get CloudTrail events from CloudTrail API

To query CloudTrail API directly for events matching a filter:

```bash
trailscraper select --use-cloudtrail-api \ 
                    --filter-assumed-role-arn some-arn \ 
                    --from 'one hour ago' \ 
                    --to 'now'
```  

### Download CloudTrail Logs

To download logs from an S3 bucket:

```bash
trailscraper download --bucket some-bucket \
                      --account-id some-account-id \
                      --region some-other-region \ 
                      --region us-east-1 \
                      --from 'two days ago' \
                      --to 'now'
```  

### Download Logs from Organisational Trails

For AWS Organizations trails:

```bash
trailscraper download --bucket some-bucket \
                      --account-id some-account-id \
                      --region us-east-1 \
                      --org-id o-someorgid \
                      --from 'two days ago' \
                      --to 'now'
```  

### Find CloudTrail Events in Downloaded Logs

To search through previously downloaded logs:

```bash
trailscraper select --filter-assumed-role-arn some-arn \ 
                    --from 'one hour ago' \ 
                    --to 'now'
```  

### Generate IAM Policy from CloudTrail Records

To generate an IAM policy from CloudTrail events:

```bash
gzcat some-records.json.gz | trailscraper generate
```  

### Extend Policy by Guessing Related Actions

To expand a policy with related actions (e.g., adding Delete/Update when you have Create):

```bash
cat minimal-policy.json | trailscraper guess
```

Or to only guess specific action types:

```bash
cat minimal-policy.json | trailscraper guess --only Get
```  

### Combined Workflow: Select and Generate

To find CloudTrail events and generate an IAM policy in one command:

```bash
trailscraper select | trailscraper generate
```  

## Command Line Configuration Arguments

TrailScraper is a CLI tool built with Click framework that provides 5 main commands with various options:

### Global Options

```
Usage: trailscraper [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose    Enable debug logging
  --version    Show the version and exit.
  --help       Show this message and exit.
```  

### Commands

#### download
Downloads CloudTrail logs from S3 buckets to local storage.

```
Usage: trailscraper download [OPTIONS]

Options:
  --bucket TEXT               S3 bucket containing CloudTrail logs [required]
  --prefix TEXT               S3 key prefix including trailing slash [default: ""]
  --org-id TEXT               Organization ID for org-level trails (multiple)
  --account-id TEXT           AWS account ID [required, multiple]
  --region TEXT               AWS region [required, multiple]
  --log-dir PATH              Local directory for downloaded logs 
                              [default: ~/.trailscraper/logs]
  --from TEXT                 Start date (e.g., "2017-01-01", "-1days") 
                              [default: "one day ago"]
  --to TEXT                   End date (e.g., "2017-01-01", "now") 
                              [default: "now"]
  --wait                      Wait until events after timeframe are found
  --parallelism INTEGER       Number of parallel downloads [default: 10]
```  

#### select
Filters CloudTrail records from local files or CloudTrail API and outputs them as JSON.

```
Usage: trailscraper select [OPTIONS]

Options:
  --log-dir PATH                    Directory containing downloaded logs 
                                    [default: ~/.trailscraper/logs]
  --filter-assumed-role-arn TEXT    Filter by role ARN (multiple allowed)
  --use-cloudtrail-api             Query CloudTrail API instead of local files
  --from TEXT                       Start date filter [default: "1970-01-01"]
  --to TEXT                         End date filter [default: "now"]
```  

#### generate
Converts CloudTrail records from STDIN into an IAM policy document.

```
Usage: trailscraper generate [OPTIONS]

  Reads CloudTrail records from STDIN and outputs IAM policy JSON.

Options:
  (reads from STDIN, outputs to STDOUT)
```  

#### guess
Extends an existing IAM policy by inferring related actions.

```
Usage: trailscraper guess [OPTIONS]

  Reads IAM policy from STDIN and outputs extended policy with guessed actions.

Options:
  --only TEXT    Only guess actions with given prefix (multiple)
```  

#### last-event-timestamp
Displays the timestamp of the most recent CloudTrail event in the local log directory.

```
Usage: trailscraper last-event-timestamp [OPTIONS]

Options:
  --log-dir PATH    Directory to scan for events 
                    [default: ~/.trailscraper/logs]
```  
## Terms/Concepts Explanation

**CloudTrail**: An AWS service that records AWS API calls and events for an account, creating audit logs that capture who did what, when, and where in an AWS environment. TrailScraper downloads and processes these logs to generate IAM policies.  

**IAM (Identity and Access Management)**: AWS's authentication and authorization system that controls access to AWS resources through policies that define what actions are allowed or denied.  

**IAM Policy**: A JSON document that defines permissions by specifying allowed or denied actions on specific AWS resources. TrailScraper generates these automatically from observed CloudTrail events.  

**IAM Action**: A specific permission in an IAM policy formatted as `service:Operation` (e.g., `s3:GetObject`, `ec2:DescribeInstances`). Actions represent the operations that can be performed on AWS resources.

**IAM Statement**: A component of an IAM policy containing three key elements: Effect (Allow/Deny), Action (list of permissions), and Resource (list of ARNs or wildcards). Multiple statements combine to form a complete policy.

**PolicyDocument**: The top-level container for an IAM policy that includes a version identifier (typically "2012-10-17") and an array of statements.  

**CloudTrail Record/Event**: A structured JSON entry representing a single AWS API call, containing details like event time, event source, event name, and resource ARNs. TrailScraper parses these to extract IAM permissions.

**ARN (Amazon Resource Name)**: A unique identifier for AWS resources following the format `arn:aws:service:region:account-id:resource`. Used in IAM policies to specify which resources permissions apply to.  

**Event Source**: The AWS service that generated a CloudTrail event, formatted as a domain name (e.g., `s3.amazonaws.com`, `ec2.amazonaws.com`). TrailScraper maps these to IAM service prefixes.

**Event Name**: The name of the API operation recorded in CloudTrail (e.g., `GetObject`, `DescribeInstances`). TrailScraper transforms these into IAM action names using heuristics and special-case mappings.

**Assumed Role ARN**: The ARN of an IAM role that was temporarily assumed to perform an API call. Used as a filter in the `select` command to track actions performed by specific roles.  

**CloudTrail to IAM Mapping**: The process of converting CloudTrail event sources and event names into corresponding IAM service prefixes and action names. This involves complex heuristics due to naming inconsistencies between CloudTrail and IAM.  

**Statement Merging**: The process of consolidating multiple IAM statements that have the same Effect into a single statement with combined actions and resources, reducing policy redundancy.

**Action Guessing**: A feature that infers related IAM permissions based on existing actions in a policy. For example, if a policy has `s3:PutObject`, the guess command can suggest adding `s3:GetObject` and `s3:DeleteObject`.  

**Organizational Trail**: A CloudTrail configuration that logs events for all accounts in an AWS Organization rather than a single account. Requires the `--org-id` parameter when downloading logs.  

**Service Prefix**: The first part of an IAM action that identifies the AWS service (e.g., `s3`, `ec2`, `cloudwatch`). TrailScraper extracts these from CloudTrail event sources, handling special cases where naming conventions differ.

**Global Services Region (us-east-1)**: Certain AWS services like IAM, CloudFront, and Route53 log their events only in the us-east-1 region, even when used globally. TrailScraper requires including this region to capture all events.  

**Least Privilege**: An AWS security best practice where IAM policies grant only the minimum permissions necessary for a task. TrailScraper supports this by generating policies based on actual observed usage rather than broad permissions.
