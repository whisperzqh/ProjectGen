## UML Class Diagram

```mermaid
classDiagram
    class CLI {
        +main(template, extra_context, no_input, ...)
        -configure_logger()
        -list_installed_templates()
    }
    
    class Main {
        +cookiecutter(template, checkout, no_input, ...)
        -_patch_import_path_for_repo()
    }
    
    class Generate {
        +generate_files(repo_dir, context, ...)
        +generate_file(project_dir, infile, context, ...)
        +generate_context(context_file, default_context, ...)
        +is_copy_only_path(path, context)
        -render_and_create_dir()
    }
    
    class Prompt {
        +prompt_for_config(context, no_input)
        +read_user_variable(var_name, default_value, ...)
        +read_user_choice(var_name, options, ...)
        +read_user_yes_no(var_name, default_value, ...)
        +read_user_dict(var_name, default_value, ...)
        +render_variable(env, raw, cookiecutter_dict)
        +choose_nested_template(context, repo_dir, no_input)
    }
    
    class Hooks {
        +run_hook_from_repo_dir(repo_dir, hook_name, ...)
        +run_hook(script_path, cwd, context)
        +find_hook(hook_name, hooks_dir)
        +valid_hook(hook_file, hook_name)
        -run_script()
        -run_script_with_context()
    }
    
    class Config {
        +get_user_config(config_file, default_config)
        +get_config(config_path)
        -merge_configs()
    }
    
    class Repository {
        +determine_repo_dir(template, abbreviations, ...)
        +expand_abbreviations(template, config_dict)
        +is_repo_url(value)
        +is_zip_file(value)
    }
    
    class VCS {
        +clone(repo_url, checkout, clone_to_dir, ...)
        +identify_repo(repo_url)
        +is_vcs_installed(repo_type)
    }
    
    class Replay {
        +dump(replay_dir, template_name, context)
        +load(replay_dir, template_name)
    }
    
    class Environment {
        +StrictEnvironment
        +create_env_with_context(context)
    }
    
    class Extensions {
        <<interface>>
        +JsonifyExtension
        +RandomStringExtension
        +SlugifyExtension
        +UUIDExtension
        +TimeExtension
    }
    
    CLI --> Main : calls
    Main --> Config : uses
    Main --> Repository : uses
    Main --> Prompt : uses
    Main --> Generate : uses
    Main --> Replay : uses
    Main --> Hooks : uses
    Generate --> Hooks : executes
    Generate --> Environment : uses
    Environment --> Extensions : loads
    Repository --> VCS : uses
    Prompt --> Environment : uses
```

## UML Package Diagram

```mermaid
graph TD
    CLI["cli.py"]
    Main["main.py"]
    Generate["generate.py"]
    Prompt["prompt.py"]
    Hooks["hooks.py"]
    Config["config.py"]
    Repository["repository.py"]
    VCS["vcs.py"]
    Replay["replay.py"]
    Environment["environment.py"]
    Extensions["extensions.py"]
    Utils["utils.py"]
    Exceptions["exceptions.py"]
    
    CLI --> Main
    Main --> Config
    Main --> Repository
    Main --> Generate
    Main --> Prompt
    Main --> Replay
    Main --> Hooks
    Main --> Utils
    Main --> Exceptions
    
    Generate --> Hooks
    Generate --> Environment
    Generate --> Utils
    Generate --> Exceptions
    
    Prompt --> Environment
    Prompt --> Utils
    Prompt --> Exceptions
    
    Repository --> VCS
    Repository --> Utils
    Repository --> Exceptions
    
    Environment --> Extensions
    
    Hooks --> Utils
    Hooks --> Exceptions
```

## UML Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant CLI as "CLI (cli.py)"
    participant Main as "Main (main.py)"
    participant Config as "Config"
    participant Repo as "Repository"
    participant Hooks as "Hooks"
    participant Context as "Generate Context"
    participant Prompt as "Prompt"
    participant Gen as "Generate Files"
    participant Replay as "Replay"
    
    User->>CLI: cookiecutter template [options]
    CLI->>CLI: configure_logger()
    CLI->>Main: cookiecutter(template, **kwargs)
    
    Main->>Main: validate parameters
    Main->>Config: get_user_config()
    Config-->>Main: config_dict
    
    Main->>Repo: determine_repo_dir(template)
    Repo->>Repo: check if local/url/zip
    Repo-->>Main: repo_dir, cleanup
    
    alt accept_hooks is True
        Main->>Hooks: run_pre_prompt_hook(repo_dir)
        Hooks->>Hooks: find_hook("pre_prompt")
        Hooks->>Hooks: run_hook()
        Hooks-->>Main: hook result
    end
    
    alt replay mode
        Main->>Replay: load(replay_dir, template_name)
        Replay-->>Main: context_from_replay
    end
    
    Main->>Context: generate_context(context_file, ...)
    Context-->>Main: context_dict
    
    alt no_input is False
        Main->>Prompt: prompt_for_config(context)
        loop for each variable
            Prompt->>User: prompt for value
            User-->>Prompt: user input
        end
        Prompt-->>Main: updated_context
    end
    
    Main->>Main: enrich context with metadata
    
    Main->>Replay: dump(replay_dir, template_name, context)
    
    Main->>Gen: generate_files(repo_dir, context, ...)
    
    alt accept_hooks is True
        Gen->>Hooks: run_hook_from_repo_dir("pre_gen_project")
        Hooks-->>Gen: hook result
    end
    
    Gen->>Gen: process template files
    loop for each file
        Gen->>Gen: render template with context
        Gen->>Gen: write to output directory
    end
    
    alt accept_hooks is True
        Gen->>Hooks: run_hook_from_repo_dir("post_gen_project")
        Hooks-->>Gen: hook result
    end
    
    Gen-->>Main: project_dir
    
    alt cleanup needed
        Main->>Main: rmtree(repo_dir)
    end
    
    Main-->>CLI: project_dir
    CLI-->>User: "Project generated successfully"
```
