# PRD Document for zxcvbn

## Introduction

zxcvbn-python is a realistic password strength estimator that serves as a Python implementation of the original library created by the team at Dropbox.The original library was written for JavaScript, and while other Python ports may exist, this particular implementation is noted as the most up-to-date version and is recommended by the original developers of zxcvbn.  

## Goals

The primary goals of this project are to provide comprehensive password strength assessment capabilities across modern Python versions. The library aims to accept user-specific data (such as names and birthdates) to enhance dictionary-based testing, assign passwords a score ranging from 0 (terrible) to 4 (great), provide actionable feedback on how to improve passwords, and estimate the time required to crack passwords under various attack scenarios.  

## Features and Functionalities

The following features and functionalities are available in the zxcvbn-python project:

### Password Strength Estimation
- Ability to evaluate password strength with a score from 0 (terrible) to 4 (great)  
- Ability to calculate the number of guesses required to crack the password  
- Ability to estimate calculation time for password analysis  
- Ability to provide logarithmic representation of guesses (base 10)  

### Pattern Detection and Matching
- Ability to detect dictionary matches against multiple word lists (passwords, names, surnames, Wikipedia terms, TV/film references)  
- Ability to detect reversed dictionary matches  
- Ability to detect l33t speak substitutions (e.g., '@' for 'a', '3' for 'e')  
- Ability to detect spatial keyboard patterns (QWERTY, Dvorak, keypad layouts)  
- Ability to detect repeat patterns (e.g., "aaa" or "abcabcabc")  
- Ability to detect sequence patterns (e.g., "abc", "6543") with support for Unicode characters  
- Ability to detect regex patterns including recent years  
- Ability to detect date patterns with or without separators  

### Attack Time Estimation
- Ability to estimate crack times for online throttled attacks (100 attempts per hour)  
- Ability to estimate crack times for online unthrottled attacks (10 attempts per second)  
- Ability to estimate crack times for offline slow hashing attacks (1e4 attempts per second)  
- Ability to estimate crack times for offline fast hashing attacks (1e10 attempts per second)  
- Ability to display crack times in human-readable format (seconds, minutes, hours, days, months, years, centuries)  

### User Customization
- Ability to accept user-specific data (name, birthdate, etc.) to test against  
- Ability to add custom frequency lists/dictionaries to the pattern matching  
- Ability to override default maximum password length of 72 characters  
- Ability to sanitize user inputs by converting to lowercase  

### Feedback Generation
- Ability to provide warnings about password weaknesses  
- Ability to provide specific suggestions for password improvement  
- Ability to provide pattern-specific feedback (dictionary, spatial, repeat, sequence, regex, date patterns)  
- Ability to warn about common password issues like capitalization, reversals, and l33t substitutions  

### Built-in Dictionary Support
- Ability to test against common passwords dictionary  
- Ability to test against English Wikipedia terms dictionary  
- Ability to test against female names dictionary  
- Ability to test against surnames dictionary  
- Ability to test against US TV and film references dictionary  
- Ability to test against male names dictionary  

### Command-Line Interface
- Ability to use zxcvbn from the command line with piped input  
- Ability to specify user inputs via command-line arguments  
- Ability to specify custom max-length via command-line arguments  
- Ability to output results in JSON format  
- Ability to read password from stdin or prompt user securely  

### Guessing Algorithm
- Ability to calculate guesses based on uppercase variations  
- Ability to calculate guesses based on l33t variations  
- Ability to calculate spatial pattern complexity including turns and shifted keys  
- Ability to optimize match sequence selection to find minimum guessable path  

### Python Version Support
- Ability to run on Python versions 3.8 through 3.13  

## Technical Constraints

- The repository must use **Python 3.8-3.13** as the primary programming language  

- The repository must support Python versions 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13  

- The repository must provide a **command-line interface using argparse** (not Click) from the standard library  

- The repository must have **no external runtime dependencies** - it uses only Python standard library modules (os, datetime, json, select, sys, getpass, argparse, codecs, operator)  

- The repository must enforce a **default maximum password length of 72 characters**, configurable via the `max_length` parameter  

- The repository must support **type checking with mypy** as part of the build process  

- The repository must use **pytest** for testing (version 3.5.0 for Python <3.6, version 7.4.2 for Python ≥3.6)  

- The repository must use **setuptools** for packaging and distribution  

- The repository must provide **console script entry points** for CLI access  

- The repository must maintain **frequency list data files** in plain text format for password dictionaries  

## Requirements

### Dependencies

This project has **no external runtime dependencies**. The zxcvbn-python library uses only the Python standard library and does not require any third-party packages to be installed.  

### Development Dependencies

- `pytest==3.5.0` (for Python < 3.6) or `pytest==7.4.2` (for Python >= 3.6) - Testing framework  

- `tox` - Test automation tool for running tests across multiple Python versions  

- `mypy` - Static type checker for Python  

### Python Version Support

- Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13  



## Usage

### Basic Usage

Import the library and pass a password to evaluate its strength:

```python
from zxcvbn import zxcvbn

results = zxcvbn('JohnSmith123', user_inputs=['John', 'Smith'])

print(results)
```  

The function returns a dictionary with detailed information including a score (0-4), time estimates to crack the password, and feedback for improvement.  

### Advanced Usage Examples

**Override maximum password length:**

```python
from zxcvbn import zxcvbn

results = zxcvbn('JohnSmith321', user_inputs=['John', 'Smith'], max_length=88)
```  

**Add custom ranked dictionaries:**

```python
from zxcvbn.matching import add_frequency_lists

add_frequency_lists({
    'my_list': ['foo', 'bar'],
    'another_list': ['baz']
})
```  

### CLI Usage

Evaluate password strength from the command line:

```bash
echo 'password' | zxcvbn --user-input <user-input> | jq
```  

With custom max length:

```bash
echo '<long password>' | zxcvbn --max-length 142
```  

Or execute as a Python module:

```bash
echo 'password' | python -m zxcvbn --user-input <user-input> | jq
```  

## Command Line Configuration Arguments

The zxcvbn-python project provides a CLI interface with the following options:  

```
Usage: zxcvbn [OPTIONS]

Description: Python implementation of Dropbox's realistic password strength estimator

Options:
  --user-input TEXT       User data to be added to the dictionaries that are 
                          tested against (name, birthdate, etc). Can be used 
                          multiple times.
  
  --max-length INTEGER    Override password max length (default: 72)
```

The CLI reads the password from stdin or prompts for it interactively if stdin is not available.  

**Example Usage:**  

```bash
echo 'password' | zxcvbn --user-input <user-input> | jq
```

or with max-length:

```bash
echo '<long password>' | zxcvbn --max-length 142
```


## Terms/Concepts Explanation

**Password Strength Estimation**: A realistic assessment of how difficult a password is to crack, based on pattern recognition and entropy calculation rather than simple rules like character requirements.  

**Guesses**: The estimated number of attempts an attacker would need to crack a password, calculated by analyzing detected patterns and their combinations. This is the core metric used to evaluate password strength.  

**Score**: A simplified password strength rating from 0 (terrible) to 4 (great), derived from the number of guesses using logarithmic thresholds (< 10³, < 10⁶, < 10⁸, < 10¹⁰, and ≥ 10¹⁰).  

**Pattern Matching**: The process of identifying recognizable patterns in passwords such as dictionary words, keyboard patterns, sequences, repeats, dates, and l33t speak substitutions.  

**Dictionary Match**: Matching password substrings against ranked frequency lists of common passwords, English words, names, surnames, and other commonly used terms.  

**Spatial Match**: Detection of keyboard patterns based on the physical adjacency of keys on common keyboard layouts (QWERTY, Dvorak, numeric keypad), including tracking of turns and shifted characters.  

**Sequence Match**: Identification of sequential character patterns like "abc", "6543", or "XYZ" by analyzing repeated differences in Unicode codepoints.  

**Repeat Match**: Detection of repeated patterns such as "aaa" or "abcabcabc" using both greedy and lazy regex matching to find the shortest base pattern.  

**L33t Speak (Leetspeak)**: Character substitutions where letters are replaced with similar-looking numbers or symbols (e.g., '@' for 'a', '3' for 'e', '0' for 'o'). The library detects these substitutions and calculates the reduced entropy they provide.  

**Frequency Lists**: Pre-ranked dictionaries containing common passwords, English Wikipedia words, names, surnames, and TV/film references, ordered by frequency of use. Words appearing earlier in the list (lower rank) are considered more common and easier to guess.  

**Adjacency Graphs**: Data structures representing the physical layout of keyboard keys, mapping each key to its neighboring keys in different directions, used to calculate the entropy of spatial patterns.  

**Crack Time Estimates**: Projected time required to crack a password under different attack scenarios: online with throttling (100/hour), online without throttling (10/second), offline slow hashing (10⁴/second), and offline fast hashing (10¹⁰/second).  

**User Inputs**: Custom words or data (like names, birthdates, company names) that can be added to the dictionary matching to account for personalized information an attacker might know about the target.  

**Feedback**: Actionable suggestions provided to users for improving weak passwords, including warnings about specific pattern vulnerabilities and recommendations for stronger alternatives.  

**Match Sequence**: The optimal non-overlapping combination of detected patterns that covers the entire password with the minimum estimated guesses, calculated using dynamic programming.  

**Ranked Dictionary**: A mapping of words to their rank (position) in a frequency list, where lower numbers indicate more common words that are easier to guess.  
