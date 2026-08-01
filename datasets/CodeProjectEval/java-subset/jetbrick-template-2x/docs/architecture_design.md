# Architecture Design

Below is a text-based representation of the file tree. 
```bash
src
    ├── main
    │   ├── antlr4
    │   │   └── jetbrick
    │   │       └── template
    │   │           └── runtime
    │   │               └── parser
    │   │                   └── grammer
    │   │                       ├── JetTemplateLexer.g4
    │   │                       └── JetTemplateParser.g4
    │   └── java
    │       └── jetbrick
    │           └── template
    │               ├── Errors.java
    │               ├── JetAnnotations.java
    │               ├── JetConfig.java
    │               ├── JetContext.java
    │               ├── JetEngineImpl.java
    │               ├── JetEngine.java
    │               ├── JetGlobalContext.java
    │               ├── JetSecurityManagerImpl.java
    │               ├── JetSecurityManager.java
    │               ├── JetTemplateImpl.java
    │               ├── JetTemplate.java
    │               ├── JetTemplateMacro.java
    │               ├── JetTemplateOption.java
    │               ├── TemplateException.java
    │               ├── loader
    │               │   ├── AbstractResourceLoader.java
    │               │   ├── ClasspathResourceLoader.java
    │               │   ├── FileSystemResourceLoader.java
    │               │   ├── resource
    │               │   │   └── SourceResource.java
    │               │   └── ResourceLoader.java
    │               ├── parser
    │               │   ├── ast
    │               │   │   ├── ALU.java
    │               │   │   ├── AstConstant.java
    │               │   │   ├── AstConstantList.java
    │               │   │   ├── AstConstantMapEntry.java
    │               │   │   ├── AstConstantMap.java
    │               │   │   ├── AstDirectiveBreak.java
    │               │   │   ├── AstDirectiveCall.java
    │               │   │   ├── AstDirectiveContinue.java
    │               │   │   ├── AstDirectiveFor.java
    │               │   │   ├── AstDirectiveIf.java
    │               │   │   ├── AstDirectiveInclude.java
    │               │   │   ├── AstDirective.java
    │               │   │   ├── AstDirectiveMacro.java
    │               │   │   ├── AstDirectiveNoop.java
    │               │   │   ├── AstDirectiveReturn.java
    │               │   │   ├── AstDirectiveSet.java
    │               │   │   ├── AstDirectiveStop.java
    │               │   │   ├── AstDirectiveTag.java
    │               │   │   ├── AstExpression.java
    │               │   │   ├── AstExpressionList.java
    │               │   │   ├── AstIdentifier.java
    │               │   │   ├── AstInvokeField.java
    │               │   │   ├── AstInvokeFieldStatic.java
    │               │   │   ├── AstInvokeFunction.java
    │               │   │   ├── AstInvokeIndexGet.java
    │               │   │   ├── AstInvokeMethod.java
    │               │   │   ├── AstInvokeMethodStatic.java
    │               │   │   ├── AstInvokeNewArray.java
    │               │   │   ├── AstInvokeNewObject.java
    │               │   │   ├── AstNode.java
    │               │   │   ├── AstOperatorBinary.java
    │               │   │   ├── AstOperatorEquals.java
    │               │   │   ├── AstOperatorInstanceof.java
    │               │   │   ├── AstOperatorNullAsDefault.java
    │               │   │   ├── AstOperatorUnary.java
    │               │   │   ├── AstStatement.java
    │               │   │   ├── AstStatementList.java
    │               │   │   ├── AstTemplate.java
    │               │   │   ├── AstTernaryOperator.java
    │               │   │   ├── AstTernarySimplifyOperator.java
    │               │   │   ├── AstText.java
    │               │   │   ├── AstType.java
    │               │   │   ├── AstValueEscaped.java
    │               │   │   ├── AstValue.java
    │               │   │   ├── Position.java
    │               │   │   └── Tokens.java
    │               │   ├── AstBuilder.java
    │               │   ├── AstCodeVisitor.java
    │               │   ├── ParserContext.java
    │               │   ├── Source.java
    │               │   ├── Symbols.java
    │               │   └── SyntaxException.java
    │               ├── resolver
    │               │   ├── clazz
    │               │   │   └── ClassResolver.java
    │               │   ├── function
    │               │   │   ├── ExtensionFunctionInvoker.java
    │               │   │   ├── FunctionInvoker.java
    │               │   │   └── FunctionInvokerResolver.java
    │               │   ├── GlobalResolver.java
    │               │   ├── macro
    │               │   │   └── MacroResolver.java
    │               │   ├── method
    │               │   │   ├── ClassBuildinMethodInvoker.java
    │               │   │   ├── ExtensionMethodInvoker.java
    │               │   │   ├── MethodInvoker.java
    │               │   │   └── MethodInvokerResolver.java
    │               │   ├── ParameterUtils.java
    │               │   ├── property
    │               │   │   ├── ArrayLengthGetter.java
    │               │   │   ├── DefaultGetterResolver.java
    │               │   │   ├── FieldGetter.java
    │               │   │   ├── Getter.java
    │               │   │   ├── GetterResolver.java
    │               │   │   ├── MapGetter.java
    │               │   │   └── PropertyGetter.java
    │               │   ├── SignatureUtils.java
    │               │   └── tag
    │               │       ├── TagInvoker.java
    │               │       └── TagInvokerResolver.java
    │               ├── runtime
    │               │   ├── buildin
    │               │   │   ├── JetFunctions.java
    │               │   │   ├── JetMethods.java
    │               │   │   └── JetTags.java
    │               │   ├── InterpretContextImpl.java
    │               │   ├── InterpretContext.java
    │               │   ├── InterpretException.java
    │               │   ├── JetForIterator.java
    │               │   ├── JetTagContext.java
    │               │   ├── JetWriter.java
    │               │   ├── OriginalStream.java
    │               │   ├── TemplateStack.java
    │               │   ├── ValueContext.java
    │               │   ├── ValueStack.java
    │               │   └── writer
    │               │       ├── JetOutputStreamPrinterEx.java
    │               │       ├── JetOutputStreamPrinter.java
    │               │       ├── JetWriterPrinterEx.java
    │               │       ├── JetWriterPrinter.java
    │               │       ├── TrimLeadingWhitespacesOutputStream.java
    │               │       └── TrimLeadingWhitespacesWriter.java

```

`JetEngine.java`:

- `JetEngine`: The abstract base class representing the template engine, serving as the main entry point for creating and managing different template contexts and configurations.

  - `create() -> JetEngine`: Creates a `JetEngine` instance using the default configuration file `classpath:/jetbrick-template.properties`.

  - `create(configLocation: String) -> JetEngine`: Creates a `JetEngine` instance using a specified configuration file path.

  - `create(config: Properties) -> JetEngine`: Creates a `JetEngine` instance using a provided `Properties` object for configuration.

  - `create(defaultConfig: Properties, configLocation: String) -> JetEngine`: Creates a `JetEngine` instance using both default properties and a specific configuration file, where the file location takes precedence.

  - `getConfig() -> JetConfig`: Retrieves the global configuration information associated with this engine.

  - `getGlobalContext() -> JetGlobalContext`: Retrieves the global context which holds variables accessible across all templates.

  - `getGlobalResolver() -> GlobalResolver`: Retrieves the global resolver used for resolving methods, functions, and tags.

  - `checkTemplate(name: String) -> boolean`: Checks if a template with the given name exists.

  - `getTemplate(name: String) -> JetTemplate`: Retrieves a `JetTemplate` object by its name. Throws `ResourceNotFoundException` if not found.

  - `createTemplate(source: String) -> JetTemplate`: Creates a new `JetTemplate` from a raw source string with no caching.

  - `createTemplate(name: String, source: String) -> JetTemplate`: Creates a new `JetTemplate` from a raw source string, identified by a given name.

  - `getResource(name: String) -> Resource`: Retrieves a `Resource` object by name. Throws `ResourceNotFoundException` if unavailable.


`JetEngineImpl.java`:

- `JetEngineImpl`: The default final implementation of `JetEngine`, handling the lifecycle of templates, resources, and global contexts.

  - `JetEngineImpl(config: JetConfig) -> JetEngineImpl`: Initializes the engine with the provided configuration, setting up resource loaders, global resolvers, and loading global macros.

  - `getConfig() -> JetConfig`: Returns the associated `JetConfig` object.

  - `getGlobalContext() -> JetGlobalContext`: Returns the `JetGlobalContext` instance.

  - `getGlobalResolver() -> GlobalResolver`: Returns the `GlobalResolver` instance.

  - `checkTemplate(name: String) -> boolean`: Verifies the existence of a template by checking its internal retrieval status.

  - `getTemplate(name: String) -> JetTemplate`: Retrieves a specific template by name, ensuring it is reloaded if modifications are detected.

  - `createTemplate(source: String) -> JetTemplate`: Creates a template from a source string using a default name.

  - `createTemplate(name: String, source: String) -> JetTemplate`: Creates a formatted source resource and initializes a `JetTemplateImpl` from it.

  - `internalGetTemplate(name: String) -> JetTemplate`: Internal helper to find a template in the cache or load it via configured resource loaders.

  - `getResource(name: String) -> Resource`: Iterates through available resource loaders to find the specified resource.

  - `doCreateGlobalResolver() -> GlobalResolver`: Internal method to initialize and configure the `GlobalResolver` with imports and auto-scanned packages.

  - `doCreateGlobalContext() -> JetGlobalContext`: Internal method to initialize the `JetGlobalContext`, defining global types and objects.

  - `doLoadGlobalMacroFiles() -> void`: Internal method to load global macro files as defined in the configuration.


`GlobalResolver.java`:

- `GlobalResolver`: Responsible for resolving classes, methods, functions, tags, and macros within the template engine.

  - `scan(packageNames: List<String>, skipErrors: boolean) -> void`: Scans packages for annotated components (@JetMethods, @JetFunctions, @JetTags).

  - `importClass(name: String) -> void`: Registers a class import.

  - `registerGetterResolver(resolver: GetterResolver) -> void`: Registers a custom property getter resolver.

  - `registerMethods(className: String) -> void`: Registers static method extensions from a class name.

  - `registerMethods(cls: Class<?>) -> void`: Registers static method extensions from a class.

  - `registerMethod(method: MethodInfo) -> void`: Registers a specific method extension.

  - `registerFunctions(className: String) -> void`: Registers functions from a class name.

  - `registerFunctions(cls: Class<?>) -> void`: Registers functions from a class.

  - `registerFunction(method: MethodInfo) -> void`: Registers a specific function.

  - `registerTags(className: String) -> void`: Registers tags from a class name.

  - `registerTags(cls: Class<?>) -> void`: Registers tags from a class.

  - `registerTag(method: MethodInfo) -> void`: Registers a specific tag.

  - `registerMacros(template: JetTemplate) -> void`: Registers global macros defined in a template.

  - `resolveClass(name: String) -> Class<?>`: Resolves a class by name (handling imports).

  - `resolveMethod(clazz: Class<?>, name: String, argumentTypes: Class<?>[], isStatic: boolean) -> MethodInvoker`: Resolves a method invoker.

  - `resolveFunction(name: String, argumentTypes: Class<?>[]) -> FunctionInvoker`: Resolves a function invoker.

  - `resolveTag(name: String, argumentTypes: Class<?>[]) -> TagInvoker`: Resolves a tag invoker.

  - `resolveMacro(name: String, argumentTypes: Class<?>[], reloadable: boolean) -> JetTemplateMacro`: Resolves a macro.

  - `resolveGetter(objectClass: Class<?>, name: String) -> Getter`: Resolves a property getter.


`JetTemplate.java`:

- `JetTemplate`: An interface representing a compiled template file, capable of rendering output to a writer or stream.

  - `reload() -> void`: Reloads the template content if it has been modified and the template is reloadable.

  - `render(context: Map<String, Object>, out: Writer) -> void`: Renders the template using the provided context map and writes the result to a `Writer`.

  - `render(context: Map<String, Object>, out: OutputStream) -> void`: Renders the template using the provided context map and writes the result to an `OutputStream`.

  - `resolveMacro(name: String, argumentTypes: Class<?>[], root: boolean) -> JetTemplateMacro`: Resolves a macro within the template by name and argument types.

  - `getName() -> String`: Returns the name of the template.

  - `getSource() -> Source`: Returns the source code object associated with the template.

  - `isReloadable() -> boolean`: Checks if the template supports reloading.

  - `getLastModified() -> long`: Returns the timestamp of when the template was last modified.

  - `getOption() -> JetTemplateOption`: Retrieves the configuration options specific to this template.

  - `getAstNode() -> AstTemplate`: Returns the Abstract Syntax Tree (AST) root node of the template.

  - `getEngine() -> JetEngine`: Returns the `JetEngine` instance that created this template.

  - `getSecurityManager() -> JetSecurityManager`: Returns the security manager associated with the template.


`JetTemplateImpl.java`:

- `JetTemplateImpl`: The final implementation of `JetTemplate`, managing the parsing, AST generation, and execution of the template.

  - `JetTemplateImpl(engine: JetEngine, resource: Resource, reloadable: boolean, securityManager: JetSecurityManager) -> JetTemplateImpl`: Constructs a new template instance, initializing its configuration and macro resolver.

  - `reload() -> void`: Checks the resource's last modified time and rebuilds the AST if changes are detected.

  - `rebuildAstNodeAndConfig() -> void`: Internal method to parse the source code, generate the AST, and configure template options.

  - `render(context: Map<String, Object>, out: Writer) -> void`: Creates a `JetWriter` and initiates the interpretation process.

  - `render(context: Map<String, Object>, out: OutputStream) -> void`: Creates a `JetWriter` for the output stream and initiates interpretation.

  - `doInterpret(context: Map<String, Object>, writer: JetWriter) -> void`: Internal method setting up the `InterpretContext` and executing the AST within a thread-safe environment.

  - `resolveMacro(name: String, argumentTypes: Class<?>[], root: boolean) -> JetTemplateMacro`: Resolves macros from local definitions or delegates to the global resolver.

  - `getName() -> String`: Returns the relative path name of the resource.

  - `getSource() -> Source`: Returns the parsed source object.

  - `isReloadable() -> boolean`: Returns the reloadable status.

  - `getLastModified() -> long`: Returns the last modified timestamp.

  - `getOption() -> JetTemplateOption`: Returns the current template options.

  - `getAstNode() -> AstTemplate`: Returns the root AST node.

  - `getEngine() -> JetEngine`: Returns the parent engine instance.

  - `getSecurityManager() -> JetSecurityManager`: Returns the configured security manager.

  - `toString() -> String`: Returns the template name.


`JetTemplateMacro.java`:

- `JetTemplateMacro`: Represents a defined macro in a template, implementing `FunctionInvoker`.

  - `getTemplate() -> JetTemplate`: Returns the template where this macro is defined.

  - `getAstNode() -> AstDirectiveMacro`: Returns the AST node of the macro definition.

  - `getName() -> String`: Returns the macro name.

  - `getArgumentNames() -> List<String>`: Returns the list of argument names.

  - `getSymbols() -> Map<String, Class<?>>`: Returns the local variable symbols defined in the macro.

  - `checkAccess(securityManager: JetSecurityManager) -> void`: Checks if access to this macro is allowed.

  - `invoke(arguments: Object[]) -> Object`: Executes the macro with the provided arguments.

  - `getSignature() -> String`: Returns the signature of the macro.


`JetTemplateOption.java`:

- `JetTemplateOption`: Runtime options for a specific template.

  - `isStrict() -> boolean`: Indicates if strict mode is enabled.

  - `isSafecall() -> boolean`: Indicates if safe calls are enabled.

  - `isTrimLeadingWhitespaces() -> boolean`: Indicates if leading whitespaces should be trimmed.

  - `getSymbols() -> Map<String, Class<?>>`: Returns the variables defined in the template.


`Source.java`:

- `Source`: Represents the source code of a template.

  - `getFilename() -> String`: Returns the filename of the source.

  - `getContents() -> char[]`: Returns the content characters.

  - `getLines() -> String[]`: Returns the content split by lines.


`AstBuilder.java`:

- `AstBuilder`: Responsible for converting template source code into an AST (Abstract Syntax Tree).

  - `create(source: Source, ctx: ParserContext) -> AstTemplate`: Parses the source using ANTLR and visits the tree to generate the AST.


`ParserContext.java`:

- `ParserContext`: Holds configuration and state during the parsing process.

  - `ParserContext(globalResolver: GlobalResolver, globalContext: JetGlobalContext) -> ParserContext`: Initializes the parser context.

  - `isStrict() / setStrict(boolean) -> boolean / void`: strict mode accessor.

  - `isSafecall() / setSafecall(boolean) -> boolean / void`: safecall mode accessor.

  - `isTrimLeadingWhitespaces() / setTrimLeadingWhitespaces(boolean) -> boolean / void`: trimLeadingWhitespaces accessor.

  - `isTrimDirectiveWhitespaces() / setTrimDirectiveWhitespaces(boolean) -> boolean / void`: trimDirectiveWhitespaces accessor.

  - `isTrimDirectiveComments() / setTrimDirectiveComments(boolean) -> boolean / void`: trimDirectiveComments accessor.

  - `getTrimDirectiveCommentsPrefix() / setTrimDirectiveCommentsPrefix(String) -> String / void`: trimDirectiveCommentsPrefix accessors.

  - `getTrimDirectiveCommentsSuffix() / setTrimDirectiveCommentsSuffix(String) -> String / void`: trimDirectiveCommentsSuffix accessors.

  - `isNullSafe() / setNullSafe(boolean) -> boolean / void`: nullSafe accessor.

  - `importClass(name: String) -> void`: Imports a class for the current compilation unit.

  - `resolveClass(className: String) -> Class<?>`: Resolves a class name.

  - `enterMacros() -> void`: Prepares for parsing macro arguments.

  - `exitMacros() -> void`: Cleans up after parsing macro arguments.

  - `defineSymbol(name: String, type: Class<?>) -> void`: Defines a variable symbol in the current scope.

  - `useSymbol(name: String) -> void`: Marks a symbol as used.

  - `getSymbols() -> Map<String, Class<?>>`: Returns the current defined symbols.

  - `getMacroArgumentNames() -> List<String>`: Returns argument names for the macro being parsed.

  - `loadMacroFile(file: String) -> void`: Records a macro file to load.

  - `defineMacro(macro: AstDirectiveMacro) -> void`: Records a defined macro.

  - `getLoadMacroFiles() -> List<String>`: Returns the list of macro files to load.

  - `getDeclaredMacros() -> List<AstDirectiveMacro>`: Returns the list of macros defined in the source.


`JetContext.java`:

- `JetContext`: A specialization of `HashMap<String, Object>` representing the context for template variables.

  - `JetContext() -> JetContext`: Constructs an empty context.

  - `JetContext(initialCapacity: int) -> JetContext`: Constructs a context with a specified initial capacity.

  - `get(name: String) -> Object`: Retrieves a variable value by name.

  - `set(name: String, value: Object) -> void`: Sets a variable value in the context.


`JetConfig.java`:

- `JetConfig`: Manages configuration settings for the template engine, loading properties from files or objects.

  - `JetConfig(config: Properties, configLocation: String) -> JetConfig`: Initializes configuration by loading from a `Properties` object and/or a specific file location.

  - `initialize(config: Config) -> void`: Internal method to process and assign configuration values to fields.

  - `getImportClasses() -> List<String>`: Returns a list of classes to be imported.

  - `getImportMethods() -> List<String>`: Returns a list of classes/packages containing static methods to be imported.

  - `getImportFunctions() -> List<String>`: Returns a list of registered functions.

  - `getImportTags() -> List<String>`: Returns a list of registered tags.

  - `getImportMacros() -> List<String>`: Returns a list of global macro files.

  - `getImportDefines() -> List<String>`: Returns a list of global definitions.

  - `getAutoscanPackages() -> List<String>`: Returns packages to auto-scan for components.

  - `isAutoscanSkiperrors() -> boolean`: Indicates if errors during auto-scanning should be skipped.

  - `getTemplateLoaders() -> List<ResourceLoader>`: Returns the list of configured resource loaders.

  - `getTemplateSuffix() -> String`: Returns the default template file suffix.

  - `getTemplateSecurityManager() -> JetSecurityManager`: Returns the security manager class.

  - `getInputEncoding() -> Charset`: Returns the character set for reading templates.

  - `getOutputEncoding() -> Charset`: Returns the character set for writing output.

  - `isSyntaxStrict() -> boolean`: Indicates if strict syntax mode is enabled.

  - `isSyntaxSafecall() -> boolean`: Indicates if safe calls (ignoring nulls) are enabled.

  - `isTrimLeadingWhitespaces() -> boolean`: Indicates if leading whitespaces should be trimmed.

  - `isTrimDirectiveWhitespaces() -> boolean`: Indicates if directive whitespaces should be trimmed.

  - `isTrimDirectiveComments() -> boolean`: Indicates if directive comments should be trimmed.

  - `getTrimDirectiveCommentsPrefix() -> String`: Returns the prefix for trimming directive comments.

  - `getTrimDirectiveCommentsSuffix() -> String`: Returns the suffix for trimming directive comments.

  - `isIoSkiperrors() -> boolean`: Indicates if I/O errors should be ignored during output.


`JetGlobalContext.java`:

- `JetGlobalContext`: Manages global variables and type definitions available to all templates.

  - `JetGlobalContext() -> JetGlobalContext`: Initializes the global symbol and context maps.

  - `define(type: Class<?>, name: String) -> void`: Defines a globally accessible type with a specific name.

  - `set(type: Class<?>, name: String, value: Object) -> void`: Defines a type and sets its global value simultaneously.

  - `set(name: String, value: Object) -> void`: Sets a global variable's value, enforcing type consistency if already defined.

  - `getType(name: String) -> Class<?>`: Retrieves the class type of a defined global symbol.

  - `getValue(name: String) -> Object`: Retrieves the value of a global variable.


`ResourceLoader.java`:

- `ResourceLoader`: An interface for loading template resources from various sources (classpath, file system, etc.).

  - `getRoot() -> String`: Returns the root path used by this loader.

  - `isReloadable() -> boolean`: Indicates whether resources loaded by this loader support hot reloading.

  - `load(name: String) -> Resource`: Loads and returns a `Resource` object for the given name, or `null` if not found.

  - `getSecurityManager() -> JetSecurityManager`: Retrieves the security manager associated with this loader.


`JetSecurityManager.java`:

- `JetSecurityManager`: An interface for implementing security checks on class, method, and field access within templates.

  - `checkAccess(cls: Class<?>) -> void`: Checks if access to the specified class is allowed.

  - `checkAccess(constructor: Constructor<?>) -> void`: Checks if access to the specified constructor is allowed.

  - `checkAccess(method: Method) -> void`: Checks if access to the specified method is allowed.

  - `checkAccess(field: Field) -> void`: Checks if access to the specified field is allowed.


`JetSecurityManagerImpl.java`:

- `JetSecurityManagerImpl`: The default implementation of `JetSecurityManager`.

  - `setConfigFile(configFile: String) -> void`: Loads security configuration from a file.

  - `setNameList(nameList: List<String>) -> void`: Loads security configuration from a list of strings.

  - `setDisallowConstructor(disallowConstructor: boolean) -> void`: Sets whether to disallow all constructor calls.

  - `setDisallowStaticMethod(disallowStaticMethod: boolean) -> void`: Sets whether to disallow all static method calls.

  - `setDisallowStaticField(disallowStaticField: boolean) -> void`: Sets whether to disallow all static field access.

  - `checkAccess(cls: Class<?>) -> void`: Checking whether the class access is allowed.

  - `checkAccess(constructor: Constructor<?>) -> void`: Checking whether the constructor access is allowed.

  - `checkAccess(method: Method) -> void`: Checking whether the method access is allowed.

  - `checkAccess(field: Field) -> void`: Checking whether the field access is allowed.


`InterpretContext.java`:

- `InterpretContext`: An abstract class defining the execution context for the template interpreter.

  - `current() -> InterpretContext`: Returns the current thread-local interpret context.

  - `getEngine() -> JetEngine`: Returns the current engine instance.

  - `getGlobalResolver() -> GlobalResolver`: Returns the global resolver.

  - `getSecurityManager() -> JetSecurityManager`: Returns the security manager.

  - `getTemplateStack() -> TemplateStack`: Returns the stack of templates currently being processed (for includes/macros).

  - `getValueStack() -> ValueStack`: Returns the stack of variable values (local scopes).

  - `getTemplate() -> JetTemplate`: Returns the currently executing template.

  - `getSource() -> Source`: Returns the source of the current template.

  - `getWriter() -> JetWriter`: Returns the writer used for output.

  - `setWriter(writer: JetWriter) -> void`: updates the current writer.

  - `getSignal() -> int`: Returns the current flow control signal (e.g., break, continue).

  - `setSignal(signal: int) -> void`: Sets the flow control signal.

  - `getReturnName() -> String`: Returns the name associated with a return signal.

  - `doIncludeCall(file: String, arguments: Map<String, Object>, returnName: String) -> void`: Executes an include directive.

  - `doMacroCall(macro: JetTemplateMacro, arguments: Object[]) -> void`: Executes a macro call.


`InterpretContextImpl.java`:

- `InterpretContextImpl`: The concrete implementation of `InterpretContext`.

  - `InterpretContextImpl(engine: JetEngine, writer: JetWriter, context: Map<String, Object>, securityManager: JetSecurityManager) -> InterpretContextImpl`: Initializes the context.

  - `setThreadLocal() -> void`: Binds this context to the current thread.

  - `freeThreadLocal() -> void`: Removes this context from the current thread.

  - `getEngine() -> JetEngine`: Returns the engine instance.

  - `getGlobalResolver() -> GlobalResolver`: Returns the global resolver.

  - `getSecurityManager() -> JetSecurityManager`: Returns the security manager.

  - `getTemplateStack() -> TemplateStack`: Returns the template stack.

  - `getValueStack() -> ValueStack`: Returns the value stack.

  - `getTemplate() -> JetTemplate`: Returns the current template from stack.

  - `getSource() -> Source`: Returns the current source from stack.

  - `getWriter() -> JetWriter`: Returns the current writer.

  - `setWriter(writer: JetWriter) -> void`: Sets the current writer.

  - `getSignal() -> int`: Returns the current signal.

  - `setSignal(signal: int) -> void`: Sets the current signal.

  - `getReturnName() -> String`: Returns the return name.

  - `doIncludeCall(file: String, arguments: Map<String, Object>, returnName: String) -> void`: Handles an `#include` directive call.

  - `doMacroCall(macro: JetTemplateMacro, arguments: Object[]) -> void`: Handles a macro call.


`JetWriter.java`:

- `JetWriter`: An abstract class wrapper for output streams or writers, providing optimized printing and error handling.

  - `create(os: Writer, charset: Charset, trimLeadingWhitespaces: boolean, skipErrors: boolean) -> JetWriter`: Factory method to create a `JetWriter` for a `Writer`.

  - `create(os: OutputStream, charset: Charset, trimLeadingWhitespaces: boolean, skipErrors: boolean) -> JetWriter`: Factory method to create a `JetWriter` for an `OutputStream`.

  - `create(os: JetWriter, trimLeadingWhitespaces: boolean) -> JetWriter`: Factory method to wrap an existing `JetWriter` with whitespace trimming capability.

  - `getOriginStream() -> Object`: Returns the underlying stream or writer.

  - `isStreaming() -> boolean`: Returns true if the underlying output is an `OutputStream`.

  - `getCharset() -> Charset`: Returns the character set used by the writer.

  - `isSkipErrors() -> boolean`: Indicates if I/O errors are suppressed.

  - `print(x: int) -> void`: Writes an integer.

  - `print(x: byte[]) -> void`: Writes a byte array.

  - `print(x: byte[], offset: int, length: int) -> void`: Writes a portion of a byte array.

  - `print(x: char[]) -> void`: Writes a char array.

  - `print(x: char[], offset: int, length: int) -> void`: Writes a portion of a char array.

  - `print(x: String) -> void`: Writes a string.

  - `flush() -> void`: Flushes the stream.

  - `close() -> void`: Closes the stream.
