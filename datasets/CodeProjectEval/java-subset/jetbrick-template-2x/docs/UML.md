``` mermaid
classDiagram
direction BT
class ALU {
  + plus(Object, Object) Object
  + ushr(Object, Object) Object
  + getNumberType(Class~?~) int
  + bitOr(Object, Object) Object
  + shl(Object, Object) Object
  + equals(Object, Object) Boolean
  + minus(Object, Object) Object
  + positive(Object) Object
  + shr(Object, Object) Object
  + isTrue(Object) boolean
  + negative(Object) Object
  + bitXor(Object, Object) Object
  + getNumberType(Class~?~, Class~?~) int
  + lt(Object, Object) Object
  + le(Object, Object) Object
  + gt(Object, Object) Object
  + bitAnd(Object, Object) Object
  + ge(Object, Object) Object
  + div(Object, Object) Object
  + mod(Object, Object) Object
  + mul(Object, Object) Object
  + bitNot(Object) Object
  + ALU() 
}
class ALUGetNumberTypeTest {
  + testNumberType_double() void
  + testNumberType_short() void
  + testNumberType_long() void
  + testNumberType() void
  + testNumberType_int() void
  + testNumberType_float() void
  + testNumberType_byte() void
  + ALUGetNumberTypeTest() 
}
class ALUTest {
  + testMinis() void
  + testPlus() void
  + testMul() void
  + testDiv() void
  + ALUTest() 
}
class AbstractJetxTest {
  + destory() void
  # eval(Map~String, Object~) String
  # eval(JetTemplate, Map~String, Object~) String
  # errbefore(String) String
  # initializeConfig() void
  # eval(String) String
  # initializeEngine() void
  + initialize() void
  # str(Object) String
  # err(String) String
  # eval() String
  # eval(String, Map~String, Object~) String
  + AbstractJetxTest() 
}
class AbstractResourceLoader {
  # String root
  # boolean reloadable
  # JetSecurityManager securityManager
   boolean reloadable
   String root
   JetSecurityManager securityManager
  + AbstractResourceLoader() 
}
class ArrayLengthGetter {
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
  + ArrayLengthGetter() 
}
class AstBuilder {
  + create(Source, ParserContext) AstTemplate
  + AstBuilder() 
}
class AstCodeVisitor {
  - accept(ParseTree) T
  + visitDirective_continue(Directive_continueContext) AstDirectiveContinue
  - getJavaString(String, ParserRuleContext) String
  + visitValue(ValueContext) AstNode
  + visitExpression_method(Expression_methodContext) AstNode
  + visitExpression_index_get(Expression_index_getContext) AstNode
  + visitHash_map_entry(Hash_map_entryContext) AstConstantMapEntry
  + visitExpression_ternary_operator(Expression_ternary_operatorContext) AstNode
  + visitExpression_unary_operator(Expression_unary_operatorContext) AstNode
  - validateInsideOfDirectiveFor(ParserRuleContext, String) void
  + visitExpression_list(Expression_listContext) AstExpressionList
  - pos(ParserRuleContext, int) Position
  + visitExpression_new_array(Expression_new_arrayContext) AstNode
  + visitExpression_constant(Expression_constantContext) AstNode
  + visitExpression_field_static(Expression_field_staticContext) AstNode
  + visitDirective_tag(Directive_tagContext) AstNode
  + visitDirective_if(Directive_ifContext) AstDirectiveIf
  + visitExpression_nullsafe_operator(Expression_nullsafe_operatorContext) AstNode
  + visitExpression_new_object(Expression_new_objectContext) AstNode
  - pos(Object) Position
  + visitTemplate(TemplateContext) AstTemplate
  + visitExpression_method_static(Expression_method_staticContext) AstNode
  + visitDirective_set(Directive_setContext) AstStatementList
  + visitDirective_macro(Directive_macroContext) AstNode
  + visitIdentifier(IdentifierContext) AstIdentifier
  + visitDirective_define_expression(Directive_define_expressionContext) AstNode?
  + visitDirective_define(Directive_defineContext) AstNode
  + visitType(TypeContext) AstType
  + visitDirective_stop(Directive_stopContext) AstNode
  + visitConstant(ConstantContext) AstConstant
  + visitExpression_instanceof(Expression_instanceofContext) AstNode
  + visitDirective_macro_arguments(Directive_macro_argumentsContext) AstNode?
  + visitDirective(DirectiveContext) AstNode
  + visitExpression_hash_map(Expression_hash_mapContext) AstExpression
  - validateIdentifier(String, boolean, ParseTree) void
  + visitBlock(BlockContext) AstStatementList
  + visitDirective_for(Directive_forContext) AstDirectiveFor
  + visitDirective_call(Directive_callContext) AstNode
  + visitDirective_invalid(Directive_invalidContext) AstNode
  + visitDirective_include(Directive_includeContext) AstNode
  + visitExpression_array_list(Expression_array_listContext) AstExpression
  + visitText(TextContext) AstText
  + visitDirective_elseif(Directive_elseifContext) AstDirectiveIf
  + visitExpression_binary_operator(Expression_binary_operatorContext) AstNode
  - resolveClass(AstType) Class~?~
  + visitDirective_break(Directive_breakContext) AstDirectiveBreak
  + visitDirective_return(Directive_returnContext) AstNode
  + visitDirective_options_expression(Directive_options_expressionContext) AstNode?
  + visitDirective_set_expression(Directive_set_expressionContext) AstStatement
  + visitExpression_function(Expression_functionContext) AstNode
  + visitDirective_options(Directive_optionsContext) AstNode
  - accept(List~ParseTree~) List~T~
  + visitExpression_field(Expression_fieldContext) AstNode
  + visitExpression_primary(Expression_primaryContext) AstNode
  + visitExpression_identifier(Expression_identifierContext) AstNode
  + visitDirective_else(Directive_elseContext) AstNode
  + AstCodeVisitor(ParserContext) 
}
class AstConstant {
  - Object value
   Object value
  + toString() String
  + execute(InterpretContext) Object
  + AstConstant(Object, Position) 
}
class AstConstantList {
  + execute(InterpretContext) Object
  + AstConstantList(AstExpressionList, Position) 
}
class AstConstantMap {
  + execute(InterpretContext) Object
  + AstConstantMap(List~AstConstantMapEntry~, Position) 
}
class AstConstantMapEntry {
  + execute(InterpretContext) NameValuePair~String, Object~
  + AstConstantMapEntry(String, AstExpression, Position) 
}
class AstDirective {
  # Position position
   Position position
  + AstDirective(Position) 
}
class AstDirectiveBreak {
  + execute(InterpretContext) void
  + AstDirectiveBreak(AstExpression, Position) 
}
class AstDirectiveCall {
  + execute(InterpretContext) void
  + AstDirectiveCall(String, AstExpressionList, Position) 
}
class AstDirectiveContinue {
  + execute(InterpretContext) void
  + AstDirectiveContinue(AstExpression, Position) 
}
class AstDirectiveFor {
  + execute(InterpretContext) void
  + AstDirectiveFor(String, AstExpression, AstStatementList, AstStatementList, Position) 
}
class AstDirectiveIf {
  + execute(InterpretContext) void
  + AstDirectiveIf(AstExpression, AstStatementList, AstStatement, Position) 
}
class AstDirectiveInclude {
  + execute(InterpretContext) void
  + AstDirectiveInclude(AstExpression, AstExpression, String, Position) 
}
class AstDirectiveMacro {
  - String name
  - AstStatementList statements
  - Map~String, Class~?~~ symbols
  - List~String~ argumentNames
   String name
   List~String~ argumentNames
   AstStatementList statements
   Map~String, Class~?~~ symbols
   Position position
  + execute(InterpretContext) void
  + AstDirectiveMacro(String, List~String~, Map~String, Class~?~~, AstStatementList, Position) 
}
class AstDirectiveNoop {
  + execute(InterpretContext) void
  - AstDirectiveNoop() 
}
class AstDirectiveReturn {
  + execute(InterpretContext) void
  + AstDirectiveReturn(AstExpression, Position) 
}
class AstDirectiveSet {
  + execute(InterpretContext) void
  + AstDirectiveSet(String, AstExpression, Position) 
}
class AstDirectiveStop {
  + execute(InterpretContext) void
  + AstDirectiveStop(AstExpression, Position) 
}
class AstDirectiveTag {
  + execute(InterpretContext) void
  - doInvoke(InterpretContext, TagInvoker, Object[]) void
  + AstDirectiveTag(String, AstExpressionList, AstStatementList, Position) 
}
class AstErrorListener {
  + syntaxError(Recognizer~?, ?~, Object, int, int, String, RecognitionException) void
  + AstErrorListener() 
}
class AstErrorStrategy {
  + recover(Parser, RecognitionException) void
  + recoverInline(Parser) Token
  + AstErrorStrategy() 
}
class AstExpression {
  # Position position
   Position position
  + execute(InterpretContext) Object
  + getResultType(ValueStack, Object) Class~?~
  + AstExpression(Position) 
}
class AstExpressionList {
  + execute(InterpretContext) Object[]
  + AstExpressionList(List~AstExpression~, Position) 
}
class AstIdentifier {
  - String name
   String name
  + execute(InterpretContext) Object
  + getResultType(ValueStack, Object) Class~?~?
  + AstIdentifier(String, Position) 
}
class AstInvokeField {
  - doInvokeGetter(InterpretContext, Getter, Object) Object
  + execute(InterpretContext) Object?
  + AstInvokeField(AstExpression, String, boolean, Position) 
}
class AstInvokeFieldStatic {
  + execute(InterpretContext) Object
  + AstInvokeFieldStatic(Class~?~, String, Position) 
}
class AstInvokeFunction {
  + execute(InterpretContext) Object
  - doInvoke(InterpretContext, FunctionInvoker, Object[]) Object
  + AstInvokeFunction(String, AstExpressionList, Position) 
}
class AstInvokeIndexGet {
  + execute(InterpretContext) Object?
  + AstInvokeIndexGet(AstExpression, AstExpression, boolean, Position) 
}
class AstInvokeMethod {
  + execute(InterpretContext) Object?
  - doInvoke(InterpretContext, MethodInvoker, Object, Object[]) Object?
  + AstInvokeMethod(AstExpression, String, AstExpressionList, boolean, Position) 
}
class AstInvokeMethodStatic {
  + execute(InterpretContext) Object
  - doInvoke(InterpretContext, MethodInvoker, Object[]) Object?
  + AstInvokeMethodStatic(Class~?~, String, AstExpressionList, Position) 
}
class AstInvokeNewArray {
  + execute(InterpretContext) Object
  - validate(InterpretContext, int, Object) void
  + AstInvokeNewArray(Class~?~, List~AstExpression~, Position) 
}
class AstInvokeNewObject {
  + execute(InterpretContext) Object
  + AstInvokeNewObject(Class~?~, AstExpressionList, Position) 
}
class AstNode {
  + AstNode() 
}
class AstOperatorBinary {
  + execute(InterpretContext) Object
  + AstOperatorBinary(int, AstExpression, AstExpression, Position) 
}
class AstOperatorEquals {
  + execute(InterpretContext) Object
  + AstOperatorEquals(int, AstExpression, AstExpression, Position) 
}
class AstOperatorInstanceof {
  + execute(InterpretContext) Object
  + AstOperatorInstanceof(AstExpression, Class~?~, Position) 
}
class AstOperatorNullAsDefault {
  + execute(InterpretContext) Object
  + AstOperatorNullAsDefault(AstExpression, AstExpression, Position) 
}
class AstOperatorUnary {
  + execute(InterpretContext) Object
  + AstOperatorUnary(int, AstExpression, Position) 
}
class AstStatement {
  + execute(InterpretContext) void
  + AstStatement() 
}
class AstStatementList {
  - removeNoopDirective(ListIterator~AstStatement~) void
  - splitStatementList(ListIterator~AstStatement~) void
  - trimDirectiveWhitespacesAndComments(ListIterator~AstStatement~, int, ParserContext) void
  + execute(InterpretContext) void
  - combinedContinuousTexts(ListIterator~AstStatement~) void
  - isAstDirective(AstNode, boolean) boolean
  + AstStatementList(List~AstStatement~, int, ParserContext) 
}
class AstTemplate {
  + execute(InterpretContext) void
  + AstTemplate(AstStatementList) 
}
class AstTernaryOperator {
  + execute(InterpretContext) Object
  + AstTernaryOperator(AstExpression, AstExpression, AstExpression, Position) 
}
class AstTernarySimplifyOperator {
  + execute(InterpretContext) Object
  + AstTernarySimplifyOperator(AstExpression, AstExpression, Position) 
}
class AstText {
  - int line
  - String text
   int line
   String text
   boolean empty
  # trimDirectiveWhitespaces(boolean, boolean, boolean) void
  + toString() String
  + execute(InterpretContext) void
  # trimDirectiveComments(boolean, boolean, String, String) void
  # trimLastNewLine() void
  + AstText(String, int) 
}
class AstType {
  - Position position
  - String className
   Position position
   String className
  + AstType(String, Position) 
}
class AstValue {
  + execute(InterpretContext) void
  + AstValue(AstExpression) 
}
class AstValueEscaped {
  + execute(InterpretContext) void
  + AstValueEscaped(AstExpression) 
}
class BinaryOperatorTest {
  + testNullAsDefault() void
  + testMinus() void
  + testMod() void
  + testDiv() void
  + testInstanceOf() void
  + testPlus() void
  + testArithmetic() void
  + testMul() void
  + testStringAdd() void
  + BinaryOperatorTest() 
}
class BitwiseOperatorTest {
  + testShift() void
  + testBasic() void
  + BitwiseOperatorTest() 
}
class BuildinFunctionTest {
  + testRange() void
  + testDebug() void
  + testMacroGet() void
  + BuildinFunctionTest() 
}
class BuildinMethodTest {
  + testFormatDate() void
  + testWord() void
  + testStringWithException() void
  + testJson() void
  + testFormatNumber() void
  + testString() void
  + testAsDate() void
  + testEscapeString() void
  + BuildinMethodTest() 
}
class BuildinTagTest {
  + test() void
  + test_default_block() void
  + BuildinTagTest() 
}
class ByteArrayEncoder {
  + writeTo(JetWriter) void
  + ByteArrayEncoder(String, Charset) 
}
class ClassBuildinMethodInvoker {
   boolean voidResult
   String signature
  + checkAccess(JetSecurityManager) void
  + invoke(Object, Object[]) Object
  + ClassBuildinMethodInvoker(MethodInfo) 
}
class ClassResolver {
  + resolveClass(String) Class~?~?
  - getPackages(String) List~String~
  + importClass(String) void
  + ClassResolver(boolean) 
  + ClassResolver() 
}
class ClasspathResourceLoader {
  + load(String) Resource?
  + ClasspathResourceLoader() 
}
class CommentTest {
  + testLine1() void
  + testBlock() void
  + testLine2() void
  + CommentTest() 
}
class ConstantTest {
  + testString() void
  + testMap() void
  + testNumber() void
  + testOthers() void
  + testList() void
  + ConstantTest() 
}
class DefaultGetterResolver {
  + resolve(Class~?~, String) Getter?
  + register(GetterResolver) void
  - doGetGetter(Class~?~, String) Getter?
  + DefaultGetterResolver() 
}
class DirectiveCallTest {
  + test() void
  + DirectiveCallTest() 
}
class DirectiveDefineTest {
  + test() void
  + testDefineAfterUse() void
  + testRedefine() void
  + DirectiveDefineTest() 
}
class DirectiveForTest {
  + testForMap() void
  + testForOuter() void
  + testForList() void
  + testForStatus() void
  + testForElse() void
  + testForComplex() void
  + DirectiveForTest() 
}
class DirectiveIfTest {
  + testElseIf() void
  + testElse() void
  + testIf() void
  + DirectiveIfTest() 
}
class DirectiveIncludeTest {
  + testInclude_args() void
  + testReturn() void
  + testInclude() void
  + DirectiveIncludeTest() 
}
class DirectiveInvalidTest {
  + testInvalid_if() void
  + testInvalid_define() void
  + testInvalid_continue() void
  + testInvalid_break() void
  + testInvalid_missing_end() void
  + DirectiveInvalidTest() 
}
class DirectiveMacroTest {
  + testDefination() void
  + testRedefination() void
  + testEmbed() void
  + DirectiveMacroTest() 
}
class DirectiveSetTest {
  + testOk() void
  + test() void
  + testFailed() void
  + DirectiveSetTest() 
}
class DirectiveStopTest {
  + testForStop() void
  + testForContinue() void
  + testForBreak() void
  + DirectiveStopTest() 
}
class DirectiveTagTest {
  + initializeEngine() void
  + test() void
  + testClosure() void
  + testNotFound() void
  + DirectiveTagTest() 
}
class EnvHolder {
  - Environment environment
   Environment environment
  - EnvHolder() 
}
class EqualsOperatorTest {
  + testEquals() void
  + testComparable() void
  + testAndOrNot() void
  + testIdenticallyEquals() void
  + testCompare() void
  + testTrue() void
  + testAndOrQuickPath() void
  + EqualsOperatorTest() 
}
class Errors {
  ~ markSourceLines(StringBuilder, String[], int, int) void
  + format(String, Object[]) String
  + format(String, Source, Position) String
  + typeName(Object) String
  + isReflectIllegalArgumentException(Throwable) boolean
  + Errors() 
}
class ExtensionFunctionInvoker {
   String signature
  + invoke(Object[]) Object
  + checkAccess(JetSecurityManager) void
  + ExtensionFunctionInvoker(MethodInfo) 
}
class ExtensionMethodInvoker {
   boolean voidResult
   String signature
  + invoke(Object, Object[]) Object
  + checkAccess(JetSecurityManager) void
  + ExtensionMethodInvoker(MethodInfo) 
}
class FieldGetter {
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
  + FieldGetter(FieldInfo) 
}
class FileSystemResourceLoader {
  + load(String) Resource?
  + FileSystemResourceLoader() 
}
class FunctionInvoker {
<<Interface>>
   String signature
  + invoke(Object[]) Object
  + checkAccess(JetSecurityManager) void
}
class FunctionInvokerResolver {
  - doGetFunctionInvoker(String, Class~?~[]) FunctionInvoker?
  + register(MethodInfo) void
  + resolve(String, Class~?~[]) FunctionInvoker?
  + register(Class~?~) void
  + FunctionInvokerResolver() 
}
class Functions
class Getter {
<<Interface>>
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
}
class GetterResolver {
<<Interface>>
  + resolve(Class~?~, String) Getter
}
class GlobalResolver {
  + registerFunctions(String) void
  + resolveGetter(Class~?~, String) Getter
  + registerMethods(Class~?~) void
  + registerMethods(String) void
  + importClass(String) void
  + registerMacros(JetTemplate) void
  + resolveFunction(String, Class~?~[]) FunctionInvoker
  + registerGetterResolver(GetterResolver) void
  + resolveMethod(Class~?~, String, Class~?~[], boolean) MethodInvoker
  + registerTag(MethodInfo) void
  + registerFunctions(Class~?~) void
  + registerFunction(MethodInfo) void
  + scan(List~String~, boolean) void
  + registerTags(String) void
  + resolveMacro(String, Class~?~[], boolean) JetTemplateMacro
  + registerMethod(MethodInfo) void
  + resolveClass(String) Class~?~
  + registerTags(Class~?~) void
  + resolveTag(String, Class~?~[]) TagInvoker
  + GlobalResolver() 
}
class IdentifierTest {
  + test() void
  + testInvalid_for_status() void
  + testInvalid_keyword_var() void
  + IdentifierTest() 
}
class InconsistentClassTest {
  + testInclude() void
  + InconsistentClassTest() 
}
class InterpretContext {
   GlobalResolver globalResolver
   ValueStack valueStack
   Source source
   JetTemplate template
   JetWriter writer
   int signal
   TemplateStack templateStack
   JetSecurityManager securityManager
   JetEngine engine
   String returnName
  + current() InterpretContext
  + doMacroCall(JetTemplateMacro, Object[]) void
  + doIncludeCall(String, Map~String, Object~, String) void
  + InterpretContext() 
}
class InterpretContextImpl {
  - GlobalResolver globalResolver
  - JetWriter writer
  - String returnName
  - JetSecurityManager securityManager
  - ValueStack valueStack
  - JetEngine engine
  - int signal
  - TemplateStack templateStack
   GlobalResolver globalResolver
   ValueStack valueStack
   Source source
   JetTemplate template
   JetWriter writer
   int signal
   TemplateStack templateStack
   JetSecurityManager securityManager
   JetEngine engine
   String returnName
  + doMacroCall(JetTemplateMacro, Object[]) void
  + doIncludeCall(String, Map~String, Object~, String) void
  + setThreadLocal() void
  + freeThreadLocal() void
  + InterpretContextImpl(JetEngine, JetWriter, Map~String, Object~, JetSecurityManager) 
}
class InterpretException {
   String message
  + set(Source) InterpretException
  + set(Position) InterpretException
  + cause(Throwable) InterpretException
  + InterpretException(String, Object[]) 
  + InterpretException(Throwable) 
  + InterpretException(String) 
}
class InvokeFieldTest {
  + testNotFound() void
  + test() void
  + testMap() void
  + testStatic() void
  + testClass() void
  + testArrayLength() void
  + testStaticNotFound() void
  + InvokeFieldTest() 
}
class InvokeFunctionTest {
  + test() void
  + initializeEngine() void
  + InvokeFunctionTest() 
}
class InvokeIndexGetTest {
  + testList() void
  + testList_args_error() void
  + testArray() void
  + testArray_args_error() void
  + testMap() void
  + testMap_args_error() void
  + InvokeIndexGetTest() 
}
class InvokeInterfaceTest {
  + test() void
  + InvokeInterfaceTest() 
}
class InvokeMethodExtensionTest {
  + test() void
  + initializeEngine() void
  + testVarargs() void
  + testVarargsIssue() void
  + InvokeMethodExtensionTest() 
}
class InvokeMethodTest {
  + testOverload() void
  + testStaticOverload() void
  + testVarargs() void
  + testStaticVarargs() void
  + test() void
  + testStatic() void
  + InvokeMethodTest() 
}
class InvokeNewArrayTest {
  + test() void
  + InvokeNewArrayTest() 
}
class InvokeNewObjectTest {
  + initializeEngine() void
  + test3() void
  + test1() void
  + testClassNotFound() void
  + test2() void
  + testCtorNotFound() void
  + InvokeNewObjectTest() 
}
class JFinalActiveRecordGetterResolver {
  + resolve(Class~?~, String) Getter?
  + JFinalActiveRecordGetterResolver() 
}
class Jdk6CharArrayEncoder {
  + writeTo(JetWriter) void
  + Jdk6CharArrayEncoder(String) 
}
class Jdk7CharArrayEncoder {
  + writeTo(JetWriter) void
  + Jdk7CharArrayEncoder(String) 
}
class Jdk9CharArrayEncoder {
  + writeTo(JetWriter) void
  + Jdk9CharArrayEncoder(String) 
}
class JetAnnotations {
  + JetAnnotations() 
}
class JetConfig {
  - boolean trimDirectiveComments
  - boolean syntaxSafecall
  - JetSecurityManager templateSecurityManager
  - String trimDirectiveCommentsPrefix
  - List~String~ importTags
  - List~String~ autoscanPackages
  - List~String~ importFunctions
  - boolean syntaxStrict
  - List~String~ importMethods
  - boolean autoscanSkiperrors
  - boolean trimLeadingWhitespaces
  - List~String~ importDefines
  - String templateSuffix
  - Charset inputEncoding
  - boolean trimDirectiveWhitespaces
  - List~String~ importMacros
  - String trimDirectiveCommentsSuffix
  - boolean ioSkiperrors
  - List~String~ importClasses
  - List~ResourceLoader~ templateLoaders
  - Charset outputEncoding
   List~String~ importClasses
   List~String~ importFunctions
   JetSecurityManager templateSecurityManager
   List~String~ autoscanPackages
   List~String~ importDefines
   Charset inputEncoding
   boolean ioSkiperrors
   List~String~ importMacros
   boolean syntaxSafecall
   List~ResourceLoader~ templateLoaders
   String templateSuffix
   String trimDirectiveCommentsPrefix
   boolean autoscanSkiperrors
   List~String~ importTags
   String trimDirectiveCommentsSuffix
   boolean trimDirectiveComments
   boolean syntaxStrict
   boolean trimLeadingWhitespaces
   boolean trimDirectiveWhitespaces
   Charset outputEncoding
   List~String~ importMethods
  - initialize(Config) void
  # JetConfig(Properties, String) 
}
class JetContext {
  + get(String) Object
  + set(String, Object) void
  + JetContext(int) 
  + JetContext() 
}
class JetEngine {
   GlobalResolver globalResolver
   JetGlobalContext globalContext
   JetConfig config
  + getTemplate(String) JetTemplate
  + create() JetEngine
  + create(Properties, String) JetEngine
  + createTemplate(String, String) JetTemplate
  + checkTemplate(String) boolean
  + create(Properties) JetEngine
  + create(String) JetEngine
  + getResource(String) Resource
  + createTemplate(String) JetTemplate
  + JetEngine() 
}
class JetEngineImpl {
  - JetConfig config
  - GlobalResolver globalResolver
  - JetGlobalContext globalContext
   GlobalResolver globalResolver
   JetGlobalContext globalContext
   JetConfig config
  + createTemplate(String, String) JetTemplate
  + checkTemplate(String) boolean
  + getTemplate(String) JetTemplate
  + createTemplate(String) JetTemplate
  - internalGetTemplate(String) JetTemplate?
  + getResource(String) Resource
  - doCreateGlobalContext() JetGlobalContext
  - doCreateGlobalResolver() GlobalResolver
  - doLoadGlobalMacroFiles() void
  + JetEngineImpl(JetConfig) 
}
class JetEngineListener {
  + contextInitialized(ServletContextEvent) void
  + contextDestroyed(ServletContextEvent) void
  + JetEngineListener() 
}
class JetForIterator {
  # int index
  # int size
  # JetForIterator outer
   boolean even
   boolean odd
   int size
   boolean last
   boolean first
   int index
   JetForIterator outer
  + remove() void
  + hasNext() boolean
  + next() Object
  - asList(Iterator~?~) List~?~
  + empty() boolean
  + JetForIterator(Object) 
}
class JetFunctions {
  + includeGet(String) String
  + includeGet(String, Map~String, Object~) String
  + random() int
  + range(int, int) Iterator~Integer~
  + fileGet(String) String
  + range(int, int, int) Iterator~Integer~
  + macroGet(String, Object[]) String
  + uuid() UUID
  + debug(String, Object[]) void
  + now() Date
  + fileGet(String, String) String
  + JetFunctions() 
}
class JetGlobalContext {
  + set(String, Object) void
  + set(Class~?~, String, Object) void
  + getValue(String) Object
  + getType(String) Class~?~
  + define(Class~?~, String) void
  + JetGlobalContext() 
}
class JetMethods {
  + asLong(Object) Long
  + unescapeJava(String) String
  + asList(Collection~T~) List~T~
  + unescapeUrl(String) String
  + escapeJava(String) String
  + unescapeJavaScript(String) String
  + repeat(String, int) String
  + format(Date, String) String
  + format(Date) String
  + asList(Object[]) List~Object~
  + escapeUrl(String) String
  + asFloat(Object) Float
  + format(Number, String) String
  + deleteWhitespace(String) String
  + asBoolean(Object) Boolean
  + repeat(String, String, int) String
  + abbreviate(String, int, int) String
  + toUnderlineName(String) String
  + sha1Hex(String) String
  + unescapeXml(String) String
  + asInt(Object) Integer
  + asDate(String) Date
  + asJson(Object) String
  + asString(Object) String
  + escapeXml(String) String
  + asDate(String, String) Date
  + toCapitalizeCamelCase(String) String
  + format(Number) String
  + sha1Hex(String, String) String
  + capitalize(String) String
  + toCamelCase(String) String
  + escapeUrl(String, String) String
  + md5Hex(String, String) String
  + unescapeUrl(String, String) String
  + asDouble(Object) Double
  + md5Hex(String) String
  + abbreviate(String, int) String
  + escapeJavaScript(String) String
  + JetMethods() 
}
class JetOutputStreamPrinter {
  - Charset charset
   Object originStream
   Charset charset
   boolean streaming
   boolean skipErrors
  + print(int) void
  + close() void
  + print(char[]) void
  + print(byte[]) void
  + print(char[], int, int) void
  + print(byte[], int, int) void
  + print(String) void
  + flush() void
  + JetOutputStreamPrinter(OutputStream, Charset) 
}
class JetOutputStreamPrinterEx {
  - Charset charset
   Object originStream
   Charset charset
   boolean streaming
   boolean skipErrors
  + print(int) void
  + flush() void
  + print(char[]) void
  + print(byte[]) void
  + print(char[], int, int) void
  + print(String) void
  + close() void
  + print(byte[], int, int) void
  + JetOutputStreamPrinterEx(OutputStream, Charset) 
}
class JetSecurityManager {
<<Interface>>
  + checkAccess(Field) void
  + checkAccess(Constructor~?~) void
  + checkAccess(Class~?~) void
  + checkAccess(Method) void
}
class JetSecurityManagerImpl {
  - boolean disallowStaticField
  - boolean disallowConstructor
  - boolean disallowStaticMethod
   String configFile
   List~String~ nameList
   boolean disallowStaticMethod
   boolean disallowConstructor
   boolean disallowStaticField
  - addList(String) void
  + checkAccess(Constructor~?~) void
  + checkAccess(Class~?~) void
  + checkAccess(Method) void
  + checkAccess(Field) void
  - checkAccess(String) void
  + JetSecurityManagerImpl() 
}
class JetTagContext {
   ValueStack valueStack
   JetWriter writer
   InterpretContext interpretContext
   JetEngine engine
   String bodyContent
  + invoke() void
  + JetTagContext(AstStatementList) 
}
class JetTags {
  + layout_block_default(JetTagContext, String) void
  + layout_block(JetTagContext, String) void
  + JetTags() 
}
class JetTemplate {
<<Interface>>
   String name
   Source source
   long lastModified
   boolean reloadable
   JetTemplateOption option
   JetSecurityManager securityManager
   JetEngine engine
   AstTemplate astNode
  + render(Map~String, Object~, OutputStream) void
  + resolveMacro(String, Class~?~[], boolean) JetTemplateMacro
  + render(Map~String, Object~, Writer) void
  + reload() void
}
class JetTemplateAutoConfiguration {
  + envHolder() EnvHolder
  + autoRegiesterBeanPostProcessor() BeanPostProcessor
  + jetTemplateViewResolver(JetTemplateProperties) JetTemplateViewResolver
  + JetTemplateAutoConfiguration() 
}
class JetTemplateFilter {
  + init(FilterConfig) void
  + destroy() void
  + doFilter(ServletRequest, ServletResponse, FilterChain) void
  + JetTemplateFilter() 
}
class JetTemplateImpl {
  - long lastModified
  - JetTemplateOption option
  - JetSecurityManager securityManager
  - Source source
  - boolean reloadable
  - AstTemplate astNode
  - JetEngine engine
   String name
   Source source
   long lastModified
   boolean reloadable
   JetTemplateOption option
   JetSecurityManager securityManager
   JetEngine engine
   AstTemplate astNode
  + resolveMacro(String, Class~?~[], boolean) JetTemplateMacro
  + render(Map~String, Object~, OutputStream) void
  + reload() void
  + render(Map~String, Object~, Writer) void
  - doInterpret(Map~String, Object~, JetWriter) void
  - rebuildAstNodeAndConfig() void
  + toString() String
  + JetTemplateImpl(JetEngine, Resource, boolean, JetSecurityManager) 
}
class JetTemplateMacro {
  - JetTemplate template
  - AstDirectiveMacro astNode
   String name
   List~String~ argumentNames
   JetTemplate template
   AstDirectiveMacro astNode
   Map~String, Class~?~~ symbols
   String signature
  + checkAccess(JetSecurityManager) void
  + invoke(Object[]) Object?
  + JetTemplateMacro(JetTemplate, AstDirectiveMacro) 
}
class JetTemplateOption {
  - boolean safecall
  - boolean trimLeadingWhitespaces
  - Map~String, Class~?~~ symbols
  - boolean strict
   boolean strict
   Map~String, Class~?~~ symbols
   boolean trimLeadingWhitespaces
   boolean safecall
  # JetTemplateOption(ParserContext) 
}
class JetTemplateProperties {
  - String configLocation
  - Properties config
  - String prefix
  - int order
  - String suffix
   String configLocation
   Properties config
   int order
   String suffix
   String prefix
  + JetTemplateProperties() 
}
class JetTemplateRender {
  + render() void
  + JetTemplateRender(String) 
}
class JetTemplateRenderFactory {
  + getRender(String) Render
  + getDefaultRender(String) Render
  + JetTemplateRenderFactory() 
}
class JetTemplateResult {
  # doExecute(String, ActionInvocation) void
  + JetTemplateResult() 
}
class JetTemplateResult {
  - String contentType
   String contentType
  # locateTarget(ActionRequest, String) String?
  # renderView(ActionRequest, String) void
  + JetTemplateResult() 
}
class JetTemplateServlet {
  + doPost(HttpServletRequest, HttpServletResponse) void
  + init() void
  + doGet(HttpServletRequest, HttpServletResponse) void
  + JetTemplateServlet() 
}
class JetTemplateView {
  + checkResource(Locale) boolean
  # renderMergedTemplateModel(Map~String, Object~, HttpServletRequest, HttpServletResponse) void
  + JetTemplateView() 
}
class JetTemplateView {
  + render(HttpServletRequest, HttpServletResponse, Object) void
  + JetTemplateView(String) 
}
class JetTemplateViewHandler {
  - String prefix
  - String suffix
   String prefix
   String type
   String suffix
  # doRender(RequestContext, String) void
  - initialize() void
  + JetTemplateViewHandler() 
}
class JetTemplateViewMaker {
  + make(Ioc, String, String) View?
  + JetTemplateViewMaker() 
}
class JetTemplateViewResolver {
  - Properties configProperties
  - JetEngine jetEngine
  - String configLocation
   Properties configProperties
   String configLocation
   JetEngine jetEngine
  + afterPropertiesSet() void
  # requiredViewClass() Class~?~
  # loadView(String, Locale) View
  + JetTemplateViewResolver() 
}
class JetWebContext {
  + String WEBROOT_PATH
   String WEBROOT_PATH
  + disableSession() void
  + get(Object) Object?
  - createImplicitWebObject(TYPE) Object?
  + JetWebContext(HttpServletRequest, HttpServletResponse, Map~String, Object~) 
  + JetWebContext(HttpServletRequest, HttpServletResponse) 
}
class JetWebEngine {
  - ServletContext servletContext
  - JetEngine engine
   JetEngine engine
   ServletContext servletContext
  + create(ServletContext, Properties, String) JetEngine
  - doCreateWebEngine(ServletContext, Properties, String) JetEngine
  + create(ServletContext) JetEngine
  + JetWebEngine() 
}
class JetWebFunctions {
  + servletGet(String) String
  + JetWebFunctions() 
}
class JetWebTags {
  + application_cache(JetTagContext, String, long) void
  + session_cache(JetTagContext, String, long) void
  + JetWebTags() 
}
class JetWriter {
   Object originStream
   Charset charset
   boolean streaming
   boolean skipErrors
  + create(OutputStream, Charset, boolean, boolean) JetWriter
  + print(char[], int, int) void
  + close() void
  + print(int) void
  + flush() void
  + create(JetWriter, boolean) JetWriter
  + print(String) void
  + print(byte[], int, int) void
  + print(char[]) void
  + print(byte[]) void
  + create(Writer, Charset, boolean, boolean) JetWriter
  + JetWriter() 
}
class JetWriterPrinter {
  - Charset charset
   Object originStream
   Charset charset
   boolean streaming
   boolean skipErrors
  + print(char[]) void
  + print(char[], int, int) void
  + print(byte[], int, int) void
  + print(String) void
  + close() void
  + print(byte[]) void
  + flush() void
  + print(int) void
  + JetWriterPrinter(Writer, Charset) 
}
class JetWriterPrinterEx {
  - Charset charset
   Object originStream
   Charset charset
   boolean streaming
   boolean skipErrors
  + print(char[], int, int) void
  + close() void
  + print(char[]) void
  + print(String) void
  + print(byte[], int, int) void
  + print(byte[]) void
  + print(int) void
  + flush() void
  + JetWriterPrinterEx(Writer, Charset) 
}
class ListIterator~T~ {
  + remove() void
  + reset() void
  + add(T) void
  + has() boolean
  + peek() T
  + move() void
  + has(int) boolean
  + addAll(T[]) void
  + hasNext() boolean
  + move(int) void
  + peek(int) T
  + hasPrevious() boolean
  + ListIterator(List~T~) 
}
class MacroResolver {
  - checkImportedMacrosReload() void
  + clear() void
  + resolve(String, Class~?~[], boolean) JetTemplateMacro?
  + register(JetTemplateMacro) void
  + register(JetTemplate) void
  + MacroResolver() 
}
class MapGetter {
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
  + MapGetter(String) 
}
class MethodInvoker {
<<Interface>>
   boolean voidResult
   String signature
  + checkAccess(JetSecurityManager) void
  + invoke(Object, Object[]) Object
}
class MethodInvokerResolver {
  + register(MethodInfo) void
  + resolve(Class~?~, String, Class~?~[], boolean) MethodInvoker?
  + register(Class~?~) void
  - doGetMethodInvoker(Class~?~, String, Class~?~[], boolean) MethodInvoker?
  + MethodInvokerResolver() 
}
class Methods
class Model {
  - double gravity
  - String name
  - String code
  - String amount
  - int id
  - double range
  - int capacity
  - double price
   String name
   double gravity
   String amount
   int capacity
   String code
   double range
   int id
   double price
  + dummyItems() List~Model~
  + Model(int, String, String, double, double, String, double) 
}
class Model {
  + toString() String
  + Model() 
  + Model(long) 
}
class Model {
  + format(Object[]) String
  + Model() 
}
class Model {
   String name
   boolean good
  + Model() 
}
class ModelGetter {
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
  + ModelGetter(String) 
}
class Name {
  + value() String
}
class OptionImportTest {
  + testMultiPkgs() void
  + testBasic() void
  + OptionImportTest() 
}
class OptionLoadmacroTest {
  + testInclude() void
  + OptionLoadmacroTest() 
}
class OptionSafecallTest {
  + testFail() void
  + testOk() void
  + OptionSafecallTest() 
}
class OptionStrictTest {
  + testFail() void
  + testOk() void
  + OptionStrictTest() 
}
class OptionSyntaxTest {
  + testInvalidValue() void
  + testSyntax() void
  + testInvalidName() void
  + OptionSyntaxTest() 
}
class OptionTrimLeadingWhitespacesTest {
  + test() void
  + OptionTrimLeadingWhitespacesTest() 
}
class OriginalStream {
<<Interface>>
   Object originStream
}
class ParameterUtils {
  + getActualArguments(Object[], int, Class~?~, int) Object[]
  + getParameterTypes(Object[]) Class~?~[]
  + ParameterUtils() 
}
class ParserContext {
  - List~AstDirectiveMacro~ declaredMacros
  - boolean safecall
  - boolean trimLeadingWhitespaces
  - boolean nullSafe
  - String trimDirectiveCommentsPrefix
  - boolean strict
  - boolean trimDirectiveWhitespaces
  - boolean trimDirectiveComments
  - String trimDirectiveCommentsSuffix
  - List~String~ loadMacroFiles
   boolean nullSafe
   boolean strict
   boolean trimDirectiveComments
   Map~String, Class~?~~ symbols
   boolean trimLeadingWhitespaces
   boolean safecall
   List~String~ loadMacroFiles
   boolean trimDirectiveWhitespaces
   List~AstDirectiveMacro~ declaredMacros
   List~String~ macroArgumentNames
   String trimDirectiveCommentsPrefix
   String trimDirectiveCommentsSuffix
  + defineSymbol(String, Class~?~, boolean) void
  + loadMacroFile(String) void
  + importClass(String) void
  + useSymbol(String) void
  + exitMacros() void
  + resolveClass(String) Class~?~
  + enterMacros() void
  + defineSymbol(String, Class~?~) void
  + defineMacro(AstDirectiveMacro) void
  + ParserContext(GlobalResolver, JetGlobalContext) 
}
class PerformanceTest {
  + main(String[]) void
  # eval(JetEngine, Map~String, Object~) void
  + PerformanceTest() 
}
class Position {
  - int column
  - int line
   int line
   int column
  + toString() String
  + Position(int, int) 
}
class PropertyGetter {
  + get(Object) Object
  + checkAccess(JetSecurityManager) void
  + PropertyGetter(PropertyInfo) 
}
class RecordGetter {
  + checkAccess(JetSecurityManager) void
  + get(Object) Object
  + RecordGetter(String) 
}
class ResourceLoader {
<<Interface>>
   boolean reloadable
   String root
   JetSecurityManager securityManager
  + load(String) Resource
}
class SandboxJetEngine {
  - JetSecurityManager securityManager
   GlobalResolver globalResolver
   JetSecurityManager securityManager
   JetGlobalContext globalContext
   JetConfig config
  + createTemplate(String) JetTemplate
  + getTemplate(String) JetTemplate
  + getResource(String) Resource
  + createTemplate(String, String) JetTemplate
  + set(String, String) void
  + checkTemplate(String) boolean
  + SandboxJetEngine(JetEngine) 
}
class SecurityManagerTest {
  + fieldAccess() void
  + methodAccess() void
  + classAccess() void
  + constructorAccess() void
  # initializeEngine() void
  + pkgAccess() void
  + SecurityManagerTest() 
}
class ServletResourceLoader {
  + load(String) Resource?
  + ServletResourceLoader() 
}
class ShiroJetTags {
   Subject subject
  + guest(JetTagContext) void
  + lacks_permission(JetTagContext, String) void
  + not_remembered(JetTagContext) void
  + remembered(JetTagContext) void
  + not_authenticated(JetTagContext) void
  + authenticated(JetTagContext) void
  + principal(JetTagContext) void
  + principal(JetTagContext, String) void
  + has_permission(JetTagContext, String) void
  + user(JetTagContext) void
  - printTagBody(JetTagContext) void
  + has_any_role(JetTagContext, String[]) void
  + lacks_role(JetTagContext, String) void
  + ShiroJetTags() 
}
class SignatureUtils {
  + getFieldSignature(Class~?~, String) String
  + getFunctionSignature(String, Class~?~[]) String
  + getMethodSignature(Class~?~, String, Class~?~[]) String
  + SignatureUtils() 
}
class Source {
  - String[] lines
  - String filename
  - char[] contents
   String[] lines
   String filename
   char[] contents
  + Source(String, char[]) 
}
class SourceResource {
  + openStream() InputStream
  + toCharArray(Charset) char[]
  + lastModified() long
  + SourceResource(String) 
  + SourceResource(String, String) 
}
class SpringedTags {
  + activedProfile(JetTagContext, String) void
  + activedProfile(JetTagContext, String[]) void
  + SpringedTags() 
}
class StrUtils {
  + link(String, String, String[]) String
  + StrUtils() 
}
class Symbols {
  + Symbols() 
}
class SyntaxException {
   String message
  + set(Source) SyntaxException
  + cause(Throwable) SyntaxException
  + set(Position) SyntaxException
  + SyntaxException(String, Object[]) 
  + SyntaxException(Throwable) 
  + SyntaxException(String) 
}
class TYPE {
<<enumeration>>
  + valueOf(String) TYPE
  + values() TYPE[]
  + TYPE() 
}
class TagInvoker {
  + invoke(JetTagContext, Object[]) void
  + TagInvoker(MethodInfo) 
}
class TagInvokerResolver {
  + resolve(String, Class~?~[]) TagInvoker?
  + register(Class~?~) void
  + register(MethodInfo) void
  - doGetTagInvoker(String, Class~?~[]) TagInvoker?
  + TagInvokerResolver() 
}
class Tags {
  + helloWithBody(JetTagContext) void
  + helloWithParam(JetTagContext, String) void
  + hello(JetTagContext) void
  + Tags() 
}
class Tags
class Tags {
  + body(JetTagContext) void
  + Tags() 
}
class TemplateException {
  + TemplateException(String) 
  + TemplateException(Throwable) 
  + TemplateException(String, Throwable) 
  + TemplateException() 
}
class TemplateStack {
  + pop() void
  + push(JetTemplate) void
  + current() JetTemplate
  + TemplateStack() 
}
class TernaryOperatorTest {
  + testBasic() void
  + testSimplify() void
  + TernaryOperatorTest() 
}
class TextEncoder {
<<Interface>>
  + writeTo(JetWriter) void
}
class TextTest {
  + testText() void
  + testTextEscape() void
  + testCDATA() void
  + TextTest() 
}
class Tokens {
  + Tokens() 
}
class TrimDirectiveCommentsCustomTest {
  # initializeConfig() void
  + test() void
  + TrimDirectiveCommentsCustomTest() 
}
class TrimDirectiveCommentsTest {
  + testBasic() void
  + testMultiline() void
  # initializeConfig() void
  + testIssue10() void
  + TrimDirectiveCommentsTest() 
}
class TrimDirectiveWhitespacesTest {
  + testInline2() void
  + testBasic2() void
  + testInline1() void
  + testInline3() void
  + testBasic1() void
  + testInline4() void
  + testTagCall() void
  + testMacroCall() void
  + testIncludeCall() void
  + TrimDirectiveWhitespacesTest() 
}
class TrimLeadingWhitespacesOutputStream {
   Object originStream
  + flush() void
  + write(int) void
  + write(byte[], int, int) void
  + close() void
  + TrimLeadingWhitespacesOutputStream(OutputStream) 
}
class TrimLeadingWhitespacesWriter {
   Object originStream
  + flush() void
  + close() void
  + write(char[], int, int) void
  + write(int) void
  + TrimLeadingWhitespacesWriter(Writer) 
}
class UnaryOperatorTest {
  + testBasic() void
  + UnaryOperatorTest() 
}
class ValueContext {
  + getType(String, boolean) Class~?~?
  + getLocal(String) Object?
  + getPrivate(String) Object?
  + setLocal(String, Object) void
  + ValueContext(ValueContext, Map~String, Class~?~~, Map~String, Object~) 
}
class ValueStack {
  - doGetType(String, ValueContext, boolean) Class~?~?
  + pop() void
  + setLocal(String, Object) void
  + setSuper(String, Object) void
  + getType(String) Class~?~
  + getValue(String) Object?
  + push(Map~String, Class~?~~, Map~String, Object~, boolean) void
  + ValueStack(JetGlobalContext, Map~String, Object~) 
}
class ValueTest {
  + testValue() void
  + testValueEscape() void
  + ValueTest() 
}
class VoidTest {
  + testListGet3() void
  + testMethodInvoke() void
  + testValue() void
  + testListGet1() void
  + testArgumentIsVoid() void
  + testListGet2() void
  + VoidTest() 
}

AstBuilder  -->  AstErrorListener 
AstBuilder  -->  AstErrorStrategy 
AstText  -->  ByteArrayEncoder 
ByteArrayEncoder  ..>  TextEncoder 
JetAnnotations  -->  Functions 
AstText  -->  Jdk6CharArrayEncoder 
Jdk6CharArrayEncoder  ..>  TextEncoder 
AstText  -->  Jdk7CharArrayEncoder 
Jdk7CharArrayEncoder  ..>  TextEncoder 
AstText  -->  Jdk9CharArrayEncoder 
Jdk9CharArrayEncoder  ..>  TextEncoder 
AstStatementList  -->  ListIterator~T~ 
JetAnnotations  -->  Methods 
InvokeFieldTest  -->  Model 
InvokeMethodTest  -->  Model 
InvokeNewObjectTest  -->  Model 
JFinalActiveRecordGetterResolver  -->  ModelGetter 
JetAnnotations  -->  Name 
JFinalActiveRecordGetterResolver  -->  RecordGetter 
InvokeMethodExtensionTest  -->  StrUtils 
JetWebContext  -->  TYPE 
DirectiveTagTest  -->  Tags 
JetAnnotations  -->  Tags 
TrimDirectiveWhitespacesTest  -->  Tags 
AstText  -->  TextEncoder 
```