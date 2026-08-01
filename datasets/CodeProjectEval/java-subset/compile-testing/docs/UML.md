```mermaid
classDiagram
direction BT
class BreadcrumbVisitor {
  - kindString(Tree) String
  + visitImport(ImportTree, Void) String
  + visitContinue(ContinueTree, Void) String
  + visitMemberSelect(MemberSelectTree, Void) String
  + visitTypeParameter(TypeParameterTree, Void) String
  + visitLiteral(LiteralTree, Void) String
  + visitVariable(VariableTree, Void) String
  + visitPrimitiveType(PrimitiveTypeTree, Void) String
  + defaultAction(Tree, Void) String
  + visitLabeledStatement(LabeledStatementTree, Void) String
  + visitClass(ClassTree, Void) String
  - detailedKindString(Tree, Object) String
  + visitMethod(MethodTree, Void) String
  + visitBlock(BlockTree, Void) String
  + visitIdentifier(IdentifierTree, Void) String
  + visitModifiers(ModifiersTree, Void) String
  + visitBreak(BreakTree, Void) String
  + BreadcrumbVisitor() 
}
class Breadcrumbs {
  ~ describeTreePath(TreePath) String
  ~ getBreadcrumbList(TreePath) List~String~
  - Breadcrumbs() 
}
class Builder {
  ~ addExtraExpectedNode(TreePath) Builder
  ~ addExtraActualNode(TreePath, String) Builder
  ~ build() TreeDifference
  ~ addExtraExpectedNode(TreePath, String) Builder
  ~ addExtraActualNode(TreePath) Builder
  ~ addDifferingNodes(TreePath, TreePath) Builder
  ~ addDifferingNodes(TreePath, TreePath, String) Builder
  ~ Builder() 
}
class ChainingClause~T~ {
<<Interface>>
  + and() T
}
class CleanCompilationBuilder {
  ~ CleanCompilationBuilder(Compilation) 
}
class CleanCompilationClause {
<<Interface>>

}
class ColumnClause~T~ {
<<Interface>>
  + atColumn(long) ChainingClause~T~
}
class Compilation {
  ~ describeGeneratedSourceFiles() String
  - describeGeneratedFile(JavaFileObject) String
  + notes() ImmutableList~Diagnostic~JavaFileObject~~
  - toImmutableList() Collector~T, ?, ImmutableList~T~~
  + compiler() Compiler
  + generatedSourceFile(String) Optional~JavaFileObject~
  + toString() String
  + warnings() ImmutableList~Diagnostic~JavaFileObject~~
  + status() Status
  + generatedFile(Location, String, String) Optional~JavaFileObject~
  + diagnostics() ImmutableList~Diagnostic~JavaFileObject~~
  + generatedFiles() ImmutableList~JavaFileObject~
  + errors() ImmutableList~Diagnostic~JavaFileObject~~
  ~ diagnosticsOfKind(Kind, Kind[]) ImmutableList~Diagnostic~JavaFileObject~~
  + generatedSourceFiles() ImmutableList~JavaFileObject~
  + generatedFile(Location, String) Optional~JavaFileObject~
  ~ describeFailureDiagnostics() String
  + sourceFiles() ImmutableList~JavaFileObject~
  ~ Compilation(Compiler, Iterable~JavaFileObject~, boolean, Iterable~Diagnostic~JavaFileObject~~, Iterable~JavaFileObject~) 
}
class CompilationBuilder {
  ~ CompilationBuilder(Compilation) 
}
class CompilationClause {
  + compilesWithoutError() SuccessfulCompilationClause
  - failWithCandidate(JavaFileObject, JavaFileObject, String) void
  + failsToCompile() UnsuccessfulCompilationClause
  + compilesWithoutWarnings() CleanCompilationClause
  - compilation() Compilation
  - failNoCandidates(ImmutableSet~String~, CompilationUnitTree, ImmutableList~TypedCompilationUnit~) void
  + parsesAs(JavaFileObject, JavaFileObject[]) void
  - CompilationClause() 
  - CompilationClause(Iterable~Processor~) 
}
class CompilationFailureException {
  ~ CompilationFailureException(Compilation) 
}
class CompilationRule {
  - Types types
  - Elements elements
   Types types
   Elements elements
  + apply(Statement, Description) Statement
  + CompilationRule() 
}
class CompilationSubject {
  - kindSingular(Kind) String
  - hadDiagnosticContainingMatch(String, Pattern, Kind, Kind[]) DiagnosticInFile
  - findMatchingDiagnostics(String, Pattern, Kind, Kind[]) ImmutableList~Diagnostic~JavaFileObject~~
  + hadNoteContainingMatch(String) DiagnosticInFile
  + hadWarningContaining(String) DiagnosticInFile
  + hadNoteCount(int) void
  + succeeded() void
  - messageListing(Iterable~Diagnostic~?~~, String, Object[]) String
  - hadDiagnosticContainingMatch(String, Kind, Kind[]) DiagnosticInFile
  - hadDiagnosticContainingMatch(Pattern, Kind, Kind[]) DiagnosticInFile
  + succeededWithoutWarnings() void
  + generatedFile(Location, String) JavaFileObjectSubject
  + generatedFile(Location, String, String) JavaFileObjectSubject
  - kindPlural(Kind) String
  + hadWarningContainingMatch(String) DiagnosticInFile
  + hadNoteContainingMatch(Pattern) DiagnosticInFile
  + hadErrorContainingMatch(String) DiagnosticInFile
  - toImmutableList() Collector~T, ?, ImmutableList~T~~
  - checkGeneratedFile(Optional~JavaFileObject~, Location, String) JavaFileObjectSubject
  - actualNotNull() Compilation
  - hadDiagnosticContaining(String, Kind, Kind[]) DiagnosticInFile
  + compilations() Factory~CompilationSubject, Compilation~
  + failed() void
  + hadErrorCount(int) void
  + hadWarningContainingMatch(Pattern) DiagnosticInFile
  + hadNoteContaining(String) DiagnosticInFile
  + assertThat(Compilation) CompilationSubject
  + generatedSourceFile(String) JavaFileObjectSubject
  + hadErrorContaining(String) DiagnosticInFile
  - checkDiagnosticCount(int, Kind, Kind[]) void
  - toImmutableSet() Collector~T, ?, ImmutableSet~T~~
  + hadErrorContainingMatch(Pattern) DiagnosticInFile
  + hadWarningCount(int) void
  ~ CompilationSubject(FailureMetadata, Compilation) 
}
class CompilationSubjectFactory {
  + createSubject(FailureMetadata, Compilation) CompilationSubject
  + CompilationSubjectFactory() 
}
class CompilationWithNotesClause~T~ {
<<Interface>>
  + withNoteContaining(String) FileClause~T~
  + withNoteCount(int) T
}
class CompilationWithWarningsBuilder~T~ {
  + withErrorContaining(String) FileClause~T~
  + withWarningContaining(String) FileClause~T~
  # thisObject() T
  + withWarningCount(int) T
  + withNoteCount(int) T
  + withNoteContaining(String) FileClause~T~
  + withErrorCount(int) T
  # CompilationWithWarningsBuilder(Compilation) 
}
class CompilationWithWarningsClause~T~ {
<<Interface>>
  + withWarningCount(int) T
  + withWarningContaining(String) FileClause~T~
}
class CompileTester {
<<Interface>>
  + compilesWithoutError() SuccessfulCompilationClause
  + failsToCompile() UnsuccessfulCompilationClause
  + compilesWithoutWarnings() CleanCompilationClause
  + parsesAs(JavaFileObject, JavaFileObject[]) void
}
class Compiler {
  ~ ClassLoader platformClassLoader
   ClassLoader? platformClassLoader
  + options() ImmutableList~String~
  + withClasspathFrom(ClassLoader) Compiler
  + withOptions(Object[]) Compiler
  + withAnnotationProcessorPath(Iterable~File~) Compiler
  + processors() ImmutableList~Processor~
  + annotationProcessorPath() Optional~ImmutableList~File~~
  - standardFileManager(DiagnosticCollector~JavaFileObject~) StandardJavaFileManager
  ~ javaCompiler() JavaCompiler
  + compile(Iterable~JavaFileObject~) Compilation
  + withProcessors(Iterable~Processor~) Compiler
  + withClasspath(Iterable~File~) Compiler
  + withProcessors(Processor[]) Compiler
  + withOptions(Iterable~Object~) Compiler
  + classPath() Optional~ImmutableList~File~~
  - setLocation(InMemoryJavaFileManager, StandardLocation, ImmutableList~File~) void
  + javac() Compiler
  + compile(JavaFileObject[]) Compilation
  - copy(ImmutableList~Processor~, ImmutableList~String~, Optional~ImmutableList~File~~, Optional~ImmutableList~File~~) Compiler
  + compiler(JavaCompiler) Compiler
  - getClasspathFromClassloader(ClassLoader) ImmutableList~File~
  + Compiler() 
}
class DiagnosticAssertions {
  ~ filterDiagnostics(Predicate~Diagnostic~JavaFileObject~~) ImmutableList~Diagnostic~JavaFileObject~~
  ~ mapDiagnostics(Function~Diagnostic~JavaFileObject~, T~) Stream~T~
  # failExpectingMatchingDiagnostic(String, Object[]) void
  ~ DiagnosticAssertions(String, Iterable~Diagnostic~JavaFileObject~~) 
  ~ DiagnosticAssertions(DiagnosticAssertions, Iterable~Diagnostic~JavaFileObject~~) 
}
class DiagnosticAtColumn {
  - columnsWithDiagnostics() ImmutableSet~String~
  + atColumn(long) void
  - DiagnosticAtColumn(DiagnosticAssertions, LinesInFile, long, ImmutableList~Diagnostic~JavaFileObject~~) 
}
class DiagnosticInFile {
  - sourceFilesWithDiagnostics() ImmutableSet~String~
  + inFile(JavaFileObject) DiagnosticOnLine
  - findDiagnosticsInFile(JavaFileObject) ImmutableList~Diagnostic~JavaFileObject~~
  - DiagnosticInFile(String, Iterable~Diagnostic~JavaFileObject~~) 
}
class DiagnosticOnLine {
  + onLineContaining(String) void
  + onLine(long) DiagnosticAtColumn
  - findLineContainingSubstring(String) long
  - findMatchingDiagnosticsOnLine(long) ImmutableList~Diagnostic~JavaFileObject~~
  - DiagnosticOnLine(DiagnosticAssertions, JavaFileObject, ImmutableList~Diagnostic~JavaFileObject~~) 
}
class DiffVisitor {
  - namesEqual(Name, Name) boolean
  - parallelScan(Iterable~Tree~, Iterable~Tree~) void
  - expectedPathPlus(Tree) TreePath
  + addTypeMismatch(Tree, Tree) void
  - isIterableOfTree(Type) boolean
  - reportDiff(String, Object[]) void
  - actualPathPlus(Tree) TreePath
  + visitOther(Tree, Tree) Void
  - defaultCompare(Method, Kind, Object, Object) void
  + defaultAction(Tree, Tree) Void?
  - scan(Tree, Tree) void
  - filterActual(Method, Kind, Iterable~Tree~, Iterable~Tree~) Iterable~Tree~
  - pushPathAndAccept(Tree, Tree) Void
  ~ DiffVisitor(Builder, TreeFilter) 
  - DiffVisitor(Builder, TreeFilter, TreePath, TreePath) 
}
class EvaluatingProcessor {
   SourceVersion supportedSourceVersion
   Set~String~ supportedAnnotationTypes
  + init(ProcessingEnvironment) void
  + process(Set~TypeElement~, RoundEnvironment) boolean
  ~ throwIfStatementThrew() void
  ~ EvaluatingProcessor(Statement) 
}
class FileBuilder {
  + and() T
  + in(JavaFileObject) LineClause~T~
  - FileBuilder(DiagnosticInFile) 
}
class FileClause~T~ {
<<Interface>>
  + in(JavaFileObject) LineClause~T~
}
class ForwardingStandardJavaFileManager {
  + setLocation(Location, Iterable~File~) void
  + getJavaFileObjectsFromStrings(Iterable~String~) Iterable~JavaFileObject~
  + getLocation(Location) Iterable~File~
  + getJavaFileObjectsFromFiles(Iterable~File~) Iterable~JavaFileObject~
  + getJavaFileObjects(String[]) Iterable~JavaFileObject~
  + getJavaFileObjects(File[]) Iterable~JavaFileObject~
  + setLocationFromPaths(Location, Collection~Path~) void
  # ForwardingStandardJavaFileManager(StandardJavaFileManager) 
}
class GeneratedCompilationBuilder~T~ {
  + generatesFiles(JavaFileObject, JavaFileObject[]) T
  ~ wasGenerated(JavaFileObject) boolean
  + and() GeneratedPredicateClause~T~
  + generatesSources(JavaFileObject, JavaFileObject[]) T
  + generatesFileNamed(Location, String, String) SuccessfulFileClause~T~
  # GeneratedCompilationBuilder(Compilation) 
}
class GeneratedPredicateClause~T~ {
<<Interface>>
  + generatesSources(JavaFileObject, JavaFileObject[]) T
  + generatesFiles(JavaFileObject, JavaFileObject[]) T
  + generatesFileNamed(Location, String, String) SuccessfulFileClause~T~
}
class InMemoryJavaFileManager {
   ImmutableList~JavaFileObject~ generatedSources
   ImmutableList~JavaFileObject~ outputFiles
  + getJavaFileForOutput(Location, String, Kind, FileObject) JavaFileObject
  ~ addSourceFiles(Iterable~JavaFileObject~) void
  - uriForFileObject(Location, String, String) URI
  + getFileForInput(Location, String, String) FileObject
  + isSameFile(FileObject, FileObject) boolean
  - findInMemoryInput(String, String) Optional~JavaFileObject~
  - uriForJavaFileObject(Location, String, Kind) URI
  + getJavaFileForInput(Location, String, Kind) JavaFileObject
  - findInMemoryInput(String) Optional~JavaFileObject~
  + getFileForOutput(Location, String, String, FileObject) FileObject
  ~ InMemoryJavaFileManager(StandardJavaFileManager) 
}
class InMemoryJavaFileObject {
  - long lastModified
   long lastModified
  + openOutputStream() OutputStream
  + delete() boolean
  + openReader(boolean) Reader
  + getCharContent(boolean) CharSequence
  + openWriter() Writer
  + toString() String
  + openInputStream() InputStream
  ~ InMemoryJavaFileObject(URI) 
}
class JarFileJavaFileObject {
  ~ getPathUri(URL) URI
  ~ JarFileJavaFileObject(URL) 
}
class JavaFileObjectSubject {
  - performTreeDifference(JavaFileObject, String, String, BiFunction~ParseResult, ParseResult, TreeDifference~) void
  + assertThat(JavaFileObject) JavaFileObjectSubject
  + contentsAsString(Charset) StringSubject
  + contentsAsUtf8String() StringSubject
  # actualCustomStringRepresentation() String
  + isEqualTo(Object) void
  + hasSourceEquivalentTo(JavaFileObject) void
  + javaFileObjects() Factory~JavaFileObjectSubject, JavaFileObject~
  + hasContents(ByteSource) void
  + containsElementsIn(JavaFileObject) void
  - actualNotNull() JavaFileObject
  ~ JavaFileObjectSubject(FailureMetadata, JavaFileObject) 
}
class JavaFileObjectSubjectFactory {
  + createSubject(FailureMetadata, JavaFileObject) JavaFileObjectSubject
  + JavaFileObjectSubjectFactory() 
}
class JavaFileObjects {
  + forResource(URL) JavaFileObject
  ~ deduceKind(URI) Kind
  + forSourceLines(String, String[]) JavaFileObject
  ~ asByteSource(JavaFileObject) ByteSource
  + forSourceString(String, String) JavaFileObject
  + forResource(String) JavaFileObject
  + forSourceLines(String, Iterable~String~) JavaFileObject
  - JavaFileObjects() 
}
class JavaSourceSubjectFactory {
  + javaSource() JavaSourceSubjectFactory
  + createSubject(FailureMetadata, JavaFileObject) SingleSourceAdapter
  - JavaSourceSubjectFactory() 
}
class JavaSourcesSubject {
  + withCompilerOptions(String[]) JavaSourcesSubject
  + parsesAs(JavaFileObject, JavaFileObject[]) void
  + withCompilerOptions(Iterable~String~) JavaSourcesSubject
  + compilesWithoutWarnings() CleanCompilationClause
  + withClasspathFrom(ClassLoader) JavaSourcesSubject
  + withClasspath(Iterable~File~) JavaSourcesSubject
  - actualNotNull() Iterable~JavaFileObject~
  - toImmutableList() Collector~T, ?, ImmutableList~T~~
  + processedWith(Iterable~Processor~) CompileTester
  - newCompilationClause(Iterable~Processor~) CompilationClause
  + assertThat(JavaFileObject, JavaFileObject[]) JavaSourcesSubject
  + failsToCompile() UnsuccessfulCompilationClause
  + assertThat(JavaFileObject) JavaSourcesSubject
  + processedWith(Processor, Processor[]) CompileTester
  + compilesWithoutError() SuccessfulCompilationClause
  ~ JavaSourcesSubject(FailureMetadata, Iterable~JavaFileObject~) 
}
class JavaSourcesSubjectFactory {
  + javaSources() JavaSourcesSubjectFactory
  + createSubject(FailureMetadata, Iterable~JavaFileObject~) JavaSourcesSubject
  - JavaSourcesSubjectFactory() 
}
class LineClause~T~ {
<<Interface>>
  + onLine(long) ColumnClause~T~
}
class LinesInFile {
  ~ linesInFile() ImmutableList~String~
  ~ toLineList() Collector~Long, ?, String~
  ~ listLine(long) String
  ~ fileName() String
  ~ LinesInFile(JavaFileObject) 
}
class MatchExpectedTreesFilter {
  - fullyQualifiedImport(ImportTree) String
  + filterActualMembers(ImmutableList~Tree~, ImmutableList~Tree~) ImmutableList~Tree~
  + filterImports(ImmutableList~ImportTree~, ImmutableList~ImportTree~) ImmutableList~ImportTree~
  ~ MatchExpectedTreesFilter(CompilationUnitTree, Trees, CompilationUnitTree, Trees) 
}
class MethodSignature {
  ~ create(CompilationUnitTree, MethodTree, Trees) MethodSignature
  ~ name() String
  ~ parameterTypes() ImmutableList~Wrapper~TypeMirror~~
  + MethodSignature() 
}
class MoreTrees {
  ~ parseLinesToTree(Iterable~String~) CompilationUnitTree
  ~ findSubtreePath(CompilationUnitTree, Kind, String) TreePath
  ~ findSubtree(CompilationUnitTree, Kind) Tree
  ~ findSubtree(CompilationUnitTree, Kind, String) Tree
  ~ findSubtreePath(CompilationUnitTree, Kind) TreePath
  ~ parseLines(String[]) ParseResult
  ~ parseLinesToTree(String[]) CompilationUnitTree
  ~ parseLines(Iterable~String~) ParseResult
  + MoreTrees() 
}
class OneWayDiff {
  - String details
  - TreePath nodePath
   String details
   TreePath nodePath
  ~ OneWayDiff(TreePath, String) 
}
class ParseResult {
  ~ diagnosticsByKind() ImmutableListMultimap~Kind, Diagnostic~JavaFileObject~~
  ~ compilationUnits() ImmutableList~CompilationUnitTree~
  ~ trees() Trees
  ~ ParseResult(ImmutableListMultimap~Kind, Diagnostic~JavaFileObject~~, Iterable~CompilationUnitTree~, Trees) 
}
class Parser {
  ~ parse(Iterable~JavaFileObject~, String) ParseResult
  - foundParseErrors(List~Diagnostic~JavaFileObject~~) boolean
  - sortDiagnosticsByKind(Iterable~Diagnostic~JavaFileObject~~) ImmutableListMultimap~Kind, Diagnostic~JavaFileObject~~
  - Parser() 
}
class ProcessedCompileTesterFactory {
<<Interface>>
  + processedWith(Processor, Processor[]) CompileTester
  + withClasspathFrom(ClassLoader) ProcessedCompileTesterFactory
  + processedWith(Iterable~Processor~) CompileTester
  + withCompilerOptions(Iterable~String~) ProcessedCompileTesterFactory
  + withCompilerOptions(String[]) ProcessedCompileTesterFactory
  + withClasspath(Iterable~File~) ProcessedCompileTesterFactory
}
class ResourceSourceJavaFileObject {
  + openInputStream() InputStream
  + openReader(boolean) Reader
  + getCharContent(boolean) CharSequence
  ~ ResourceSourceJavaFileObject(URL) 
  ~ ResourceSourceJavaFileObject(URL, URI) 
}
class SearchScanner {
  - isMatch(Tree, Optional~Object~) boolean
  + visitMemberSelect(MemberSelectTree, Void) Optional~TreePath~
  + scan(Tree, Void) Optional~TreePath~
  + visitClass(ClassTree, Void) Optional~TreePath~
  + visitVariable(VariableTree, Void) Optional~TreePath~
  + visitIdentifier(IdentifierTree, Void) Optional~TreePath~
  + visitMethod(MethodTree, Void) Optional~TreePath~
  + scan(Iterable~Tree~, Void) Optional~TreePath~
  + visitBreak(BreakTree, Void) Optional~TreePath~
  + visitTypeParameter(TypeParameterTree, Void) Optional~TreePath~
  - absentIfNull(Optional~TreePath~) Optional~TreePath~
  + visitContinue(ContinueTree, Void) Optional~TreePath~
  - isMatch(Tree, Object) boolean
  + visitLabeledStatement(LabeledStatementTree, Void) Optional~TreePath~
  + visitLiteral(LiteralTree, Void) Optional~TreePath~
  - currentPathPlus(Tree) Optional~TreePath~
  + reduce(Optional~TreePath~, Optional~TreePath~) Optional~TreePath~
  + SearchScanner(Kind, Optional~String~) 
}
class SingleSourceAdapter {
  + withClasspath(Iterable~File~) JavaSourcesSubject
  + processedWith(Iterable~Processor~) CompileTester
  + failsToCompile() UnsuccessfulCompilationClause
  + parsesAs(JavaFileObject, JavaFileObject[]) void
  + withClasspathFrom(ClassLoader) JavaSourcesSubject
  + compilesWithoutError() SuccessfulCompilationClause
  + withCompilerOptions(String[]) JavaSourcesSubject
  + processedWith(Processor, Processor[]) CompileTester
  + compilesWithoutWarnings() CleanCompilationClause
  + withCompilerOptions(Iterable~String~) JavaSourcesSubject
  ~ SingleSourceAdapter(FailureMetadata, JavaFileObject) 
}
class Status {
<<enumeration>>
  + values() Status[]
  + valueOf(String) Status
  + Status() 
}
class StringSourceJavaFileObject {
  ~ long lastModified
   long lastModified
  + openInputStream() InputStream
  + openWriter() Writer
  + openReader(boolean) Reader
  + openOutputStream() OutputStream
  ~ createUri(String) URI
  + getCharContent(boolean) CharSequence
  ~ StringSourceJavaFileObject(String, String) 
}
class SuccessfulCompilationBuilder {
  ~ SuccessfulCompilationBuilder(Compilation) 
}
class SuccessfulCompilationClause {
<<Interface>>

}
class SuccessfulFileClause~T~ {
<<Interface>>
  + withStringContents(Charset, String) SuccessfulFileClause~T~
  + withContents(ByteSource) SuccessfulFileClause~T~
}
class TreeContext {
  - CompilationUnitTree compilationUnit
  - Trees trees
   Trees trees
   CompilationUnitTree compilationUnit
  ~ getNodeEndColumn(Tree) long
  ~ getNodePath(Tree) TreePath
  ~ getNodeStartLine(Tree) long
  ~ getNodeStartColumn(Tree) long
  ~ getNodeStartPosition(Tree) long
  ~ getNodeEndPosition(Tree) long
  ~ getNodeEndLine(Tree) long
  ~ TreeContext(CompilationUnitTree, Trees) 
}
class TreeDiffer {
  ~ diffSubtrees(TreePath, TreePath) TreeDifference
  ~ diffCompilationUnits(CompilationUnitTree, CompilationUnitTree) TreeDifference
  - createDiff(CompilationUnitTree, CompilationUnitTree, TreeFilter) TreeDifference
  ~ matchCompilationUnits(CompilationUnitTree, Trees, CompilationUnitTree, Trees) TreeDifference
  - TreeDiffer() 
}
class TreeDifference {
  - ImmutableList~TwoWayDiff~ differingNodes
  - ImmutableList~OneWayDiff~ extraActualNodes
  - ImmutableList~OneWayDiff~ extraExpectedNodes
   boolean empty
   String diffReport
   ImmutableList~OneWayDiff~ extraExpectedNodes
   ImmutableList~TwoWayDiff~ differingNodes
   ImmutableList~OneWayDiff~ extraActualNodes
  - createMessage(String, TreePath, TreeContext, TreePath, TreeContext) String
  - createMessage(String, TreePath, TreeContext, boolean) String
  - nodeContents(Tree) String
  ~ getDiffReport(TreeContext, TreeContext) String
  ~ TreeDifference(ImmutableList~OneWayDiff~, ImmutableList~OneWayDiff~, ImmutableList~TwoWayDiff~) 
  ~ TreeDifference() 
}
class TreeFilter {
<<Interface>>
  + filterActualMembers(ImmutableList~Tree~, ImmutableList~Tree~) ImmutableList~Tree~
  + filterImports(ImmutableList~ImportTree~, ImmutableList~ImportTree~) ImmutableList~ImportTree~
}
class TwoWayDiff {
  - TreePath actualNodePath
  - String details
  - TreePath expectedNodePath
   String details
   TreePath actualNodePath
   TreePath expectedNodePath
  ~ TwoWayDiff(TreePath, TreePath, String) 
}
class TypeEnumerator {
  ~ getTopLevelTypes(CompilationUnitTree) ImmutableSet~String~
  - TypeEnumerator() 
}
class TypeScanner {
  + visitMemberSelect(MemberSelectTree, Void) Set~String~
  + visitClass(ClassTree, Void) Set~String~
  + scan(Tree, Void) Set~String~
  + reduce(Set~String~, Set~String~) Set~String~
  + visitIdentifier(IdentifierTree, Void) Set~String~
  + visitExpressionStatement(ExpressionStatementTree, Void) Set~String~
  + visitCompilationUnit(CompilationUnitTree, Void) Set~String~
  + TypeScanner() 
}
class TypedCompilationUnit {
  ~ types() ImmutableSet~String~
  ~ tree() CompilationUnitTree
  ~ create(CompilationUnitTree) TypedCompilationUnit
  + TypedCompilationUnit() 
}
class UnsuccessfulCompilationBuilder {
  ~ UnsuccessfulCompilationBuilder(Compilation) 
}
class UnsuccessfulCompilationClause {
<<Interface>>
  + withErrorCount(int) UnsuccessfulCompilationClause
  + withErrorContaining(String) FileClause~UnsuccessfulCompilationClause~
}

Breadcrumbs  -->  BreadcrumbVisitor 
TreeDifference  -->  Builder 
CompileTester  -->  ChainingClause~T~ 
CleanCompilationBuilder  -->  GeneratedCompilationBuilder~T~ 
JavaSourcesSubject  -->  CleanCompilationBuilder 
CleanCompilationClause  -->  ChainingClause~T~ 
CleanCompilationClause  -->  CompilationWithNotesClause~T~ 
CompileTester  -->  CleanCompilationClause 
ColumnClause~T~  -->  ChainingClause~T~ 
CompileTester  -->  ColumnClause~T~ 
CompilationBuilder  -->  GeneratedCompilationBuilder~T~ 
JavaSourcesSubject  -->  CompilationBuilder 
JavaSourcesSubject  -->  CompilationClause 
CompileTester  -->  CompilationWithNotesClause~T~ 
JavaSourcesSubject  -->  CompilationWithWarningsBuilder~T~ 
CompilationWithWarningsClause~T~  -->  CompilationWithNotesClause~T~ 
CompileTester  -->  CompilationWithWarningsClause~T~ 
CompilationSubject  -->  DiagnosticAssertions 
CompilationSubject  -->  DiagnosticAtColumn 
DiagnosticAtColumn  -->  DiagnosticAssertions 
CompilationSubject  -->  DiagnosticInFile 
DiagnosticInFile  -->  DiagnosticAssertions 
CompilationSubject  -->  DiagnosticOnLine 
DiagnosticOnLine  -->  DiagnosticAssertions 
TreeDiffer  -->  DiffVisitor 
CompilationRule  -->  EvaluatingProcessor 
CompilationWithWarningsBuilder~T~  -->  FileBuilder 
FileClause~T~  -->  ChainingClause~T~ 
CompileTester  -->  FileClause~T~ 
GeneratedCompilationBuilder~T~  -->  CompilationWithWarningsBuilder~T~ 
JavaSourcesSubject  -->  GeneratedCompilationBuilder~T~ 
CompileTester  -->  GeneratedPredicateClause~T~ 
InMemoryJavaFileManager  -->  InMemoryJavaFileObject 
JavaFileObjects  -->  JarFileJavaFileObject 
LineClause~T~  -->  ChainingClause~T~ 
CompileTester  -->  LineClause~T~ 
CompilationSubject  -->  LinesInFile 
TreeDiffer  -->  MatchExpectedTreesFilter 
MatchExpectedTreesFilter  ..>  TreeFilter 
TreeDiffer  -->  MethodSignature 
TreeDifference  -->  OneWayDiff 
Parser  -->  ParseResult 
JavaFileObjects  -->  ResourceSourceJavaFileObject 
MoreTrees  -->  SearchScanner 
JavaSourcesSubject  -->  SingleSourceAdapter 
Compilation  -->  Status 
JavaFileObjects  -->  StringSourceJavaFileObject 
SuccessfulCompilationBuilder  -->  GeneratedCompilationBuilder~T~ 
JavaSourcesSubject  -->  SuccessfulCompilationBuilder 
SuccessfulCompilationClause  -->  ChainingClause~T~ 
SuccessfulCompilationClause  -->  CompilationWithWarningsClause~T~ 
CompileTester  -->  SuccessfulCompilationClause 
SuccessfulFileClause~T~  -->  ChainingClause~T~ 
CompileTester  -->  SuccessfulFileClause~T~ 
TreeDiffer  -->  TreeFilter 
TreeDifference  -->  TwoWayDiff 
TypeEnumerator  -->  TypeScanner 
JavaSourcesSubject  -->  TypedCompilationUnit 
UnsuccessfulCompilationBuilder  -->  CompilationWithWarningsBuilder~T~ 
JavaSourcesSubject  -->  UnsuccessfulCompilationBuilder 
UnsuccessfulCompilationClause  -->  CompilationWithWarningsClause~T~ 
CompileTester  -->  UnsuccessfulCompilationClause 

```