from langchain.prompts import PromptTemplate


ssat_prompt = PromptTemplate(
    input_variables=["prd","uml_class", "uml_sequence", "arch_design"],
    template="""You are an expert software architect assistant.

You are given **four types of inputs** describing a software system:

1. **PRD.md (Product Requirement Document)**
    - Contains natural language descriptions of functional and non-functional requirements.
    - May describe system components, data flow, user interactions, responsibilities.
2. **UML Class Diagram**
    - Describes classes and their relationships (inheritance, composition, usage).
    - Also indicates methods/functions defined in each class.
    - May include method signatures, including **parameter names and types**.
3. **UML Sequence Diagram**
    - Illustrates runtime interactions between objects/functions across different modules.
    - Specifies call orders, involved functions, and communicating components.
    - May also reveal **actual parameters used** during function calls.
4. **Architecture Design Document**
    - Lists the overall system structure (e.g., files, directories, and responsibilities).
    - May define which file belongs to which module, and what components a module encapsulates.

------

### **Your task:**

Based on the above inputs, you must extract and construct a **Semantic Software Architecture Tree (SSAT)** — a structured representation of the system's architecture, containing modules, files, classes, and functions, along with their descriptions and relations.

Note: Global_functions in UML is a fake class used only to host global functions. Do not include it as a class in the SSAT; instead, move its functions to the file-level "functions" list.

------

### **Target Output Format: Semantic Software Architecture Tree (SSAT)**

SSAT is a hierarchical, nested JSON tree with the following structure:

```
Module
 └── File
      ├── GlobalCode
      ├── Class
      │    └── Function
      └── Function
```

Each of these elements must contain the following fields:

- **`name`**: the identifier of the element, such as the module name, file name, class name, or function name (without path).

- **`description`**: brief natural language summary of its responsibility.

- **`path`** (only for File-level elements): the full relative path of the file from the project root directory (e.g., `"src/utils/io.py"`). This field reflects the actual file system structure, not the logical module hierarchy.

- **`parameters`** (only for Function-level elements): a list of parameter specifications, if available. Each parameter should be represented as a JSON object like:
  
  ```json
  {{ "name": "param_name", "type": "param_type (if available)", "description": "brief description (if available). If a default value is required according to the documentation, explicitly mention it here." }}
  ```
- **`global_code`** (only for File-level elements): a list of top-level code snippets or statements not inside any class or function.
        
  This includes:
  - Definitions of global variables or constants (including enumerations defined at the file scope).
  - Executable initialization or setup logic that runs when the file is loaded.
  - Script entry point code outside any function.


------

### **Extraction Instructions:**

Please extract the necessary SSAT components from each input as follows:

- **From PRD.md**:
  - Extract descriptions of high-level modules and their responsibilities
  - Identify any function- or class-level behavioral descriptions
- **From UML Class Diagram**:
  - Extract all classes and their methods
  - Capture class-to-class relationships (extends, uses, composition)
  - Add function declarations found in the class
  - When available, extract function parameters including names and types
- **From UML Sequence Diagram**:
  - Capture function call chains and interactions
  - Identify cross-module function relations (calls, communicates_with)
  - If parameter values are passed in interactions, infer parameter roles or examples
- **From Architecture Design Document**:
  - Extract mapping from files to modules
  - Capture file responsibilities and logical structure of the codebase
- If the UML Class Diagram or UML Sequence Diagram contains elements named Global_functions (or similar), treat them as a placeholder for global functions. Do not represent them as a class in the SSAT. Instead, place the contained functions under the file’s "functions" field (for global functions) or "global_code" field if they represent top-level executable code.
  
When extracting function parameters, if the documentation specifies that certain parameters must have default values, **always include this information explicitly in the `description` field** of the parameter.

------

### Output Example

```
[
  {{
    "name": "UserModule",
    "description": "Handles user-related operations",
    "files": [
      {{
        "name": "user_controller.py",
        "path": "src/controllers/user_controller.py",
        "description": "API handlers for user endpoints",
        "global_code": [
          {{
            "name": "USER_ROLES",
            "description": "List of valid user roles",
          }},
          {{
            "name": "init_logging",
            "description": "Sets up logging configuration at module load",
          }}
        ],
        "classes": [
          {{
            "name": "UserController",
            "description": "Coordinates user logic",
            "functions": [
              {{
                "name": "create_user",
                "description": "Creates a new user",
                "parameters": [
                  {{ "name": "user_data", "type": "dict", "description": "User input" }}
                ]
              }}
            ]
          }}
        ],
        "functions": [
          {{
            "name": "validate_username",
            "description": "Checks if the provided username is valid",
            "parameters": [
              {{ "name": "username", "type": "str", "description": "The username to validate" }}
            ]
          }}
        ]
      }}
    ]
  }}
]
```

------

### **Inputs:**

#### **PRD.md**:
{prd}

#### **UML Class Diagram**:
{uml_class} 

#### **UML Sequence Diagram**:
{uml_sequence}

#### **Architecture Design Document**:
{arch_design}

------

Please output only the **JSON representation of the complete SSAT** based on the information extracted from the given files.

You should NOT put all files into a single module unless the input architecture explicitly states so.

If any information is missing, make reasonable assumptions but clearly mark them in the descriptions using `"[assumed]"`.

"""
)

check_arch_prompt = PromptTemplate(
    input_variables=["requirement","uml_class", "uml_sequence", "arch_design", "architecture"],
    template="""You are an expert software architecture reviewer.  

You will be given five inputs:  

1. **Requirements Document (PRD)** - describing the intended functionality of the system.  
2. **UML Class Diagram** - Describes classes and their relationships (inheritance, composition, usage).
3. **UML Sequence Diagram** - Illustrates runtime interactions between objects/functions across different modules.
4. **Architecture Design Document** - Lists the overall system structure (e.g., files, directories, and responsibilities).
5. **Proposed Architecture (ARCH)** - a generated architecture design that includes modules, components, and their dependencies.  

**Important Rule**:
If the PRD, UML diagrams, or Architecture Design Document explicitly provide a file directory structure, file names, or function names, you must prioritize consistency with this given information over general design principles. Do not suggest changes that contradict explicitly provided structures or names merely for abstract notions of modularity or cohesion. Your evaluation should respect and align with the provided information as the highest authority.
Do not suggest or generate any test files as part of the evaluation or revision.

Your task is to evaluate the quality of the proposed architecture (ARCH) based on the following four criteria:  

1. **Requirement Coverage** - Does the architecture cover all the functional modules mentioned in the requirements?  
2. **Consistency with Provided Information** - Does the architecture faithfully follow the directory structure, file names, and function names explicitly given in the PRD, UML diagrams, and Architecture Design Document?
3. **Interface Consistency** - Are the interface names clear, unambiguous, and free from redundancy?  
4. **Dependency Relations** - Are there any circular dependencies? Does the dependency structure follow common layered architecture principles?  

For each criterion, provide a short justification of your evaluation.  
Then, give an **overall score** for the architecture between **1 (poor) and 10 (excellent)**, based on how well it satisfies the above aspects.  

Format your output as follows:  
```

Requirement Coverage: 
Consistency with Provided Information: 
Interface Consistency: 
Dependency Relations: 

Final Score: <a single number between 1 and 10>

```

------

### **Inputs:**

#### **PRD.md**:
{requirement}

#### **UML Class Diagram**:
{uml_class} 

#### **UML Sequence Diagram**:
{uml_sequence}

#### **Architecture Design Document**:
{arch_design}

#### **ARCH**:
{architecture}  

"""
)

iter_arch_prompt = PromptTemplate(
    input_variables=["prd","uml_class", "uml_sequence", "arch_design", "latest_arch", "feedback","history_str"],
    template="""You are an **expert software architect assistant**. Your goal is to refine and improve a previously generated architecture design based on evaluation results.

You will be given the following inputs:

1. **PRD (Product Requirement Document)** - Natural language descriptions of the target system's requirements.
2. **UML Class Diagram** - Structural class-level design of the system.
3. **UML Sequence Diagram** - Dynamic interaction design showing how modules and classes collaborate.
4. **Architecture Design** - The current architecture you generated earlier, describing modules, files, and their responsibilities.
5. **Architecture Evaluation Results** - A review of the architecture from four aspects: requirement coverage, module partitioning rationality, interface consistency, and dependency relations.


### **Your Task**

- Carefully read the **Architecture Evaluation Results**.
- Modify and refine the **Architecture Design** to address the identified issues.
- Ensure that the revised architecture still strictly follows the **PRD, UML Class Diagram, and UML Sequence Diagram**.
- Pay special attention to the four evaluation aspects:
  - **Requirement Coverage**: Does the architecture cover all requirements?
  - **Module Partitioning Rationality**: Is the module division logical, avoiding redundancy, and following high cohesion & low coupling principles?
  - **Interface Consistency**: Are the interfaces named clearly, unambiguously, and consistently?
  - **Dependency Relations**: Are dependencies free of circular references, and consistent with layered architecture principles?
- Produce a revised **Architecture Design** that explicitly incorporates improvements for these dimensions.

Note: Global_functions in UML is a fake class used only to host global functions. Do not include it as a class in the SSAT; instead, move its functions to the file-level "functions" list.

------

### **Target Output Format: Semantic Software Architecture Tree (SSAT)**

SSAT is a hierarchical, nested JSON tree with the following structure:

```
Module
 └── File
      ├── GlobalCode
      ├── Class
      │    └── Function
      └── Function
```

Each of these elements must contain the following fields:

- **`name`**: the identifier of the element, such as the module name, file name, class name, or function name (without path).

- **`description`**: brief natural language summary of its responsibility.

- **`path`** (only for File-level elements): the full relative path of the file from the project root directory (e.g., `"src/utils/io.py"`). This field reflects the actual file system structure, not the logical module hierarchy.

- **`namespace`**: a globally unique identifier for this element, constructed using its full logical hierarchy in the format `Module/File/Class/Function` (omit levels if not applicable). This ensures all `target` references in `relations` are unambiguous and resolvable.

- **`parameters`** (only for Function-level elements): a list of parameter specifications, if available. Each parameter should be represented as a JSON object like:
  
  ```json
  {{ "name": "param_name", "type": "param_type (if available)", "description": "brief description (if available). If a default value is required according to the documentation, explicitly mention it here." }}
  ```
- **`global_code`** (only for File-level elements): a list of top-level code snippets or statements not inside any class or function.
        
  This includes:
  - Definitions of global variables or constants (including enumerations defined at the file scope).
  - Executable initialization or setup logic that runs when the file is loaded.
  - Script entry point code outside any function.

------


### **Inputs:**

#### **Previous Architecture**:

```json
{latest_arch}
```

#### **Feedback from Judge**:
{feedback}

#### **PRD.md**:
{prd}

#### **UML Class Diagram**:
{uml_class} 

#### **UML Sequence Diagram**:
{uml_sequence}

#### **Architecture Design Document**:
{arch_design}

------

Here are some relevant pieces of historical information from previous steps that you may refer to.

{history_str}

------

Please output only the **JSON representation of the complete SSAT** based on the information above.

You should NOT put all files into a single module unless the input architecture explicitly states so.

If any information is missing, make reasonable assumptions but clearly mark them in the descriptions using `"[assumed]"`.


"""
)

skeleton_prompt = PromptTemplate(
    input_variables=["file_item","context"],
    template="""You are an expert software project code generator.
    
Your task is to generate the **skeleton code** for a single file based on its SSAT (Semantic Software Architecture Tree) description, while ensuring consistency with already generated files.

------

### ** Semantic Software Architecture Tree (SSAT)**

SSAT is a hierarchical, nested JSON tree with the following structure:

```
Module
 └── File
      ├── GlobalCode
      ├── Class
      │    └── Function
      └── Function
```

Each of these elements must contain the following fields:

- **`name`**: the identifier of the element, such as the module name, file name, class name, or function name (without path).

- **`description`**: brief natural language summary of its responsibility.

- **`path`** (only for File-level elements): the full relative path of the file from the project root directory (e.g., `"src/utils/io.py"`). This field reflects the actual file system structure, not the logical module hierarchy.

- **`namespace`**: a globally unique identifier for this element, constructed using its full logical hierarchy in the format `Module/File/Class/Function` (omit levels if not applicable). This ensures all `target` references in `relations` are unambiguous and resolvable.

- **`parameters`** (only for Function-level elements): a list of parameter specifications, if available. Each parameter should be represented as a JSON object like:
  
  ```json
  {{ "name": "param_name", "type": "param_type (if available)", "description": "brief description (if available). If a default value is required according to the documentation, explicitly mention it here." }}
  ```
- **`global_code`** (only for File-level elements): a list of top-level code snippets or statements not inside any class or function.
        
  This includes:
  - Definitions of global variables or constants (including enumerations defined at the file scope).
  - Executable initialization or setup logic that runs when the file is loaded.
  - Script entry point code outside any function.

------

### Input Information

You will receive the following inputs:

1. **Previously Generated Skeleton Files**
   - Skeleton code that has already been generated for other files in the project.
   - Provided for context so that imports and definitions remain consistent.
2. **Target File SSAT Description**
   - `file`: the SSAT entry describing this file (functions, classes, etc.)
   - `module`:
    - `name`: the module that this file belongs to
    - `description`: the purpose or role of this module in the project

### Output Information

- Generate **only the skeleton code** for the target file.
- Do **not** repeat the SSAT description in the output.
- The skeleton code must include:
  - import statements
  - global variables, constants, or classes if present
  - function signatures (bodies replaced with `pass`)
- **Function signature rules**:
  - Follow the parameters listed in the SSAT.
  - If a parameter has `"default": "None"`, write it as `=None` in the function signature.
  - If a parameter has another default value, use that exact default.
- If `"default"` is missing, leave the parameter without a default.
- Adds the function description as a comment immediately under each function signature.
- The file must be **syntactically valid Python code** and compilable.
- **Do not add any explanations or comments outside the code.**

------

### Inputs:

#### 1. Previously Generated Skeleton Files

```json
{context}
```

#### 2. Target File SSAT Description

```json
{file_item}
```

------

Please output **only the skeleton code** for the target file.
    
"""
)

check_skeleton_prompt = PromptTemplate(
    input_variables=["skeleton", "architecture"],
    template="""You are an expert software architecture reviewer.
 You will be given two inputs:

1. **Architecture Specification (ARCH)** - the designed architecture, including the intended directory/file structure, module definitions, and interface specifications (classes, functions, parameters).
2. **Generated Skeleton (SKEL)** - the Python code skeleton produced from the architecture, including directory/file organization, imports, class definitions, and function signatures (with `pass` as placeholders).

Your task is to evaluate the quality of the generated skeleton based on the following two criteria:

1. **Directory Structure Matching** - Does the skeleton's directory and file hierarchy match the architecture specification? Are there missing or extra files/directories? Is the nesting consistent with the design?
2. **Interface & Call Relationship Matching** - Do the classes and functions (including names, parameters, and default values) align with the architecture definition? Are all expected interfaces present? Are there inconsistencies or omissions?

For each criterion, provide a short justification of your evaluation.
 Then, give an **overall score** for the skeleton between **1 (poor) and 10 (excellent)**, based on how well it satisfies the above aspects.

Format your output as follows:

```
Directory Structure Matching: 
Interface & Call Relationship Matching: 

Final Score: <a single number between 1 and 10>
```

------

### **Inputs:**

#### **ARCH**:

```json
{architecture}
```

#### **SKEL**:

```json
{skeleton}
```


"""
)

iter_skeleton_prompt = PromptTemplate(
    input_variables=["previous_skeleton", "file_item","context","feedback","history_str"],
    template="""You are an expert software project code generator.
    
Your task is to revise the previously generated skeleton code for a single file. This revision must be based on its SSAT (Semantic Software Architecture Tree) description and reviewer feedback, while ensuring consistency with already generated files. You should only generate the skeleton for this one file in the current round.

------

You will be given structured inputs that include:

1.  the **starting point to be revised**
   - **Previous Skeleton** - the last version of the skeleton code for this file.
   - **Feedback** - reviewer comments on the previous skeleton, pointing out improvements needed (e.g., missing functions, incorrect parameters, inconsistent defaults, directory mismatch).

2. the **authoritative references** for generating the new skeleton.
   - **Current File SSAT** - describing the intended classes, functions, and parameters for this file.
   - **Previously Generated Skeletons in this Turn** - skeleton code for other files that have already been generated, provided as context to ensure cross-file consistency.

Your task is to **revise the previous skeleton** into an improved version that:

- Incorporates the feedback while preserving correct parts.
- Fully respects the SSAT definition (functions, parameters, default values; if a parameter has `default=None`, explicitly set `=None`).
- Adds the function description as a comment immediately under each function signature.
- Maintains consistency with the module's role and with the already generated skeletons in `context_skeletons`.
- Produces valid Python code that compiles.

------

### Inputs:

#### 1. Previous Skeleton

```json
{previous_skeleton}
```

#### 2. Feedback from Reviewer

{feedback}

#### 3. Target File SSAT Description

```json
{file_item}
```

#### 4. Previously Generated Skeletons in this Turn

```json
{context}
```

------

Here are some relevant pieces of historical information from previous steps that you may refer to.

{history_str}

------

Please output **only the skeleton code** for the target file.


"""
)

code_prompt = PromptTemplate(
    input_variables=["file_item", "context"],
    template="""You are an expert software project code generator.

Your task is to generate the **full implementation code** for a single file, based on its provided skeleton and the context of already generated files. 

### Requirements:
1. **Strict adherence to skeleton**  
   - Do not add new functions, classes, or methods that are not present in the skeleton.  
   - Do not remove or rename any existing functions, classes, or methods.  
   - Preserve the order and structure exactly as given.  

2. **Function implementation**  
   - Replace `pass` with the correct implementation according to the function name, parameters, and descriptions provided in the skeleton.  
   - Keep the function-level doc/comment (description) directly under the function signature.  

3. **Consistency with context**  
   - Ensure the generated code is consistent with already generated files (imports, function calls, shared classes, naming conventions, etc.).  
   - Use the context files only for reference, but do not modify them.  

4. **Output format**  
   - Output only the complete code for the current file.  
   - Do not include any explanatory text outside of code.  

------

### Inputs:

#### Skeleton for the current file:

```json
{file_item}
```

#### Previously generated files (context):

```json
{context}
```

------

Now, generate the complete implementation code for this file.

    
"""
)

check_code_prompt = PromptTemplate(
    input_variables=["error_log"],
    template="""You are an expert Python software engineer.

You are given raw error logs produced by running a test suite. 
The logs may contain multiple different error types and stack traces from different test cases.

### Your task:
1. Carefully read through the error logs and group them into distinct error categories. 
   - If multiple errors share the same root cause, group them together.
   - If they are unrelated, list them separately.
2. For each error category:
   - Summarize the error in a clear and concise way.
   - Identify the most likely root cause in the source code.
   - Provide actionable modification suggestions to fix the problem.
3. When providing suggestions:
   - Point out the file/class/function that is most relevant, if it can be inferred.
   - Suggest specific code-level changes instead of vague advice.
   - Include minimal code snippets if they clarify the fix.
4. Do not regenerate the entire codebase; only focus on the reported issues.
5. Always output in a structured format:

  ```json
  [
    {{
      "summary": "...",
      "likely_cause": "...",
      "suggested_fix": "..."
    }},
    ...
  ]
  ```

------

### Inputs

#### Raw Error Logs:

{error_log}

------

Now, generate a structured error analysis and fix suggestions based on the above logs.

""")

get_files_to_update_prompt = PromptTemplate(
    input_variables=["feedback", "context"],
    template="""You are an expert software engineer assisting in project-level debugging and refactoring.

I will provide you with two inputs:

1. **Current project code**, in JSON format.
   - Each file is represented as an object with two fields:
     - `"path"`: the file path (string).
     - `"code"`: the file content (string).
2. **Code modification suggestions**, generated previously based on error logs.

------

### Your task:

- Analyze the suggestions in the context of the current code.
- Identify which files **must be modified** to address the issues. This includes:
  - Files directly mentioned in the suggestions or the error logs.
  - Files that contain relevant functions, classes, or imports that need to be updated.
- Only output the **list of file paths** that should be modified.

### Output format (strictly follow this structure):

```json
[
  "<file_path_1>",
  "<file_path_2>",
  ...
]
```

### Inputs

#### 1. Current Project Code

```json
{context}
```

#### 2. Fix Suggestions

{feedback}

------

Now, generate the list of file paths that need to be modified based on the above inputs.

**Important**: Do **not** output full code changes or reasoning at this stage. Only output the list of file paths.

""")

iter_code_prompt = PromptTemplate(
    input_variables=["file_item","feedback","context", "history_str"],
    template="""You are an expert Python software engineer.

You will be given the following inputs:

1. **Target File (to be modified)**
   - Provided as JSON with two fields:
     - `"path"`: file path relative to the project root
     - `"code"`: original file content
2. **Test Feedback Suggestions**
   - Natural language feedback summarizing the errors and proposed fixes.
   - This should guide the modifications.
3. **Context Files**
   - Other project files (also given in JSON format with `"path"` and `"code"`).
   - These should be considered for consistency, but do not modify them.

------

### **Your task**:

- Modify only the **target file(s)** indicated.
- Implement changes strictly based on the **test feedback suggestions**.
- Ensure consistency with the **context files** (e.g., function signatures, imports, class relationships).
- Do **not** introduce unrelated changes or new functions unless explicitly required by the feedback.
- Maintain Python best practices and correctness.

------

### **Output format**:

Output a JSON array, where the element corresponds to the modified file, with the following structure:

```json
[
  {{
    "path": "src/example.py",
    "code": ".... (new code content here) ...."
  }}
]
```

Only output the modified files. Do not repeat unchanged files.

------

### **Inputs**:

#### 1. Target File to be Modified

```json
{file_item}
```

#### 2. Test Feedback Suggestions

{feedback}

#### 3. Context Files

```json
{context}
```

------

Here are some relevant pieces of historical information from previous steps that you may refer to.

{history_str}

------

Now, generate the modified file according to the above rules. Only output the JSON array of the modified file.

""")