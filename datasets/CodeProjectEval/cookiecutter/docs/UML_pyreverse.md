## UML Class Diagram

```mermaid
classDiagram
  class ExtensionLoaderMixin {
  }
  class StrictEnvironment {
    loader : FileSystemLoader
  }
  class ConfigDoesNotExistException {
  }
  class ContextDecodingException {
  }
  class CookiecutterException {
  }
  class EmptyDirNameException {
  }
  class FailedHookException {
  }
  class InvalidConfiguration {
  }
  class InvalidModeException {
  }
  class InvalidZipRepository {
  }
  class MissingProjectDir {
  }
  class NonTemplatedInputDirException {
  }
  class OutputDirExistsException {
  }
  class RepositoryCloneFailed {
  }
  class RepositoryNotFound {
  }
  class UndefinedVariableInTemplate {
    context : dict[str, Any]
    error : TemplateError
    message : str
  }
  class UnknownExtension {
  }
  class UnknownRepoType {
  }
  class UnknownTemplateDirException {
  }
  class VCSNotInstalled {
  }
  class JsonifyExtension {
  }
  class RandomStringExtension {
  }
  class SlugifyExtension {
  }
  class TimeExtension {
    tags : set
    parse(parser: Parser) nodes.Output
  }
  class UUIDExtension {
  }
  class _patch_import_path_for_repo {
  }
  class JsonPrompt {
    default : NoneType
    response_type : dict
    validate_error_message : str
    process_response(value: str) dict[str, Any]
  }
  class YesNoPrompt {
    no_choices : list
    yes_choices : list
    process_response(value: str) bool
  }
  class SimpleFilterExtension {
  }
  StrictEnvironment --|> ExtensionLoaderMixin
  ConfigDoesNotExistException --|> CookiecutterException
  ContextDecodingException --|> CookiecutterException
  EmptyDirNameException --|> CookiecutterException
  FailedHookException --|> CookiecutterException
  InvalidConfiguration --|> CookiecutterException
  InvalidModeException --|> CookiecutterException
  InvalidZipRepository --|> CookiecutterException
  MissingProjectDir --|> CookiecutterException
  NonTemplatedInputDirException --|> CookiecutterException
  OutputDirExistsException --|> CookiecutterException
  RepositoryCloneFailed --|> CookiecutterException
  RepositoryNotFound --|> CookiecutterException
  UndefinedVariableInTemplate --|> CookiecutterException
  UnknownExtension --|> CookiecutterException
  UnknownRepoType --|> CookiecutterException
  UnknownTemplateDirException --|> CookiecutterException
  VCSNotInstalled --|> CookiecutterException
```

## UML Package Diagram

```mermaid
classDiagram
  class cookiecutter {
  }
  class __main__ {
  }
  class cli {
  }
  class config {
  }
  class environment {
  }
  class exceptions {
  }
  class extensions {
  }
  class find {
  }
  class generate {
  }
  class hooks {
  }
  class log {
  }
  class main {
  }
  class prompt {
  }
  class replay {
  }
  class repository {
  }
  class utils {
  }
  class vcs {
  }
  class zipfile {
  }
  __main__ --> cli
  cli --> cookiecutter
  cli --> config
  cli --> exceptions
  cli --> log
  cli --> main
  config --> exceptions
  environment --> exceptions
  find --> exceptions
  generate --> exceptions
  generate --> find
  generate --> hooks
  generate --> prompt
  generate --> utils
  hooks --> cookiecutter
  hooks --> exceptions
  hooks --> utils
  main --> config
  main --> exceptions
  main --> generate
  main --> hooks
  main --> prompt
  main --> replay
  main --> repository
  main --> utils
  prompt --> exceptions
  prompt --> utils
  replay --> utils
  repository --> exceptions
  repository --> vcs
  repository --> zipfile
  utils --> environment
  vcs --> exceptions
  vcs --> prompt
  vcs --> utils
  zipfile --> exceptions
  zipfile --> prompt
  zipfile --> utils
  zipfile --> zipfile
```
