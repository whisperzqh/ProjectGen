# Architecture Design

Below is a text-based representation of the file tree.
```bash
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── google
    │               └── testing
    │                   └── compile
    │                       ├── Breadcrumbs.java
    │                       ├── Compilation.java
    │                       ├── CompilationFailureException.java
    │                       ├── CompilationRule.java
    │                       ├── CompilationSubject.java
    │                       ├── CompilationSubjectFactory.java
    │                       ├── Compiler.java
    │                       ├── CompileTester.java
    │                       ├── ForwardingStandardJavaFileManager.java
    │                       ├── InMemoryJavaFileManager.java
    │                       ├── JavaFileObjects.java
    │                       ├── JavaFileObjectSubject.java
    │                       ├── JavaFileObjectSubjectFactory.java
    │                       ├── JavaSourcesSubject.java
    │                       ├── JavaSourcesSubjectFactory.java
    │                       ├── JavaSourceSubjectFactory.java
    │                       ├── MoreTrees.java
    │                       ├── package-info.java
    │                       ├── Parser.java
    │                       ├── ProcessedCompileTesterFactory.java
    │                       ├── TreeContext.java
    │                       ├── TreeDiffer.java
    │                       ├── TreeDifference.java
    │                       └── TypeEnumerator.java
```

---

`Breadcrumbs.java`:

- `Breadcrumbs`: Utility class for providing breadcrumb strings describing the contents of a TreePath.

  - `Breadcrumbs() -> Breadcrumbs`: Private constructor preventing instantiation.

  - `describeTreePath(path: TreePath) -> String`: Returns a string describing the given TreePath by joining breadcrumb components with "->".

  - `getBreadcrumbList(path: TreePath) -> List<String>`: Returns a list of breadcrumb strings describing the TreePath in reverse order.

- `Breadcrumbs.BreadcrumbVisitor`: A SimpleTreeVisitor for providing breadcrumb strings for Tree nodes.

  - `BreadcrumbVisitor() -> BreadcrumbVisitor`: Package-private constructor.

  - `kindString(t: Tree) -> String`: Returns a string describing the Tree.Kind of the given Tree.

  - `detailedKindString(t: Tree, detail: Object) -> String`: Returns a string describing the Tree.Kind with additional detail information.

  - `defaultAction(t: Tree, v: Void) -> String`: Returns the kind string for the tree, or empty string if null.

  - `visitBlock(reference: BlockTree, v: Void) -> String`: Returns detailed kind string indicating whether the block is static or non-static.

  - `visitBreak(reference: BreakTree, v: Void) -> String`: Returns detailed kind string with the break label.

  - `visitClass(reference: ClassTree, v: Void) -> String`: Returns detailed kind string with the class simple name.

  - `visitContinue(reference: ContinueTree, v: Void) -> String`: Returns detailed kind string with the continue label.

  - `visitIdentifier(reference: IdentifierTree, v: Void) -> String`: Returns detailed kind string with the identifier name.

  - `visitImport(reference: ImportTree, v: Void) -> String`: Returns detailed kind string indicating whether import is static or non-static.

  - `visitLabeledStatement(reference: LabeledStatementTree, v: Void) -> String`: Returns detailed kind string with the statement label.

  - `visitLiteral(reference: LiteralTree, v: Void) -> String`: Returns detailed kind string with the literal value.

  - `visitMethod(reference: MethodTree, v: Void) -> String`: Returns detailed kind string with the method name.

  - `visitModifiers(reference: ModifiersTree, v: Void) -> String`: Returns detailed kind string with the modifier flags.

  - `visitMemberSelect(reference: MemberSelectTree, v: Void) -> String`: Returns detailed kind string with the selected member identifier.

  - `visitPrimitiveType(reference: PrimitiveTypeTree, v: Void) -> String`: Returns detailed kind string with the primitive type kind.

  - `visitTypeParameter(reference: TypeParameterTree, v: Void) -> String`: Returns detailed kind string with the type parameter name.

  - `visitVariable(reference: VariableTree, v: Void) -> String`: Returns detailed kind string with the variable name.

---

`Compilation.java`:

- `Compilation`: Represents the results of compiling source files, including diagnostics and generated files.

  - `Compilation(compiler: Compiler, sourceFiles: Iterable<? extends JavaFileObject>, successful: boolean, diagnostics: Iterable<Diagnostic<? extends JavaFileObject>>, generatedFiles: Iterable<JavaFileObject>) -> Compilation`: Package-private constructor initializing compilation results.

  - `compiler() -> Compiler`: Returns the compiler used for this compilation.

  - `sourceFiles() -> ImmutableList<JavaFileObject>`: Returns the source files that were compiled.

  - `status() -> Status`: Returns the status of the compilation (SUCCESS or FAILURE).

  - `diagnostics() -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Returns all diagnostics reported during compilation in unspecified order.

  - `errors() -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Returns only the error diagnostics reported during compilation.

  - `warnings() -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Returns warning and mandatory warning diagnostics reported during compilation.

  - `notes() -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Returns note diagnostics reported during compilation.

  - `diagnosticsOfKind(kind: Kind, more: Kind...) -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Returns diagnostics matching the specified kinds.

  - `generatedFiles() -> ImmutableList<JavaFileObject>`: Returns files generated during compilation; throws IllegalStateException for failed compilations.

  - `generatedSourceFiles() -> ImmutableList<JavaFileObject>`: Returns source files generated during compilation; throws IllegalStateException for failed compilations.

  - `generatedFile(location: Location, path: String) -> Optional<JavaFileObject>`: Returns the generated file at the specified path, if present.

  - `generatedFile(location: Location, packageName: String, fileName: String) -> Optional<JavaFileObject>`: Returns the generated file with the specified package and filename, if present.

  - `generatedSourceFile(qualifiedName: String) -> Optional<JavaFileObject>`: Returns the generated source file for the type with the given qualified name, if present.

  - `toString() -> String`: Returns a string representation of the compilation including sources, processors, and options.

  - `describeFailureDiagnostics() -> String`: Returns a description of why the compilation failed.

  - `describeGeneratedSourceFiles() -> String`: Returns a description of the source files generated by this compilation.

  - `describeGeneratedFile(generatedFile: JavaFileObject) -> String`: Returns a description of the contents of a given generated file.

  - `toImmutableList() -> Collector<T, ?, ImmutableList<T>>`: Static method returning a collector that collects to ImmutableList.

- `Compilation.Status`: Enumeration of compilation status values.

  - `SUCCESS`: Compilation finished without errors.

  - `FAILURE`: Compilation finished with errors.

---

`CompilationFailureException.java`:

- `CompilationFailureException`: RuntimeException thrown when compilation fails without reporting error diagnostics.

  - `CompilationFailureException(compilation: Compilation) -> CompilationFailureException`: Package-private constructor that creates exception with descriptive message about the failure.

---

`CompilationRule.java`:

- `CompilationRule`: JUnit4 Rule that executes tests with Elements and Types instances available during execution.

  - `CompilationRule() -> CompilationRule`: Public constructor.

  - `apply(base: Statement, description: Description) -> Statement`: Applies the rule by compiling a dummy source with an evaluating processor.

  - `getElements() -> Elements`: Returns the Elements instance associated with the current rule execution; throws IllegalStateException if called outside rule execution.

  - `getTypes() -> Types`: Returns the Types instance associated with the current rule execution; throws IllegalStateException if called outside rule execution.

- `CompilationRule.EvaluatingProcessor`: AbstractProcessor that runs the test statement during annotation processing.

  - `EvaluatingProcessor(base: Statement) -> EvaluatingProcessor`: Package-private constructor.

  - `getSupportedSourceVersion() -> SourceVersion`: Returns the latest supported source version.

  - `getSupportedAnnotationTypes() -> Set<String>`: Returns a set containing "*" to process all annotation types.

  - `init(processingEnv: ProcessingEnvironment) -> void`: Initializes the processor and captures Elements and Types instances.

  - `process(annotations: Set<? extends TypeElement>, roundEnv: RoundEnvironment) -> boolean`: Executes the test statement on the last processing round after compilation.

  - `throwIfStatementThrew() -> void`: Throws the exception that the base statement threw, if any.

---

`CompilationSubject.java`:

- `CompilationSubject`: Truth Subject for making assertions about Compilation results.

  - `CompilationSubject(failureMetadata: FailureMetadata, actual: Compilation) -> CompilationSubject`: Package-private constructor.

  - `compilations() -> Subject.Factory<CompilationSubject, Compilation>`: Static method returning a factory for creating CompilationSubject instances.

  - `assertThat(actual: Compilation) -> CompilationSubject`: Static method for starting assertions about a Compilation.

  - `succeeded() -> void`: Asserts that the compilation succeeded without errors.

  - `succeededWithoutWarnings() -> void`: Asserts that the compilation succeeded without any warnings.

  - `failed() -> void`: Asserts that the compilation failed with errors.

  - `hadErrorCount(expectedCount: int) -> void`: Asserts that the compilation had exactly the expected number of errors.

  - `hadErrorContaining(expectedSubstring: String) -> DiagnosticInFile`: Asserts that at least one error contains the expected substring.

  - `hadErrorContainingMatch(expectedPattern: String) -> DiagnosticInFile`: Asserts that at least one error matches the expected pattern string.

  - `hadErrorContainingMatch(expectedPattern: Pattern) -> DiagnosticInFile`: Asserts that at least one error matches the expected Pattern.

  - `hadWarningCount(expectedCount: int) -> void`: Asserts that the compilation had exactly the expected number of warnings.

  - `hadWarningContaining(expectedSubstring: String) -> DiagnosticInFile`: Asserts that at least one warning contains the expected substring.

  - `hadWarningContainingMatch(expectedPattern: String) -> DiagnosticInFile`: Asserts that at least one warning matches the expected pattern string.

  - `hadWarningContainingMatch(expectedPattern: Pattern) -> DiagnosticInFile`: Asserts that at least one warning matches the expected Pattern.

  - `hadNoteCount(expectedCount: int) -> void`: Asserts that the compilation had exactly the expected number of notes.

  - `hadNoteContaining(expectedSubstring: String) -> DiagnosticInFile`: Asserts that at least one note contains the expected substring.

  - `hadNoteContainingMatch(expectedPattern: String) -> DiagnosticInFile`: Asserts that at least one note matches the expected pattern string.

  - `hadNoteContainingMatch(expectedPattern: Pattern) -> DiagnosticInFile`: Asserts that at least one note matches the expected Pattern.

  - `checkDiagnosticCount(expectedCount: int, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> void`: Private method checking that diagnostic count matches expected value.

  - `messageListing(diagnostics: Iterable<? extends Diagnostic<?>>, headingFormat: String, formatArgs: Object...) -> String`: Static method creating a formatted message listing diagnostics.

  - `kindSingular(kind: Diagnostic.Kind) -> String`: Static method returning the singular phrase for a diagnostic kind.

  - `kindPlural(kind: Diagnostic.Kind) -> String`: Static method returning the plural phrase for a diagnostic kind.

  - `hadDiagnosticContaining(expectedSubstring: String, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> DiagnosticInFile`: Private method finding diagnostics containing a substring.

  - `hadDiagnosticContainingMatch(expectedPattern: String, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> DiagnosticInFile`: Private method finding diagnostics matching a pattern string.

  - `hadDiagnosticContainingMatch(expectedPattern: Pattern, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> DiagnosticInFile`: Private method finding diagnostics matching a Pattern.

  - `hadDiagnosticContainingMatch(diagnosticMatchDescription: String, expectedPattern: Pattern, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> DiagnosticInFile`: Private method finding diagnostics matching pattern with custom description.

  - `findMatchingDiagnostics(expectedDiagnostic: String, expectedPattern: Pattern, kind: Diagnostic.Kind, more: Diagnostic.Kind...) -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Private method returning diagnostics matching kinds and pattern; fails if none found.

  - `generatedFile(location: Location, packageName: String, fileName: String) -> JavaFileObjectSubject`: Asserts that compilation generated a file with the specified name in the specified package.

  - `generatedFile(location: Location, path: String) -> JavaFileObjectSubject`: Asserts that compilation generated a file at the specified path.

  - `generatedSourceFile(qualifiedName: String) -> JavaFileObjectSubject`: Asserts that compilation generated a source file for the type with the given qualified name.

  - `checkGeneratedFile(generatedFile: Optional<JavaFileObject>, location: Location, path: String) -> JavaFileObjectSubject`: Private method checking if a file was generated and returning subject for it.

  - `actualNotNull() -> Compilation`: Private method asserting actual is not null and returning it.

  - `toImmutableList() -> Collector<T, ?, ImmutableList<T>>`: Static method returning collector for ImmutableList.

  - `toImmutableSet() -> Collector<T, ?, ImmutableSet<T>>`: Static method returning collector for ImmutableSet.

- `CompilationSubject.DiagnosticAssertions`: Base class for making assertions about diagnostics.

  - `DiagnosticAssertions(expectedDiagnostic: String, matchingDiagnostics: Iterable<Diagnostic<? extends JavaFileObject>>) -> DiagnosticAssertions`: Package-private constructor.

  - `DiagnosticAssertions(previous: DiagnosticAssertions, matchingDiagnostics: Iterable<Diagnostic<? extends JavaFileObject>>) -> DiagnosticAssertions`: Package-private constructor copying from previous assertions.

  - `filterDiagnostics(predicate: Predicate<? super Diagnostic<? extends JavaFileObject>>) -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Filters diagnostics by predicate.

  - `mapDiagnostics(mapper: Function<? super Diagnostic<? extends JavaFileObject>, T>) -> Stream<T>`: Maps diagnostics using the provided function.

  - `failExpectingMatchingDiagnostic(format: String, args: Object...) -> void`: Protected method that fails with a formatted message.

- `CompilationSubject.DiagnosticInFile`: Assertions that a diagnostic was found in a specific file.

  - `DiagnosticInFile(expectedDiagnostic: String, diagnosticsWithMessage: Iterable<Diagnostic<? extends JavaFileObject>>) -> DiagnosticInFile`: Private constructor.

  - `inFile(expectedFile: JavaFileObject) -> DiagnosticOnLine`: Asserts that the diagnostic was found in the given file.

  - `findDiagnosticsInFile(expectedFile: JavaFileObject) -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Private method finding diagnostics in the specified file; fails if none found.

  - `sourceFilesWithDiagnostics() -> ImmutableSet<String>`: Private method returning set of source file names that have diagnostics.

- `CompilationSubject.LinesInFile`: Object that provides access to lines in a file.

  - `LinesInFile(file: JavaFileObject) -> LinesInFile`: Package-private constructor.

  - `fileName() -> String`: Returns the file name.

  - `linesInFile() -> ImmutableList<String>`: Returns the lines in the file, lazily loading them if needed.

  - `toLineList() -> Collector<Long, ?, String>`: Returns a Collector that formats line numbers as a numbered list.

  - `listLine(lineNumber: long) -> String`: Returns a formatted string for the line at the given line number (1-based).

- `CompilationSubject.DiagnosticOnLine`: Assertions that a diagnostic was found on a specific line.

  - `DiagnosticOnLine(previous: DiagnosticAssertions, file: JavaFileObject, diagnosticsInFile: ImmutableList<Diagnostic<? extends JavaFileObject>>) -> DiagnosticOnLine`: Private constructor.

  - `onLine(expectedLine: long) -> DiagnosticAtColumn`: Asserts that the diagnostic was found on the given line.

  - `onLineContaining(expectedLineSubstring: String) -> void`: Asserts that the diagnostic was found on the single line containing the specified substring.

  - `findLineContainingSubstring(expectedLineSubstring: String) -> long`: Private method finding the single line number containing the expected substring.

  - `findMatchingDiagnosticsOnLine(expectedLine: long) -> ImmutableList<Diagnostic<? extends JavaFileObject>>`: Private method finding diagnostics on the specified line; fails if none found.

- `CompilationSubject.DiagnosticAtColumn`: Assertions that a diagnostic was found at a specific column.

  - `DiagnosticAtColumn(previous: DiagnosticAssertions, linesInFile: LinesInFile, line: long, diagnosticsOnLine: ImmutableList<Diagnostic<? extends JavaFileObject>>) -> DiagnosticAtColumn`: Private constructor.

  - `atColumn(expectedColumn: long) -> void`: Asserts that the diagnostic was found at the given column.

  - `columnsWithDiagnostics() -> ImmutableSet<String>`: Private method returning set of column numbers where diagnostics were found.

---

`CompilationSubjectFactory.java`:

- `CompilationSubjectFactory`: Factory for creating CompilationSubject instances for use with Truth.

  - `CompilationSubjectFactory() -> CompilationSubjectFactory`: Package-private constructor.

  - `createSubject(failureMetadata: FailureMetadata, that: Compilation) -> CompilationSubject`: Creates a new CompilationSubject with the given metadata and actual value.

---

`Compiler.java`:

- `Compiler`: An object that can compile Java source files with annotation processors.

  - `javac() -> Compiler`: Static factory method returning the system javac compiler.

  - `compiler(javaCompiler: JavaCompiler) -> Compiler`: Static factory method returning a Compiler using the given JavaCompiler instance.

  - `javaCompiler() -> JavaCompiler`: Abstract method returning the JavaCompiler instance.

  - `processors() -> ImmutableList<Processor>`: Abstract method returning the annotation processors applied during compilation.

  - `options() -> ImmutableList<String>`: Abstract method returning the options passed to the compiler.

  - `classPath() -> Optional<ImmutableList<File>>`: Abstract method returning the compilation class path; if not present, system class path is used.

  - `annotationProcessorPath() -> Optional<ImmutableList<File>>`: Abstract method returning the annotation processor path; if not present, system path is used.

  - `withProcessors(processors: Processor...) -> Compiler`: Returns a new instance with the specified processors, replacing any previously specified.

  - `withProcessors(processors: Iterable<? extends Processor>) -> Compiler`: Returns a new instance with the specified processors, replacing any previously specified.

  - `withOptions(options: Object...) -> Compiler`: Returns a new instance with the specified options, replacing any previously specified.

  - `withOptions(options: Iterable<? extends Object>) -> Compiler`: Returns a new instance with the specified options, replacing any previously specified.

  - `withClasspathFrom(classloader: ClassLoader) -> Compiler`: Deprecated method that returns a new instance using classpath from the given classloader.

  - `withClasspath(classPath: Iterable<File>) -> Compiler`: Returns a new instance using the given classpath instead of the system classpath.

  - `withAnnotationProcessorPath(annotationProcessorPath: Iterable<File>) -> Compiler`: Returns a new instance using the given annotation processor path.

  - `compile(files: JavaFileObject...) -> Compilation`: Compiles the given Java source files and returns the results.

  - `compile(files: Iterable<? extends JavaFileObject>) -> Compilation`: Compiles the given Java source files and returns the results.

  - `standardFileManager(diagnosticCollector: DiagnosticCollector<JavaFileObject>) -> StandardJavaFileManager`: Private method creating a StandardJavaFileManager with UTF-8 encoding.

  - `getPlatformClassLoader() -> ClassLoader`: Static method returning the platform class loader (JDK 9+) or null (JDK 8).

  - `getClasspathFromClassloader(classloader: ClassLoader) -> ImmutableList<File>`: Static method extracting classpath from the given classloader hierarchy.

  - `setLocation(fileManager: InMemoryJavaFileManager, location: StandardLocation, path: ImmutableList<File>) -> void`: Static method setting the location on the file manager.

  - `copy(processors: ImmutableList<Processor>, options: ImmutableList<String>, classPath: Optional<ImmutableList<File>>, annotationProcessorPath: Optional<ImmutableList<File>>) -> Compiler`: Private method creating a new Compiler instance with the specified configuration.

---

`CompileTester.java`:

- `CompileTester`: Root interface of the fluent API for testing compilation results.

  - `parsesAs(first: JavaFileObject, rest: JavaFileObject...) -> void`: Tests that the code parses equivalently to the specified code.

  - `compilesWithoutError() -> SuccessfulCompilationClause`: Tests for successful compilation without errors.

  - `compilesWithoutWarnings() -> CleanCompilationClause`: Tests for successful compilation without warnings or errors.

  - `failsToCompile() -> UnsuccessfulCompilationClause`: Tests for unsuccessful compilation.

- `CompileTester.ChainingClause<T>`: Interface allowing chaining of test conditions.

  - `and() -> T`: Returns the clause type for chaining additional conditions.

- `CompileTester.CompilationWithNotesClause<T>`: Interface for checking notes in a compilation.

  - `withNoteContaining(messageFragment: String) -> FileClause<T>`: Checks that a note exists containing the given message fragment.

  - `withNoteCount(noteCount: int) -> T`: Checks that the total note count matches the given amount.

- `CompileTester.CompilationWithWarningsClause<T>`: Interface for checking notes and warnings in a compilation.

  - `withWarningContaining(messageFragment: String) -> FileClause<T>`: Checks that a warning exists containing the given message fragment.

  - `withWarningCount(warningCount: int) -> T`: Checks that the total warning count matches the given amount.

- `CompileTester.FileClause<T>`: Interface for checking that a diagnostic is associated with a particular file.

  - `in(file: JavaFileObject) -> LineClause<T>`: Specifies the file where the diagnostic should be found.

- `CompileTester.LineClause<T>`: Interface for checking that a diagnostic is on a particular line.

  - `onLine(lineNumber: long) -> ColumnClause<T>`: Specifies the line number where the diagnostic should be found.

- `CompileTester.ColumnClause<T>`: Interface for checking that a diagnostic starts at a particular column.

  - `atColumn(columnNumber: long) -> ChainingClause<T>`: Specifies the column number where the diagnostic should start.

- `CompileTester.GeneratedPredicateClause<T>`: Interface for checking that files were generated.

  - `generatesSources(first: JavaFileObject, rest: JavaFileObject...) -> T`: Checks that source files with equivalent AST were generated.

  - `generatesFiles(first: JavaFileObject, rest: JavaFileObject...) -> T`: Checks that files with equivalent kind and content were generated.

  - `generatesFileNamed(location: JavaFileManager.Location, packageName: String, relativeName: String) -> SuccessfulFileClause<T>`: Checks that a file with the specified location, package, and filename was generated.

- `CompileTester.SuccessfulFileClause<T>`: Interface for checking that a generated file has specified contents.

  - `withContents(expectedByteSource: ByteSource) -> SuccessfulFileClause<T>`: Checks that the generated file contents match the expected ByteSource.

  - `withStringContents(charset: Charset, expectedString: String) -> SuccessfulFileClause<T>`: Checks that the generated file contents equal the expected string in the given charset.

  - `and() -> GeneratedPredicateClause<T>`: Returns the clause for chaining additional file generation checks.

- `CompileTester.SuccessfulCompilationClause`: Interface for further tests on successful compilations.

  - `and() -> GeneratedPredicateClause<SuccessfulCompilationClause>`: Returns the clause for checking generated files.

- `CompileTester.CleanCompilationClause`: Interface for further tests on successful compilations without warnings.

  - `and() -> GeneratedPredicateClause<CleanCompilationClause>`: Returns the clause for checking generated files.

- `CompileTester.UnsuccessfulCompilationClause`: Interface for further tests on unsuccessful compilations.

  - `withErrorContaining(messageFragment: String) -> FileClause<UnsuccessfulCompilationClause>`: Checks that an error exists containing the given message fragment.

  - `withErrorCount(errorCount: int) -> UnsuccessfulCompilationClause`: Checks that the total error count matches the given amount.

---

`ForwardingStandardJavaFileManager.java`:

- `ForwardingStandardJavaFileManager`: Forwards calls to a given StandardJavaFileManager; subclasses may override methods.

  - `ForwardingStandardJavaFileManager(fileManager: StandardJavaFileManager) -> ForwardingStandardJavaFileManager`: Protected constructor creating a forwarding file manager.

  - `getJavaFileObjectsFromFiles(files: Iterable<? extends File>) -> Iterable<? extends JavaFileObject>`: Forwards to the delegate file manager.

  - `getJavaFileObjects(files: File...) -> Iterable<? extends JavaFileObject>`: Forwards to the delegate file manager.

  - `getJavaFileObjects(names: String...) -> Iterable<? extends JavaFileObject>`: Forwards to the delegate file manager.

  - `getJavaFileObjectsFromStrings(names: Iterable<String>) -> Iterable<? extends JavaFileObject>`: Forwards to the delegate file manager.

  - `setLocation(location: Location, path: Iterable<? extends File>) -> void`: Forwards to the delegate file manager.

  - `getLocation(location: Location) -> Iterable<? extends File>`: Forwards to the delegate file manager.

  - `setLocationFromPaths(location: Location, searchpath: Collection<? extends Path>) -> void`: Forwards to the delegate file manager if available (JDK 9+); no-op on JDK 8.

---

`InMemoryJavaFileManager.java`:

- `InMemoryJavaFileManager`: A file manager implementation that stores all output in memory.

  - `InMemoryJavaFileManager(fileManager: StandardJavaFileManager) -> InMemoryJavaFileManager`: Package-private constructor wrapping a StandardJavaFileManager.

  - `uriForFileObject(location: Location, packageName: String, relativeName: String) -> URI`: Static method creating a URI for a file object based on location, package, and name.

  - `uriForJavaFileObject(location: Location, className: String, kind: Kind) -> URI`: Static method creating a URI for a Java file object based on location, class name, and kind.

  - `isSameFile(a: FileObject, b: FileObject) -> boolean`: Returns true if both file objects have the same URI.

  - `getFileForInput(location: Location, packageName: String, relativeName: String) -> FileObject`: Returns the file for input from output cache or in-memory inputs, or delegates to super.

  - `getJavaFileForInput(location: Location, className: String, kind: Kind) -> JavaFileObject`: Returns the Java file for input from output cache or in-memory inputs, or delegates to super.

  - `findInMemoryInput(className: String) -> Optional<JavaFileObject>`: Private method finding in-memory input by class name.

  - `findInMemoryInput(packageName: String, relativeName: String) -> Optional<JavaFileObject>`: Private method finding in-memory input by package and relative name.

  - `getFileForOutput(location: Location, packageName: String, relativeName: String, sibling: FileObject) -> FileObject`: Returns an in-memory file object for output.

  - `getJavaFileForOutput(location: Location, className: String, kind: Kind, sibling: FileObject) -> JavaFileObject`: Returns an in-memory Java file object for output.

  - `getGeneratedSources() -> ImmutableList<JavaFileObject>`: Returns all generated source files from SOURCE_OUTPUT location.

  - `getOutputFiles() -> ImmutableList<JavaFileObject>`: Returns all output files stored in memory.

  - `addSourceFiles(files: Iterable<? extends JavaFileObject>) -> void`: Adds files that should be available in the source path.

- `InMemoryJavaFileManager.InMemoryJavaFileObject`: SimpleJavaFileObject implementation storing file contents in memory.

  - `InMemoryJavaFileObject(uri: URI) -> InMemoryJavaFileObject`: Package-private constructor creating an in-memory file object.

  - `openInputStream() -> InputStream`: Opens an input stream for reading the file contents; throws FileNotFoundException if no data.

  - `openOutputStream() -> OutputStream`: Opens an output stream for writing file contents; saves data on close.

  - `openReader(ignoreEncodingErrors: boolean) -> Reader`: Opens a reader for reading file contents; throws FileNotFoundException if no data.

  - `getCharContent(ignoreEncodingErrors: boolean) -> CharSequence`: Returns the character content of the file; throws FileNotFoundException if no data.

  - `openWriter() -> Writer`: Opens a writer for writing file contents; saves data on close.

  - `getLastModified() -> long`: Returns the last modified timestamp.

  - `delete() -> boolean`: Deletes the file contents and resets timestamp.

  - `toString() -> String`: Returns a string representation showing URI and kind.

---

`JavaFileObjects.java`:

- `JavaFileObjects`: Utility class for creating JavaFileObject instances.

  - `JavaFileObjects() -> JavaFileObjects`: Private constructor preventing instantiation.

  - `forSourceString(fullyQualifiedName: String, source: String) -> JavaFileObject`: Creates a read-only SOURCE kind JavaFileObject with the given name and source content.

  - `forSourceLines(fullyQualifiedName: String, lines: String...) -> JavaFileObject`: Creates a JavaFileObject by joining lines with newlines.

  - `forSourceLines(fullyQualifiedName: String, lines: Iterable<String>) -> JavaFileObject`: Creates a JavaFileObject by joining lines from an iterable with newlines.

  - `forResource(resourceUrl: URL) -> JavaFileObject`: Returns a read-only JavaFileObject for the resource at the given URL.

  - `forResource(resourceName: String) -> JavaFileObject`: Returns a read-only JavaFileObject for the classpath resource with the given name.

  - `deduceKind(uri: URI) -> Kind`: Static method deducing the JavaFileObject.Kind from the URI path extension.

  - `asByteSource(javaFileObject: JavaFileObject) -> ByteSource`: Static method wrapping a JavaFileObject as a ByteSource.

- `JavaFileObjects.StringSourceJavaFileObject`: SimpleJavaFileObject implementation storing source as a string.

  - `StringSourceJavaFileObject(fullyQualifiedName: String, source: String) -> StringSourceJavaFileObject`: Private constructor.

  - `createUri(fullyQualifiedClassName: String) -> URI`: Static method creating a URI from the fully qualified class name.

  - `getCharContent(ignoreEncodingErrors: boolean) -> CharSequence`: Returns the source string.

  - `openOutputStream() -> OutputStream`: Throws IllegalStateException as the object is read-only.

  - `openInputStream() -> InputStream`: Returns an input stream reading the source string.

  - `openWriter() -> Writer`: Throws IllegalStateException as the object is read-only.

  - `openReader(ignoreEncodingErrors: boolean) -> Reader`: Returns a reader reading the source string.

  - `getLastModified() -> long`: Returns the timestamp when the object was created.

- `JavaFileObjects.JarFileJavaFileObject`: ForwardingJavaFileObject for resources inside JAR files.

  - `JarFileJavaFileObject(jarUrl: URL) -> JarFileJavaFileObject`: Private constructor.

  - `getPathUri(jarUrl: URL) -> URI`: Static method extracting the path URI from a JAR URL.

- `JavaFileObjects.ResourceSourceJavaFileObject`: SimpleJavaFileObject for classpath resources.

  - `ResourceSourceJavaFileObject(resourceUrl: URL, resourceUri: URI) -> ResourceSourceJavaFileObject`: Private constructor to avoid creating URI twice.

  - `ResourceSourceJavaFileObject(resourceUrl: URL) -> ResourceSourceJavaFileObject`: Private constructor that creates URI from URL.

  - `getCharContent(ignoreEncodingErrors: boolean) -> CharSequence`: Reads and returns the resource content as a string.

  - `openInputStream() -> InputStream`: Opens an input stream for reading the resource.

  - `openReader(ignoreEncodingErrors: boolean) -> Reader`: Opens a reader for reading the resource.

---

`JavaFileObjectSubject.java`:

- `JavaFileObjectSubject`: Truth Subject for making assertions about JavaFileObject instances.

  - `JavaFileObjectSubject(failureMetadata: FailureMetadata, actual: JavaFileObject) -> JavaFileObjectSubject`: Package-private constructor.

  - `javaFileObjects() -> Subject.Factory<JavaFileObjectSubject, JavaFileObject>`: Static factory method returning a Subject.Factory.

  - `assertThat(actual: JavaFileObject) -> JavaFileObjectSubject`: Static method to start making assertions about a JavaFileObject.

  - `actualAsString() -> String`: Protected method returning the string representation (URI path) of the actual file.

  - `isEqualTo(other: Object) -> void`: Override that compares file contents if other is a JavaFileObject, otherwise uses Object.equals().

  - `hasContents(expectedByteSource: ByteSource) -> void`: Asserts that the file contents equal the expected ByteSource.

  - `contentsAsString(charset: Charset) -> StringSubject`: Returns a StringSubject for making assertions about file contents as a string.

  - `contentsAsUtf8String() -> StringSubject`: Returns a StringSubject for making assertions about file contents as UTF-8 string.

  - `hasSourceEquivalentTo(expected: JavaFileObject) -> void`: Asserts that the file has an equivalent AST to the expected source file.

  - `containsElementsIn(expectedFile: JavaFileObject) -> void`: Asserts that every node in the expected pattern's AST exists in the actual file's AST in order.

  - `checkDifference(expectation: String, expectedSource: JavaFileObject, filter: TreeDiffer.DiffFilter) -> void`: Private method performing tree differencing and reporting differences.

  - `actualNotNull() -> JavaFileObject`: Private method ensuring actual is not null and returning it.

---

`JavaFileObjectSubjectFactory.java`:

- `JavaFileObjectSubjectFactory`: Factory for creating JavaFileObjectSubject instances.

  - `JavaFileObjectSubjectFactory() -> JavaFileObjectSubjectFactory`: Package-private constructor.

  - `createSubject(failureMetadata: FailureMetadata, that: JavaFileObject) -> JavaFileObjectSubject`: Creates a new JavaFileObjectSubject with the given metadata and actual value.

---

`JavaSourcesSubject.java`:

- `JavaSourcesSubject`: Truth Subject for making assertions about compilations of Java sources.

  - `JavaSourcesSubject(failureMetadata: FailureMetadata, actual: Iterable<? extends JavaFileObject>) -> JavaSourcesSubject`: Package-private constructor.

  - `withCompilerOptions(options: Iterable<?>) -> JavaSourcesSubject`: Returns a new instance with the specified compiler options added.

  - `withCompilerOptions(options: Object...) -> JavaSourcesSubject`: Returns a new instance with the specified compiler options added (varargs version).

  - `withClasspathFrom(classLoader: ClassLoader) -> JavaSourcesSubject`: Deprecated method returning a new instance using classpath from the given ClassLoader.

  - `withClasspath(classPath: Iterable<File>) -> JavaSourcesSubject`: Returns a new instance using the specified compilation classpath.

  - `processedWith(processor: Processor, processors: Processor...) -> JavaSourcesSubject`: Returns a new instance using the specified annotation processors (varargs version).

  - `processedWith(processors: Iterable<? extends Processor>) -> JavaSourcesSubject`: Returns a new instance using the specified annotation processors (iterable version).

  - `parsesAs(first: JavaFileObject, rest: JavaFileObject...) -> void`: Asserts that sources parse to match the expected JavaFileObjects.

  - `compilesWithoutError() -> SuccessfulCompilationClause`: Asserts that compilation succeeds without errors.

  - `compilesWithoutWarnings() -> CleanCompilationClause`: Asserts that compilation succeeds without warnings.

  - `failsToCompile() -> UnsuccessfulCompilationClause`: Asserts that compilation fails.

  - `assertAbout(javaSource: JavaFileObject) -> SingleSourceAdapter`: Static method creating assertions for a single JavaFileObject.

  - `assertAbout(javaSources: Iterable<? extends JavaFileObject>) -> CompilationClause`: Static method creating assertions for multiple JavaFileObjects.

  - `actualNotNull() -> Iterable<? extends JavaFileObject>`: Private method ensuring actual is not null and returning it.

  - `toImmutableList() -> Collector<T, ?, ImmutableList<T>>`: Static method returning a collector for ImmutableList.

  - `newCompilationClause(javaSources: Iterable<? extends JavaFileObject>) -> CompilationClause`: Private method creating a new CompilationClause.

- `JavaSourcesSubject.CompilationClause`: Implementation of CompileTester for managing compilation and assertions.

  - `CompilationClause() -> CompilationClause`: Package-private constructor.

  - `parsesAs(first: JavaFileObject, rest: JavaFileObject...) -> void`: Verifies that sources parse to match the expected files.

  - `compilesWithoutError() -> SuccessfulCompilationClause`: Performs compilation and asserts success.

  - `compilesWithoutWarnings() -> CleanCompilationClause`: Performs compilation and asserts no warnings.

  - `failsToCompile() -> UnsuccessfulCompilationClause`: Performs compilation and asserts failure.

  - `compile() -> Compilation`: Private method performing the actual compilation.

  - `failGeneratesSources(sources: Iterable<? extends JavaFileObject>, actualSources: ImmutableList<JavaFileObject>) -> void`: Private method handling failure when no candidates match expected sources.

  - `failGeneratesSources(sources: Iterable<? extends JavaFileObject>, actualSources: ImmutableList<JavaFileObject>, nearestSourceFile: JavaFileObject, nearestSourceFileDiff: TreeDifference) -> void`: Private method handling failure with a near-match candidate.

- `JavaSourcesSubject.CompilationWithWarningsBuilder<T>`: Abstract base class for compilation clauses with warning/note checking.

  - `CompilationWithWarningsBuilder(compilation: Compilation) -> CompilationWithWarningsBuilder`: Package-private constructor.

  - `withNoteCount(noteCount: int) -> T`: Asserts the compilation had the specified number of notes.

  - `withNoteContaining(messageFragment: String) -> FileClause<T>`: Asserts the compilation had a note containing the message fragment.

  - `withWarningCount(warningCount: int) -> T`: Asserts the compilation had the specified number of warnings.

  - `withWarningContaining(messageFragment: String) -> FileClause<T>`: Asserts the compilation had a warning containing the message fragment.

  - `withErrorCount(errorCount: int) -> T`: Asserts the compilation had the specified number of errors.

  - `withErrorContaining(messageFragment: String) -> FileClause<T>`: Asserts the compilation had an error containing the message fragment.

  - `thisObject() -> T`: Protected method returning this cast to T for method chaining.

- `JavaSourcesSubject.GeneratedCompilationBuilder<T>`: Abstract class for compilation clauses with generated file checking.

  - `GeneratedCompilationBuilder(compilation: Compilation) -> GeneratedCompilationBuilder`: Package-private constructor.

  - `generatesSources(first: JavaFileObject, rest: JavaFileObject...) -> T`: Asserts that the compilation generated the specified source files.

  - `generatesFiles(first: JavaFileObject, rest: JavaFileObject...) -> T`: Asserts that the compilation generated the specified files.

  - `checkGeneratedFile(generatedFile: Optional<JavaFileObject>, location: Location, path: String) -> SuccessfulFileClause<T>`: Protected method checking if a file was generated.

  - `generatesFileNamed(location: Location, packageName: String, relativeName: String) -> SuccessfulFileClause<T>`: Asserts a file with the specified name was generated.

  - `and() -> GeneratedPredicateClause<T>`: Returns this for method chaining.

- `JavaSourcesSubject.UnsuccessfulCompilationBuilder`: Implementation for failed compilation assertions.

  - `UnsuccessfulCompilationBuilder(compilation: Compilation) -> UnsuccessfulCompilationBuilder`: Package-private constructor.

- `JavaSourcesSubject.SuccessfulCompilationBuilder`: Implementation for successful compilation assertions.

  - `SuccessfulCompilationBuilder(compilation: Compilation) -> SuccessfulCompilationBuilder`: Package-private constructor.

- `JavaSourcesSubject.CleanCompilationBuilder`: Implementation for clean (no warnings) compilation assertions.

  - `CleanCompilationBuilder(compilation: Compilation) -> CleanCompilationBuilder`: Package-private constructor.

- `JavaSourcesSubject.SingleSourceAdapter`: Adapter allowing single source file testing using the same API.

  - `SingleSourceAdapter(delegate: JavaSourcesSubject) -> SingleSourceAdapter`: Package-private constructor.

  - All methods delegate to the internal JavaSourcesSubject delegate.

- `JavaSourcesSubject.CompilationUnitTreeAndToplevelTypes`: AutoValue class pairing a CompilationUnitTree with its top-level types.

  - `create(tree: CompilationUnitTree, types: ImmutableSet<String>) -> CompilationUnitTreeAndToplevelTypes`: Static factory method.

  - `tree() -> CompilationUnitTree`: Abstract method returning the compilation unit tree.

  - `topLevelTypes() -> ImmutableSet<String>`: Abstract method returning the top-level types.

---

`JavaSourcesSubjectFactory.java`:

- `JavaSourcesSubjectFactory`: Factory for creating JavaSourcesSubject instances.

  - `JavaSourcesSubjectFactory() -> JavaSourcesSubjectFactory`: Package-private constructor.

  - `createSubject(failureMetadata: FailureMetadata, that: Iterable<? extends JavaFileObject>) -> JavaSourcesSubject`: Creates a new JavaSourcesSubject with the given metadata and actual value.

---

`JavaSourceSubjectFactory.java`:

- `JavaSourceSubjectFactory`: Factory for creating SingleSourceAdapter instances for single file testing.

  - `JavaSourceSubjectFactory() -> JavaSourceSubjectFactory`: Package-private constructor.

  - `createSubject(failureMetadata: FailureMetadata, that: JavaFileObject) -> JavaSourcesSubject.SingleSourceAdapter`: Creates a new SingleSourceAdapter wrapping a JavaSourcesSubject for single file testing.

---

`MoreTrees.java`:

- `MoreTrees`: Utility class providing additional functionality for working with Tree instances.

  - `MoreTrees() -> MoreTrees`: Private constructor preventing instantiation.

  - `parseLinesToTree(lines: String...) -> CompilationUnitTree`: Static method parsing source lines into a CompilationUnitTree (varargs version).

  - `parseLinesToTree(lines: Iterable<String>) -> CompilationUnitTree`: Static method parsing source lines into a CompilationUnitTree (iterable version).

  - `parseLines(lines: String...) -> Parser.ParseResult`: Static method parsing source lines and producing a ParseResult (varargs version).

  - `parseLines(lines: Iterable<String>) -> Parser.ParseResult`: Static method parsing source lines and producing a ParseResult (iterable version).

  - `findSubtree(root: Tree, kind: Tree.Kind) -> Tree`: Static method finding the first subtree of the specified kind.

  - `findSubtree(root: Tree, kind: Tree.Kind, id: String) -> Tree`: Static method finding the first subtree of the specified kind matching the identifier.

  - `findSubtreePath(root: TreePath, kind: Tree.Kind) -> TreePath`: Static method finding a path to the first subtree of the specified kind.

  - `findSubtreePath(root: TreePath, kind: Tree.Kind, id: String) -> TreePath`: Static method finding a path to the first subtree matching kind and identifier.

- `MoreTrees.SearchScanner`: TreePathScanner for finding specific subtrees.

  - `SearchScanner(kind: Tree.Kind, id: Optional<String>) -> SearchScanner`: Package-private constructor.

  - `matches(node: Tree) -> boolean`: Private method checking if node matches search criteria.

  - `matches(node: Tree, id: String) -> boolean`: Private overload for non-optional id value.

  - `pathWithNode(node: Tree) -> TreePath`: Private method returning current path plus the node.

  - `or(ret: TreePath) -> Optional<TreePath>`: Private method returning empty Optional if ret is null.

  - `scan(tree: Tree, p: Void) -> Optional<TreePath>`: Override scanning a single tree node.

  - `scan(trees: Iterable<? extends Tree>, p: Void) -> Optional<TreePath>`: Override scanning multiple tree nodes.

  - `reduce(r1: Optional<TreePath>, r2: Optional<TreePath>) -> Optional<TreePath>`: Override reducing two scan results.

  - `visitBreak(tree: BreakTree, p: Void) -> Optional<TreePath>`: Override for visiting break statements.

  - `visitClass(tree: ClassTree, p: Void) -> Optional<TreePath>`: Override for visiting class declarations.

  - `visitContinue(tree: ContinueTree, p: Void) -> Optional<TreePath>`: Override for visiting continue statements.

  - `visitIdentifier(tree: IdentifierTree, p: Void) -> Optional<TreePath>`: Override for visiting identifiers.

  - `visitLabeledStatement(tree: LabeledStatementTree, p: Void) -> Optional<TreePath>`: Override for visiting labeled statements.

  - `visitLiteral(tree: LiteralTree, p: Void) -> Optional<TreePath>`: Override for visiting literals.

  - `visitMethod(tree: MethodTree, p: Void) -> Optional<TreePath>`: Override for visiting method declarations.

  - `visitMemberSelect(tree: MemberSelectTree, p: Void) -> Optional<TreePath>`: Override for visiting member selections.

  - `visitTypeParameter(tree: TypeParameterTree, p: Void) -> Optional<TreePath>`: Override for visiting type parameters.

  - `visitVariable(tree: VariableTree, p: Void) -> Optional<TreePath>`: Override for visiting variable declarations.

---

`Parser.java`:

- `Parser`: Utility class for parsing Java source files without full compilation.

  - `Parser() -> Parser`: Private constructor preventing instantiation.

  - `parse(javaFileObjects: Iterable<? extends JavaFileObject>) -> ParseResult`: Static method parsing sources into compilation units without compiling.

  - `checkForParseErrors(diagnostics: Iterable<Diagnostic<? extends JavaFileObject>>) -> void`: Private static method checking if parse errors were found and throwing exception if so.

  - `sortDiagnosticsByKind(diagnostics: Iterable<Diagnostic<? extends JavaFileObject>>) -> ImmutableListMultimap<Diagnostic.Kind, Diagnostic<? extends JavaFileObject>>`: Private static method sorting diagnostics by kind.

- `Parser.ParseResult`: Contains diagnostics, compilation units, and Trees instance from a parse task.

  - `ParseResult(diagnosticsByKind: ImmutableListMultimap<Diagnostic.Kind, Diagnostic<? extends JavaFileObject>>, compilationUnits: Iterable<? extends CompilationUnitTree>, trees: Trees) -> ParseResult`: Package-private constructor.

  - `diagnosticsByKind() -> ImmutableListMultimap<Diagnostic.Kind, Diagnostic<? extends JavaFileObject>>`: Returns diagnostics organized by kind.

  - `compilationUnits() -> Iterable<? extends CompilationUnitTree>`: Returns the parsed compilation units.

  - `trees() -> Trees`: Returns the Trees instance for this parse result.

---

`ProcessedCompileTesterFactory.java`:

- `ProcessedCompileTesterFactory`: Interface for creating CompileTester instances with annotation processors configured.

  - `withCompilerOptions(options: Iterable<?>) -> ProcessedCompileTesterFactory`: Adds options to be passed to the compiler.

  - `withCompilerOptions(options: Object...) -> ProcessedCompileTesterFactory`: Adds options to be passed to the compiler (varargs version).

  - `withClasspathFrom(classLoader: ClassLoader) -> ProcessedCompileTesterFactory`: Deprecated method to set classpath from ClassLoader.

  - `withClasspath(classPath: Iterable<File>) -> ProcessedCompileTesterFactory`: Sets the compilation classpath.

  - `processedWith(firstProcessor: Processor, additionalProcessors: Processor...) -> CompileTester`: Adds annotation processors to the compilation (varargs version).

  - `processedWith(processors: Iterable<? extends Processor>) -> CompileTester`: Adds annotation processors to the compilation (iterable version).

---

`TreeContext.java`:

- `TreeContext`: Manages and retrieves contextual information for trees in a compilation unit.

  - `TreeContext(compilationUnit: CompilationUnitTree, trees: Trees) -> TreeContext`: Package-private constructor.

  - `getCompilationUnit() -> CompilationUnitTree`: Returns the CompilationUnitTree instance.

  - `getTrees() -> Trees`: Returns the Trees instance.

  - `getPath(tree: Tree) -> TreePath`: Returns the TreePath to the given sub-tree.

  - `getStartLine(tree: Tree) -> long`: Returns the start line of the given sub-tree.

  - `getStartColumn(tree: Tree) -> long`: Returns the start column of the given sub-tree.

  - `getEndLine(tree: Tree) -> long`: Returns the end line of the given sub-tree.

  - `getEndColumn(tree: Tree) -> long`: Returns the end column of the given sub-tree.

  - `getStartPosition(tree: Tree) -> long`: Returns the start position of the given sub-tree.

  - `getEndPosition(tree: Tree) -> long`: Returns the end position of the given sub-tree.

---

`TreeDiffer.java`:

- `TreeDiffer`: Determines and reports differences between two compilation trees.

  - `TreeDiffer() -> TreeDiffer`: Private constructor preventing instantiation.

  - `diffCompilationUnits(expectedUnit: CompilationUnitTree, actualUnit: CompilationUnitTree) -> TreeDifference`: Static method returning differences between two compilation units.

  - `diffCompilationUnits(expectedUnit: CompilationUnitTree, actualUnit: CompilationUnitTree, filter: DiffFilter) -> TreeDifference`: Static method returning differences between actual tree and pattern using the specified filter.

  - `diffSubtrees(expectedPath: TreePath, actualPath: TreePath, filter: DiffFilter) -> TreeDifference`: Private static method creating a diff using the specified filter.

  - `diffSubtrees(expectedPath: TreePath, actualPath: TreePath) -> TreeDifference`: Static method for testing that diffs subtrees at given paths.

- `TreeDiffer.DiffVisitor`: SimpleTreeVisitor that traverses trees and verifies equality.

  - `DiffVisitor(expectedCompilationUnit: CompilationUnitTree, actualCompilationUnit: CompilationUnitTree, filter: DiffFilter) -> DiffVisitor`: Package-private constructor.

  - `DiffVisitor(expectedCompilationUnit: CompilationUnitTree, actualCompilationUnit: CompilationUnitTree, filter: DiffFilter, expectedPath: TreePath, actualPath: TreePath) -> DiffVisitor`: Private constructor with initialized paths.

  - `addTypeMismatch(expectedTree: Tree, actualTree: Tree) -> TreeDifference`: Public method adding a TwoWayDiff for different Tree.Kinds.

  - `diff(message: String, args: Object...) -> void`: Private format method reporting a diff.

  - `pushActual(tree: Tree) -> TreePath`: Private method pushing actual tree onto path.

  - `pushExpected(tree: Tree) -> TreePath`: Private method pushing expected tree onto path.

  - `pushBoth(expected: Tree, actual: Tree, work: Runnable) -> void`: Private method pushing trees onto paths and recursing.

  - `nameEquals(n1: Name, n2: Name) -> boolean`: Private method checking if Names are equal.

  - `scanAndReduce(expected: Tree, actual: Tree) -> TreeDifference`: Private method scanning two trees.

  - `parallelScan(expectedList: Iterable<? extends Tree>, actualList: Iterable<? extends Tree>) -> TreeDifference`: Private method scanning two iterables in parallel.

  - `defaultAction(node: Tree, otherTree: Tree) -> TreeDifference`: Override using reflection to compare trees generically.

  - `compareProperties(expectedProp: Object, actualProp: Object) -> TreeDifference`: Private method comparing property values.

  - `applyFilter(actual: Iterable<? extends Tree>, expected: Iterable<? extends Tree>) -> Iterable<? extends Tree>`: Private method applying filter to actual subtrees.

  - `isTreeIterable(type: Type) -> boolean`: Private static method checking if type is Iterable<? extends Tree>.

  - `visitOther(node: Tree, otherTree: Tree) -> TreeDifference`: Override that throws for unknown tree types.

- `TreeDiffer.DiffFilter`: Strategy interface for determining which trees should be diffed.

  - `filterActualMembers(expected: Iterable<? extends Tree>, actual: Iterable<? extends Tree>) -> Iterable<? extends Tree>`: Returns subset of actual members to diff.

  - `filterActualImports(expected: Iterable<? extends ImportTree>, actual: Iterable<? extends ImportTree>) -> Iterable<? extends ImportTree>`: Returns subset of actual imports to diff.

- `TreeDiffer.MatchExpectedTreesFilter`: Filter that ignores trees without matching pattern.

  - `MatchExpectedTreesFilter() -> MatchExpectedTreesFilter`: Package-private constructor.

  - `filterActualMembers(expected: Iterable<? extends Tree>, actual: Iterable<? extends Tree>) -> Iterable<? extends Tree>`: Override filtering actual members based on pattern.

  - `filterActualImports(expected: Iterable<? extends ImportTree>, actual: Iterable<? extends ImportTree>) -> Iterable<? extends ImportTree>`: Override filtering actual imports based on pattern.

  - `importIdentifier(tree: ImportTree) -> String`: Private method returning fully qualified import string.

- `TreeDiffer.MethodSignature`: AutoValue class representing method signature with name and parameter types.

  - `name() -> String`: Abstract method returning method name.

  - `parameterTypes() -> ImmutableList<String>`: Abstract method returning parameter types.

  - `create(method: MethodTree) -> MethodSignature`: Static factory method creating a MethodSignature.

---

`TreeDifference.java`:

- `TreeDifference`: Data structure describing syntactic differences between two trees.

  - `TreeDifference() -> TreeDifference`: Package-private constructor creating an empty TreeDifference.

  - `TreeDifference(builder: Builder) -> TreeDifference`: Private constructor creating from builder.

  - `isEmpty() -> boolean`: Returns true if there are no diffs.

  - `getExtraExpectedNodes() -> ImmutableList<OneWayDiff>`: Returns diffs for unmatched expected nodes.

  - `getExtraActualNodes() -> ImmutableList<OneWayDiff>`: Returns diffs for unmatched actual nodes.

  - `getDifferingNodes() -> ImmutableList<TwoWayDiff>`: Returns diffs for differing nodes.

  - `getDiffReport() -> String`: Returns a string reporting all diffs without context.

  - `getDiffReport(expectedContext: TreeContext, actualContext: TreeContext) -> String`: Returns a string reporting all diffs with context.

  - `formatExtraNodeMessage(expectedContext: TreeContext, actualContext: TreeContext, diff: OneWayDiff) -> String`: Private method creating log entry for extra node.

  - `formatDiffMessage(expectedContext: TreeContext, actualContext: TreeContext, diff: TwoWayDiff) -> String`: Private method creating log entry for differing nodes.

  - `truncateNodeContents(node: String) -> String`: Private method returning formatted node contents with truncation if too long.

- `TreeDifference.Builder`: Builder for constructing TreeDifference objects.

  - `Builder() -> Builder`: Package-private constructor.

  - `addExtraExpectedNode(path: TreePath) -> Builder`: Logs extra expected node.

  - `addExtraExpectedNode(path: TreePath, message: String) -> Builder`: Logs extra expected node with message.

  - `addExtraActualNode(path: TreePath, message: String) -> Builder`: Logs extra actual node with message.

  - `addExtraActualNode(path: TreePath) -> Builder`: Logs extra actual node.

  - `addDifferingNodes(expectedPath: TreePath, actualPath: TreePath) -> Builder`: Logs differing nodes.

  - `addDifferingNodes(expectedPath: TreePath, actualPath: TreePath, message: String) -> Builder`: Logs differing nodes with message.

  - `build() -> TreeDifference`: Builds and returns the TreeDifference.

- `TreeDifference.OneWayDiff`: Describes an extra node on expected or actual tree.

  - `OneWayDiff(path: TreePath, message: String) -> OneWayDiff`: Package-private constructor.

  - `getPath() -> TreePath`: Returns the TreePath.

  - `getMessage() -> String`: Returns contextual details about the diff.

- `TreeDifference.TwoWayDiff`: Describes a difference between corresponding nodes.

  - `TwoWayDiff(expectedPath: TreePath, actualPath: TreePath, message: String) -> TwoWayDiff`: Package-private constructor.

  - `getExpectedPath() -> TreePath`: Returns the expected TreePath.

  - `getActualPath() -> TreePath`: Returns the actual TreePath.

  - `getMessage() -> String`: Returns contextual details about the diff.

---

`TypeEnumerator.java`:

- `TypeEnumerator`: Provides information about types declared in a CompilationUnitTree.

  - `TypeEnumerator() -> TypeEnumerator`: Private constructor preventing instantiation.

  - `getTopLevelTypes(compilationUnit: CompilationUnitTree) -> ImmutableSet<String>`: Static method returning fully qualified names of all types declared in the compilation unit.

- `TypeEnumerator.TypeScanner`: TreeScanner for determining type declarations.

  - `TypeScanner() -> TypeScanner`: Package-private constructor.

  - `reduce(existingSet: Set<String>, newSet: Set<String>) -> Set<String>`: Override ensuring non-null return value and combining sets.

  - `visitClass(classTree: ClassTree, p: Void) -> Set<String>`: Override extracting class name and scanning members.

  - `visitNewClass(newClassTree: NewClassTree, p: Void) -> Set<String>`: Override scanning the expression.

  - `visitIdentifier(idTree: IdentifierTree, p: Void) -> Set<String>`: Override extracting identifier name.

  - `visitMemberSelect(memberSelectTree: MemberSelectTree, p: Void) -> Set<String>`: Override building fully qualified name from member select.

  - `visitCompilationUnit(compilationUnit: CompilationUnitTree, p: Void) -> Set<String>`: Override extracting package name and combining with type declarations.

---

`package-info.java`:

This file contains package-level documentation and annotations for the `com.google.testing.compile` package. It describes the purpose and usage of the package for testing Java source compilation in unit tests.

**Package Documentation:**

The package provides tools for:
- Compiling Java source code in tests
- Making assertions about compilation results
- Testing annotation processors
- Verifying generated files
- Testing diagnostic messages

**Main Classes:**
- `Compiler`: For compiling source files
- `Compilation`: Represents compilation results
- `CompilationSubject`: For making Truth assertions about compilations
- `JavaSourcesSubject`: For fluent assertion API

**Annotations Applied:**
- `@CheckReturnValue`: Applied to the package
- `@ParametersAreNonnullByDefault`: Applied to the package
