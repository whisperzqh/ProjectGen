# Architecture Design

Below is a text-based representation of the file tree. 
```bash
├── cookiecutter
│   ├── cli.py
│   ├── config.py
│   ├── environment.py
│   ├── exceptions.py
│   ├── extensions.py
│   ├── find.py
│   ├── generate.py
│   ├── hooks.py
│   ├── __init__.py
│   ├── log.py
│   ├── __main__.py
│   ├── main.py
│   ├── prompt.py
│   ├── replay.py
│   ├── repository.py
│   ├── utils.py
│   ├── vcs.py
│   ├── VERSION.txt
│   └── zipfile.py
```

`__init__.py`:

- `_get_version()`: Reads the contents of the `VERSION.txt` file located in the same directory as this module and returns the version string stripped of leading/trailing whitespace.

- `__version__`: A module-level variable that holds the current version of the package, populated by calling `_get_version()` at import time.

`__main__.py`:

`cli.py`:

- `version_msg()`: Returns a formatted string containing the Cookiecutter version, its installation location, and the version of Python being used.

- `validate_extra_context(_ctx, _param, value)`: Validates and parses command-line extra context arguments provided in the form of `key=value` strings. Converts them into an `OrderedDict`; raises a `click.BadParameter` error if any item does not conform to the expected format.

- `list_installed_templates(default_config, passed_config_file)`: Lists all locally installed Cookiecutter templates by scanning the `cookiecutters_dir` directory for subdirectories containing a `cookiecutter.json` file. Exits with an error if the directory does not exist.

- `main(template, extra_context, no_input, checkout, verbose, replay, overwrite_if_exists, output_dir, config_file, default_config, debug_file, directory, skip_if_file_exists, accept_hooks, replay_file, list_installed, keep_project_on_failure)`: The main Click command-line interface function for Cookiecutter. Orchestrates project generation from a template by parsing CLI arguments, configuring logging, handling user prompts (e.g., for hooks), and invoking the core `cookiecutter()` function. Also supports listing installed templates and displaying help. Handles and reports various exceptions that may occur during template processing.

`config.py`:

- `_expand_path(path)`: Expands both environment variables (e.g., `$HOME`) and the user home directory symbol (`~`) in the given path string, returning a normalized absolute path.

- `merge_configs(default, overwrite)`: Recursively merges two dictionaries. If a value in `overwrite` is itself a dictionary, it is merged into the corresponding sub-dictionary in `default`, preserving any existing keys not overridden.

- `get_config(config_path)`: Loads and parses a YAML configuration file from the specified `config_path`. Validates that the top-level content is a dictionary, merges it with `DEFAULT_CONFIG`, and expands any paths in the `replay_dir` and `cookiecutters_dir` fields using `_expand_path`. Raises exceptions if the file doesn’t exist or contains invalid YAML.

- `get_user_config(config_file, default_config)`: Determines and returns the effective user configuration for Cookiecutter. Behavior depends on the arguments:
  - If `default_config` is `True`, returns a copy of `DEFAULT_CONFIG`.
  - If `default_config` is a dictionary, merges it with `DEFAULT_CONFIG` and returns the result.
  - If `config_file` is provided and differs from the default path, loads config from that file.
  - Otherwise, checks the `COOKIECUTTER_CONFIG` environment variable for a custom config path.
  - If no environment variable is set, attempts to load from the default user config file (`~/.cookiecutterrc`).
  - Falls back to `DEFAULT_CONFIG` if no user config file exists.

`environment.py`:

- `ExtensionLoaderMixin.__init__(self, context, **kwargs)`: Initializes a Jinja2 environment with support for loading custom extensions. It combines built-in default extensions with any specified in the `cookiecutter.json` file under the `_extensions` key. If an extension fails to load, it raises an `UnknownExtension` exception with a descriptive error message.

- `ExtensionLoaderMixin._read_extensions(self, context)`: Extracts and returns a list of extension module paths (as strings) from the `cookiecutter._extensions` key in the provided context dictionary. Returns an empty list if the key is not present.

- `StrictEnvironment.__init__(self, **kwargs)`: Initializes a strict Jinja2 environment that uses `StrictUndefined` as the undefined variable handler—causing template rendering to fail immediately if an undefined variable is referenced. Also loads any extensions defined in the context via the `ExtensionLoaderMixin`.

`exceptions.py`:

- `CookiecutterException`: Base exception class for all Cookiecutter-specific errors. All other exceptions in this module inherit from this class.

- `NonTemplatedInputDirException`: Exception raised when a project’s input directory name is not templated—that is, it does not contain any Jinja2 placeholders—making it impossible to ensure the input directory differs from the output directory.

- `UnknownTemplateDirException`: Exception raised when Cookiecutter cannot unambiguously identify the project template directory, such as when multiple directories appear to be valid templates.

- `MissingProjectDir`: Exception raised during repository cleanup when the expected generated project directory cannot be found inside the cloned repository.

- `ConfigDoesNotExistException`: Exception raised when a specified configuration file path does not point to an existing file.

- `InvalidConfiguration`: Exception raised when the global configuration file is either not valid YAML or is structurally invalid (e.g., top-level element is not a dictionary).

- `UnknownRepoType`: Exception raised when Cookiecutter cannot determine the type of a given repository (e.g., Git, Mercurial, or Zip).

- `VCSNotInstalled`: Exception raised when a required version control system (such as Git or Mercurial) is not installed on the system.

- `ContextDecodingException`: Exception raised when the `cookiecutter.json` context file cannot be decoded as valid JSON.

- `OutputDirExistsException`: Exception raised when the target output directory already exists and overwriting is not enabled.

- `EmptyDirNameException`: Exception raised when a directory name provided during project generation is empty.

- `InvalidModeException`: Exception raised when mutually exclusive modes are used together—specifically, when both `no_input=True` and `replay=True` are specified.

- `FailedHookException`: Exception raised when a pre- or post-generation hook script fails to execute successfully.

- `UndefinedVariableInTemplate`: Exception raised when a Jinja2 template references a variable that is not defined in the rendering context. Stores the original Jinja2 error, a descriptive message, and the full context for debugging.

  - `__init__(self, message, error, context)`: Initializes the exception with a custom message, the underlying `jinja2.TemplateError`, and the template context dictionary.
  
  - `__str__(self)`: Returns a human-readable string combining the message, the Jinja2 error detail, and the context.

- `UnknownExtension`: Exception raised when Cookiecutter fails to import a Jinja2 extension listed in the template’s `_extensions` configuration.

- `RepositoryNotFound`: Exception raised when the specified Cookiecutter template repository (e.g., a Git URL) does not exist or cannot be found.

- `RepositoryCloneFailed`: Exception raised when cloning a remote Cookiecutter template repository fails (e.g., due to network issues or authentication errors).

- `InvalidZipRepository`: Exception raised when a provided Zip file is not a valid Cookiecutter template repository (e.g., malformed or missing `cookiecutter.json`).

`extensions.py`:

- `JsonifyExtension.__init__(self, environment)`: Initializes the Jinja2 extension that adds a `jsonify` filter to the environment. This filter converts a Python object into a JSON-formatted string with sorted keys and optional indentation (default: 4 spaces).

- `RandomStringExtension.__init__(self, environment)`: Initializes the Jinja2 extension that adds a global function `random_ascii_string` to the environment. This function generates a random string of specified length using ASCII letters, optionally including punctuation characters.

- `SlugifyExtension.__init__(self, environment)`: Initializes the Jinja2 extension that adds a `slugify` filter to the environment. This filter converts a given string into a URL-friendly slug using the `python-slugify` library, with full support for its parameters (e.g., separator, max length, stopwords, regex patterns, Unicode support, etc.).

- `UUIDExtension.__init__(self, environment)`: Initializes the Jinja2 extension that adds a global function `uuid4` to the environment. This function generates and returns a random UUID4 as a string.

- `TimeExtension.__init__(self, environment)`: Initializes the Jinja2 extension for handling date and time operations. Sets a default `datetime_format` of `'%Y-%m-%d'` on the environment and registers the `{% now %}` tag.

- `TimeExtension._now(self, timezone, datetime_format)`: Returns a string representation of the current date and time in the specified timezone, formatted according to `datetime_format`. If `datetime_format` is `None`, uses the environment’s default format.

- `TimeExtension._datetime(self, timezone, operator, offset, datetime_format)`: Computes a shifted date/time from the current moment in the given `timezone` by applying an offset (e.g., `"hours=2,days=1"`), using the provided arithmetic `operator` (`+` or `-`). Returns the result formatted as a string using `datetime_format` (or the environment default if not provided).

- `TimeExtension.parse(self, parser)`: Parses the `{% now %}` Jinja2 tag from the template. Supports three usage forms:
  - `{% now "UTC" %}` → current time in UTC.
  - `{% now "UTC", "%Y" %}` → current time with custom format.
  - `{% now "UTC" + "hours=2" %}` or `{% now "UTC" - "days=1" %}` → shifted time with optional custom format.
  Constructs and returns a Jinja2 AST `Output` node that calls the appropriate internal method (`_now` or `_datetime`).

`find.py`:

- `find_template(repo_dir, env)`: Searches the given `repo_dir` (a local directory containing a cloned Cookiecutter template repository) for a subdirectory that appears to be the project template. A valid template directory must:
  - Contain the word `'cookiecutter'` in its name,
  - Include both the Jinja2 `variable_start_string` (e.g., `{{`) and `variable_end_string` (e.g., `}}`) in its name, indicating it is templated.
  
  If such a directory is found, its absolute path is returned as a `Path` object. If no matching directory is found, raises `NonTemplatedInputDirException`.

`generate.py`:

- `is_copy_only_path(path, context)`: Determines whether a given file or directory path should be copied without rendering by checking if it matches any pattern listed under the `_copy_without_render` key in the cookiecutter context. Returns `True` if a match is found; otherwise, returns `False`.

- `apply_overwrites_to_context(context, overwrite_context, in_dictionary_variable)`: Recursively updates the `context` dictionary in place using values from `overwrite_context`. Handles special cases such as:
  - Choice and multichoice variables (lists),
  - Nested dictionaries (partial updates),
  - Boolean variables (converted from string using `YesNoPrompt`),
  - New top-level variables (ignored unless inside a nested dictionary).
  Raises `ValueError` if an overwrite value is invalid for the variable type.

- `generate_context(context_file, default_context, extra_context)`: Loads and parses a `cookiecutter.json` file into an ordered dictionary, then applies `default_context` (from user config) and `extra_context` (from CLI) as overrides using `apply_overwrites_to_context`. Returns the final context as a dictionary with the filename stem (e.g., `cookiecutter`) as the top-level key. Raises `ContextDecodingException` if the JSON is invalid.

- `generate_file(project_dir, infile, context, env, skip_if_file_exists)`: Renders a single template file or copies it verbatim:
  - If the file is binary (detected via `binaryornot`), it is copied without modification.
  - If text, it is rendered using the Jinja2 environment.
  - The output filename is also rendered from the input path.
  - Preserves original file permissions and newline characters (or uses `_new_lines` from context if specified).
  - Skips generation if `skip_if_file_exists` is `True` and the output file already exists.

- `render_and_create_dir(dirname, context, output_dir, environment, overwrite_if_exists)`: Renders a directory name using the Jinja2 environment and creates the directory under `output_dir`. Raises `EmptyDirNameException` if the input name is empty, or `OutputDirExistsException` if the directory already exists and `overwrite_if_exists` is `False`. Returns the absolute path of the created directory and a boolean indicating whether it was newly created.

- `_run_hook_from_repo_dir(repo_dir, hook_name, project_dir, context, delete_project_on_failure)`: Deprecated wrapper that issues a `DeprecationWarning` and delegates to `cookiecutter.hooks.run_hook_from_repo_dir`.

- `generate_files(repo_dir, context, output_dir, overwrite_if_exists, skip_if_file_exists, accept_hooks, keep_project_on_failure)`: Orchestrates the full project generation process:
  1. Loads the Jinja2 environment with the given context.
  2. Locates the template directory using `find_template`.
  3. Renders and creates the root project directory.
  4. If enabled, runs the `pre_gen_project` hook.
  5. Walks the template directory recursively:
     - Directories and files marked in `_copy_without_render` are copied without rendering.
     - Other directories are rendered and created.
     - Other files are rendered via `generate_file`.
  6. If any rendering step fails with an `UndefinedError`, and the project was newly created, it is deleted unless `keep_project_on_failure` is `True`.
  7. If enabled, runs the `post_gen_project` hook.
  Returns the absolute path to the generated project directory.

`hooks.py`:

- `valid_hook(hook_file, hook_name)`: Determines whether a given file qualifies as a valid hook script. A file is valid if:
  - Its basename (without extension) matches the expected `hook_name`,
  - The hook name is one of the supported hooks (`pre_prompt`, `pre_gen_project`, `post_gen_project`),
  - It is not a backup file (i.e., does not end with `~`).

- `find_hook(hook_name, hooks_dir)`: Searches the `hooks_dir` (default: `'hooks'`) within the current working directory (assumed to be a project template root) for scripts matching the specified `hook_name`. Returns a list of absolute paths to matching hook scripts, or `None` if none are found.

- `run_script(script_path, cwd)`: Executes a hook script at `script_path` from the working directory `cwd`. Makes the script executable first. Supports both shell scripts and Python scripts (detected by `.py` extension). Raises `FailedHookException` if the script exits with a non-zero status or fails to execute due to OS errors (e.g., missing shebang).

- `run_script_with_context(script_path, cwd, context)`: Renders the contents of a hook script using the Jinja2 templating engine with the provided `context`, writes the result to a temporary file preserving the original extension, and executes it via `run_script`.

- `run_hook(hook_name, project_dir, context)`: Attempts to locate and execute all hook scripts matching `hook_name` from the template’s `hooks/` directory. Each script is rendered with the project `context` before execution. If no matching hooks exist, the function does nothing.

- `run_hook_from_repo_dir(repo_dir, hook_name, project_dir, context, delete_project_on_failure)`: Runs a specified hook (`pre_gen_project` or `post_gen_project`) from within the template repository directory (`repo_dir`). If the hook fails (raises `FailedHookException` or `UndefinedError`), and `delete_project_on_failure` is `True`, the partially generated `project_dir` is deleted. Re-raises the exception after cleanup.

- `run_pre_prompt_hook(repo_dir)`: Executes the `pre_prompt` hook before user prompts are shown. Since this hook runs before context is gathered, it is not rendered with a context. If a `pre_prompt` hook exists:

`log.py`:

- `configure_logger(stream_level, debug_file)`: Configures the `'cookiecutter'` logger with the specified console log level (`stream_level`) and optionally enables debug-level logging to a file (`debug_file`).

`main.py`:

- `cookiecutter(template, checkout=None, no_input=False, extra_context=None, replay=None, overwrite_if_exists=False, output_dir='.', config_file=None, default_config=False, password=None, directory=None, skip_if_file_exists=False, accept_hooks=True, keep_project_on_failure=False)`:  
  Run Cookiecutter just as if using it from the command line. This function orchestrates the entire template rendering process: it resolves the template source (local or remote), handles user input or replay mode, processes hooks, prompts for missing context variables, and generates the final project files. It also manages temporary directories and cleanup.

- `_patch_import_path_for_repo.__init__(self, repo_dir)`:  
  Initializes a context manager that temporarily adds the given repository directory to Python’s `sys.path` to allow importing modules from the template during hook execution or dynamic configuration.

- `_patch_import_path_for_repo.__enter__(self)`:  
  Enters the runtime context by appending the repository directory to `sys.path`, enabling Python imports from the template directory.

- `_patch_import_path_for_repo.__exit__(self, _type, _value, _traceback)`:  
  Exits the runtime context by restoring the original `sys.path`, ensuring no side effects persist after template processing.

`prompt.py`:

- `read_user_variable(var_name, default_value, prompts=None, prefix="")`:  
  Prompt user for a variable and return the entered value or the given default. Uses Rich’s `Prompt.ask` to collect input with an optional descriptive prompt.

- `YesNoPrompt.process_response(self, value)`:  
  Converts user input strings to boolean values based on predefined yes/no choices. Raises `InvalidResponse` if the input doesn’t match any known truthy or falsy values.

- `read_user_yes_no(var_name, default_value, prompts=None, prefix="")`:  
  Prompt the user to reply with 'yes' or 'no' (or equivalent values like "y"/"n", "true"/"false", etc.). Returns a boolean. Actual parsing is handled by the `YesNoPrompt` class.

- `read_repo_password(question)`:  
  Prompt the user to enter a password securely (input is hidden). Used when authenticating with private repositories.

- `read_user_choice(var_name, options, prompts=None, prefix="")`:  
  Prompt the user to choose from a list of options for a given variable. Displays a numbered menu and returns the selected option. Supports human-readable prompts and descriptions via a structured `prompts` dictionary.

- `process_json(user_value)`:  
  Attempt to parse a user-provided string as a JSON dictionary. Raises `InvalidResponse` if parsing fails or the result is not a dictionary.

- `JsonPrompt.process_response(value)`:  
  Static method that converts a JSON-formatted string input into a Python dictionary using `process_json`.

- `read_user_dict(var_name, default_value, prompts=None, prefix="")`:  
  Prompt the user to provide a dictionary via a JSON string. Validates that the input is a valid JSON object and returns it as a Python `dict`.

- `render_variable(env, raw, cookiecutter_dict)`:  
  Recursively render a variable (which may be a string, list, dict, or scalar) using a Jinja2 environment and the current context (`cookiecutter_dict`). Enables dynamic defaults like `{{ cookiecutter.project_name.replace(" ", "_") }}`.

- `_prompts_from_options(options)`:  
  Process a dictionary of template options (e.g., from `cookiecutter.json`) and generate user-friendly prompt labels, optionally using `title` and `description` fields for richer display.

- `prompt_choice_for_template(key, options, no_input)`:  
  Prompt the user to select a nested template from a structured options dictionary. If `no_input` is `True`, returns the first option without prompting.

- `prompt_choice_for_config(cookiecutter_dict, env, key, options, no_input, prompts=None, prefix="")`:  
  Render a list of choice options using the current context and prompt the user to select one. If `no_input` is `True`, returns the first rendered option.

- `prompt_for_config(context, no_input=False)`:  
  Interactively prompt the user for all variables defined in the template’s `cookiecutter.json`, respecting types (string, boolean, choice list, or dictionary). Uses Jinja2 rendering for dynamic defaults and supports structured prompts. Returns an `OrderedDict` of user-provided or default values.

- `choose_nested_template(context, repo_dir, no_input=False)`:  
  Handle templates that support multiple sub-templates (nested templates). Parses either the new-style `templates` structure or legacy `template` list, prompts the user to choose one (unless `no_input` is set), and returns the absolute path to the selected sub-template directory.

- `prompt_and_delete(path, no_input=False)`:  
  Ask the user whether it’s okay to delete a previously downloaded repository or archive at `path`. If deletion is confirmed, removes the file/directory. If not, asks whether to reuse the existing version; if reuse is declined, exits the program.

`replay.py`:

- `get_file_name(replay_dir, template_name)`:  
  Construct the full file path for a replay file by joining the `replay_dir` with the `template_name`, appending a `.json` suffix if not already present.

- `dump(replay_dir, template_name, context)`:  
  Write the given `context` dictionary (which must contain a `'cookiecutter'` key) to a JSON file in the specified `replay_dir` using the `template_name` as the filename base. Ensures the output directory exists before writing.

- `load(replay_dir, template_name)`:  
  Read and return the context dictionary from a replay JSON file located in `replay_dir` with a name derived from `template_name`. Validates that the loaded data contains a `'cookiecutter'` key.

`repository.py`:

- `is_repo_url(value)`:  
  Return `True` if the given `value` matches a known repository URL pattern (e.g., `git://`, `https://`, `user@host`, etc.), as defined by the `REPO_REGEX` regular expression.

- `is_zip_file(value)`:  
  Return `True` if the given `value` ends with the `.zip` extension (case-insensitive), indicating it is a ZIP archive.

- `expand_abbreviations(template, abbreviations)`:  
  Expand a template name using user-defined abbreviations. If the full template name matches an abbreviation key, it is replaced directly. If the template contains a colon (e.g., `myabbrev:path`), only the prefix before the colon is expanded and the suffix is formatted into the expanded string.

- `repository_has_cookiecutter_json(repo_directory)`:  
  Check whether the given `repo_directory` exists and contains a file named `cookiecutter.json`, which is required for a valid Cookiecutter template.

- `determine_repo_dir(template, abbreviations, clone_to_dir, checkout, no_input, password=None, directory=None)`:  
  Locate or obtain the directory containing a valid Cookiecutter template based on the `template` argument. Handles three cases:  
    1. Local directory path — used as-is.  
    2. Remote Git repository URL — cloned into `clone_to_dir`.  
    3. ZIP file (local or remote) — downloaded and extracted if needed.  
  Applies abbreviation expansion first, then searches candidate paths (including an optional sub-`directory`). Returns a tuple `(repo_dir, cleanup)`, where `cleanup` indicates whether the directory is temporary and should be removed after use. Raises `RepositoryNotFound` if no valid template is found.

`utils.py`:

- `force_delete(func, path, _exc_info)`:  
  Error handler for `shutil.rmtree()` that removes read-only attributes on Windows and retries deletion. Enables `rmtree` to behave like `rm -rf` by making files writable before removal.

- `rmtree(path)`:  
  Remove a directory and all its contents recursively, even if some files are read-only. Uses `force_delete` as the error handler to ensure robust deletion across platforms.

- `make_sure_path_exists(path)`:  
  Ensure that the specified directory path exists by creating it (and any necessary parent directories) if it doesn’t already exist. Logs the operation at debug level and raises an `OSError` if creation fails.

- `work_in(dirname)`:  
  A context manager that temporarily changes the current working directory to `dirname`. Upon exiting the context, it restores the original working directory, regardless of exceptions.

- `make_executable(script_path)`:  
  Set the executable bit on the given file (`script_path`) by modifying its file permissions using `os.chmod`. Primarily used to make hook scripts runnable on Unix-like systems.

- `simple_filter(filter_function)`:  
  A decorator that wraps a plain Python function into a Jinja2 extension, automatically registering it as a filter in the Jinja2 environment under the function’s original name.

- `create_tmp_repo_dir(repo_dir)`:  
  Create a temporary copy of the given `repo_dir` using `tempfile.mkdtemp()` and `shutil.copytree()`. Returns the path to the new temporary directory, useful for safely modifying template contents without affecting the original.

- `create_env_with_context(context)`:  
  Create and return a `StrictEnvironment` (a custom Jinja2 environment) initialized with the provided `context`. Also applies any Jinja2 environment variables specified in `context['cookiecutter']['_jinja2_env_vars']`.

`vcs.py`:

- `identify_repo(repo_url)`:  
  Determine whether the given `repo_url` refers to a Git or Mercurial (hg) repository. URLs can be explicitly prefixed with `git+` or `hg+`. If not prefixed, the function heuristically infers the type based on substrings like `'git'` or `'bitbucket'`. Returns a tuple `(repo_type, normalized_url)` or raises `UnknownRepoType` if the type cannot be determined.

- `is_vcs_installed(repo_type)`:  
  Check whether the version control system executable (e.g., `git` or `hg`) is available on the system’s PATH using `shutil.which`. Returns `True` if installed, `False` otherwise.

- `clone(repo_url, checkout=None, clone_to_dir=".", no_input=False)`:  
  Clone a remote repository (Git or Mercurial) into the specified `clone_to_dir`. If a directory with the same name already exists, prompts the user (unless `no_input=True`) to either delete and re-clone or reuse the existing directory. After cloning, optionally checks out a specific `checkout` reference (branch, tag, or commit). Handles Git and Mercurial differences (e.g., safe argument passing for `hg checkout`). Returns the absolute path to the cloned repository directory. Raises specific exceptions (`RepositoryNotFound`, `RepositoryCloneFailed`, `VCSNotInstalled`, `UnknownRepoType`) for various failure modes.

`zipfile.py`:

- `unzip(zip_uri, is_url, clone_to_dir, no_input, password)`: 
  Downloads and unpacks a zipfile from a given URI (either a URL or a local file path) into a temporary directory. If the URI is a URL, it caches the downloaded zip in the specified `clone_to_dir` and prompts for overwrite confirmation unless `no_input` is True. Handles password-protected zip archives by either using a provided password, prompting the user (up to three attempts), or raising an error in non-interactive mode. Validates that the zip contains a top-level directory and raises `InvalidZipRepository` if the archive is empty, malformed, or lacks the expected structure.