## Introduction

This document outlines the product requirements for `cookiecutter`, a command-line utility and Python library designed to create projects from project templates. The project aims to provide a simple yet powerful solution for project scaffolding, enabling developers to quickly generate standardized project structures from reusable templates.

## Goals

The primary goal of `cookiecutter` is to offer an efficient and easy-to-use tool for generating projects from templates, streamlining project creation and standardizing project structures across teams and organizations. It aims to assist developers, teams, and organizations in quickly bootstrapping new projects with consistent structure and best practices.

## Features and Functionalities

### 1. Cross-Platform Template Generation

Cookiecutter supports running on Windows, Mac, and Linux operating systems. This cross-platform compatibility is one of the core design principles of the project.

### 2. Multiple Template Sources Support

Cookiecutter can fetch templates from various sources:

- **Local Directories**: Directly use templates from the local filesystem 
- **Git Repositories**: Support for GitHub, GitLab, Bitbucket and other Git repositories, including shorthand forms (e.g., `gh:`, `gl:`, `bb:`)
- **Mercurial Repositories**: Support for Mercurial version control system
- **ZIP Files**: Support for local or online ZIP archives
- **Private Repositories**: Support for accessing private repositories using `git+` or `hg+` prefixes

### 3. Interactive User Prompting

Cookiecutter provides rich user interaction capabilities:

- **Multiple Variable Types**: Support for string, number, boolean, choice list, and dictionary type variables
- **Dynamic Default Values**: Support for computing default values using Jinja2 template syntax
- **Human-Readable Prompts**: Customizable prompt text for better user experience
- **Input Validation**: Ability to validate user input through hooks

### 4. Jinja2 Template Rendering

Powerful and flexible project customization using the Jinja2 templating engine:

- **Variable Substitution**: Using `{{cookiecutter.variable_name}}` syntax
- **Conditional Logic**: Support for `{% if %}` conditional statements
- **Filters**: Built-in filters such as `jsonify` and `slugify`
- **Strict Mode**: Uses strict Jinja2 environment where undefined variables raise errors

### 5. Hooks System

Provides three types of hooks for executing custom scripts at different stages:

- **pre_prompt**: Executes before prompting the user, useful for environment checks
  - Working directory: Root directory of the repository copy
  - Can modify `cookiecutter.json`
  
- **pre_gen_project**: Executes before project generation, useful for input validation
  - Working directory: Root directory of the generated project
  - Supports template variables
  
- **post_gen_project**: Executes after project generation, useful for initialization setup
  - Can conditionally delete files/directories

- **Multi-Language Support**: Hooks can be Python scripts or shell scripts
- **Error Handling**: Hook failures stop project generation and trigger cleanup

### 6. Replay Functionality

Records and replays project generation parameters for reproducible project creation:

- **Automatic Saving**: Automatically saves user input to `~/.cookiecutter_replay/` on each run
- **Replay Mode**: Use the `--replay` flag to reuse previous inputs
- **Custom Replay Files**: Support for specifying custom files using `--replay-file`
- **Cross-Machine Usage**: Can use the same replay file across multiple machines
- **API Support**: Replay functionality is also available through the Python API

### 7. Configuration Management

Support for user configuration files to set defaults and preferences:

- **Configuration File Location**: `~/.cookiecutterrc`
- **Configuration Options**: Includes `cookiecutters_dir` (template cache directory) and `replay_dir` (replay file directory) 
- **Environment Variable Expansion**: Configuration values support environment variables and user home directory expansion
- **Default Context**: Can set default values for commonly used templates

### 8. Extension System

Built-in and custom Jinja2 extensions to enhance template capabilities:

**Built-in Extensions**:

- **JsonifyExtension**: Converts Python objects to JSON
- **RandomStringExtension**: Generates random strings
- **SlugifyExtension**: String slugification
- **TimeExtension**: Date and time handling
- **UUIDExtension**: Generates UUIDs

**Custom Extensions**:

- **Template-Level Extensions**: Specified via the `_extensions` field in `cookiecutter.json`
- **Local Extensions**: Templates can include their own extension modules
- **Simple Filters**: Quick filter creation using the `@simple_filter` decorator

### 9. No-Input Mode

Generate projects without user interaction:

- **Use Default Values**: Use the `--no-input` flag to skip all prompts
- **Extra Context**: Override default values via the `extra_context` parameter
- **Automation Scenarios**: Suitable for CI/CD pipelines and automation scripts
- **Force Refresh**: No-input mode defaults to deleting and re-downloading cached resources

### 10. Rich Terminal Output

Enhanced terminal output formatting for better user experience:

- **Colored Output**: Uses the rich library to provide colored and formatted terminal output
- **Progress Indicators**: Displays operation progress
- **Error Messages**: Clear error messages and stack traces
- **Debug Mode**: Enable verbose logging using the `-v` or `--verbose` flag

### 11. Advanced Features

**Nested Templates**: Support for templates containing multiple sub-templates

**Selective Rendering**: Use `_copy_without_render` to specify files that should not be rendered

**Branch/Tag Support**: Use the `--checkout` parameter to specify Git branches, tags, or commits

**Directory Selection**: Use the `--directory` parameter to specify a subdirectory within the repository

**File Skipping**: Use `--skip-if-file-exists` to avoid overwriting existing files

**Hook Control**: Use the `--accept-hooks` parameter to control whether hooks are executed

## Supporting Data Description

The `cookiecutter` project utilizes configuration files and template structures to enable project generation:

**Template Structure:**

- **`cookiecutter.json`:**
  - **Purpose:** Defines template variables and default values for user prompts.
  - **Content:** JSON object containing variable names and their default values or options.

- **`hooks/` Directory:**
  - **Purpose:** Contains optional pre and post generation scripts.
  - **Files:** `pre_gen_project.py`, `post_gen_project.py`, `pre_prompt.py`
  - **Function:** Execute custom logic before/after project generation.

- **Template Files:**
  - **Structure:** Files and directories with Jinja2 template syntax using `{{cookiecutter.variable_name}}` placeholders.
  - **Purpose:** Define the structure and content of generated projects.

**User Configuration:**

- **`.cookiecutterrc`:**
  - **Location:** User's home directory
  - **Format:** YAML configuration file
  - **Purpose:** Store user preferences, default values, and template aliases.

## Usage

```bash
# Basic usage - generate from a template
cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage

# Generate without prompts using defaults
cookiecutter template-url --no-input

# Generate with custom output directory
cookiecutter template-url --output-dir ./projects

# Replay previous generation
cookiecutter template-url --replay

# Use specific branch/tag
cookiecutter template-url --checkout v1.0.0
```

**Programmatic Usage:**

```python
from cookiecutter.main import cookiecutter

# Generate project programmatically
cookiecutter('template-url', no_input=True, extra_context={'project_name': 'MyProject'})
```


## Requirements

### Dependencies

- **binaryornot** (>=0.4.4): Binary file detection
- **Jinja2** (>=2.7, <4.0.0): Template rendering engine
- **click** (>=7.0, <9.0.0): Command-line interface framework
- **pyyaml** (>=5.3.1): YAML configuration parsing
- **python-slugify** (>=4.0.0): String slugification
- **requests** (>=2.23.0): HTTP requests for template fetching
- **arrow**: Date and time handling
- **rich**: Terminal output formatting

### Python Version

- **Python 3.8 or newer** required

### Development Dependencies 

- **pre-commit**: Code quality and linting
- **pytest**: Testing framework with 100% code coverage requirement
- **safety**: Security vulnerability checking
- **sphinx**: Documentation generation

## Data Requirements

- **Template Sources**: Support for Git repositories, Mercurial repositories, local directories, and ZIP archives.
- **Data Storage**: Templates are cloned/downloaded to a local cache directory; user configuration stored in home directory.
- **Data Security and Privacy**: The library does not transmit user data; all processing is local.
- **Version Control**: Templates can specify branches, tags, or commits for version control.

## Design and User Interface

As a command-line utility and library, `cookiecutter` provides:

**Command-Line Interface:**
- Interactive prompts for template variables
- Rich terminal output with formatting
- Progress indicators and error messages
- Help documentation via `--help` flag

**Python API:**
- Clean, Pythonic function interface through `cookiecutter.main.cookiecutter()`
- Comprehensive parameter support for programmatic control
- Exception handling for error cases

**Design Principles:**
- Simplicity and ease of use
- Extensibility through hooks and extensions
- Conservative approach to core features
- Small, maintainable codebase

