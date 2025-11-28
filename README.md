# Towards Realistic Project-Level Code Generation via Multi-Agent Collaboration and Semantic Architecture Modeling

ProjectGen is a multi-agent framework that decomposes projects into architecture design, skeleton generation, and code filling stages with iterative refinement and memory-based context management.

## ProjectGen

#### Code Structure Overview

The core implementation resides in the `src/` directory, which contains three major components: the multi-agent system, the memory management module, and a set of workflow and utility scripts. The directory structure is shown below:

```
src/
├── agents/
│   ├── architecture_agent.py
│   ├── arch_judge_agent.py
│   ├── skeleton_agent.py
│   ├── skeleton_judge_agent.py
│   ├── code_agent.py
│   ├── code_judge_agent.py
│   └── test.py
│
├── memory_manager/
│   ├── arch_memory.py
│   ├── skeleton_memory.py
│   ├── code_memory.py
│   └── __init__.py
│
├── build_dependency_graph.py
├── extract_api.py
├── logger.py
├── main.py
├── prompts.py
├── utils.py
└── workflow.py
```

- **agents/:**
  This directory contains the core agents used in the three-stage generation workflow. Each stage consists of a generation agent and a judging agent, forming a generate–evaluate–refine loop.

- **memory_manager/:**
  The memory modules preserve intra-stage semantic information, enabling agents to efficiently access relevant context from previous iterations.

- **build_dependency_graph.py:**
  Constructs file-level dependency graphs to support ordering.

- **extract_api.py:**
  Extracts function signatures from generated code to support iteration.

- **logger.py:**
  A unified logging module for debugging, tracing agent outputs, and monitoring workflow execution.

- **main.py:**
  The main entry point of the system.

- **prompts.py:**
  Contains prompt templates used by all agents.

- **utils.py:**
  Provides general-purpose utility functions.

- **workflow.py:**
  Defines the overall multi-agent generation workflow.

#### Installation

```
conda create -n projectgen python=3.9
conda activate projectgen
pip install -r requirements.txt
```

#### Usage

Open `src/utils.py` and fill in your OpenAI API key:

```
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
```


Navigate to the `src` directory and run the main script:

```
cd src
python main.py --dataset=CodeProjectEval
```

The outputs will be stored in the `CodeProjectEval_outputs/` folder.


## CodeProjectEval

To better reflect real-world project scenarios and support evaluation through executable test cases, we construct a new project-level code generation dataset, CodeProjectEval, which consists of 18 Python repositories covering a wide range of topics.

#### Detailed Information

| Repository                    | #FILE    | #LOC        | Complexity | #Check Tests (cov.) | #Unit Tests (cov.) | #PRD tokens |
| ----------------------------- | -------- | ----------- | ---------- | ------------------- | ------------------ | ----------- |
| bplustree                     | 8        | 1,509       | 2.29       | 8 (82%)             | 356 (98%)          | 1,339       |
| cookiecutter                  | 18       | 2,805       | 3.42       | 7 (55%)             | 375 (99%)          | 2,100       |
| csvs-to-sqlite                | 3        | 816         | 5.83       | 10 (81%)            | 25 (88%)           | 1,841       |
| deprecated                    | 3        | 597         | 4.08       | 26 (80%)            | 176 (95%)          | 953         |
| djangorestframework-simplejwt | 31       | 2,014       | 2.09       | 8 (63%)             | 191 (93%)          | 1,614       |
| flask                         | 24       | 9,314       | 2.71       | 25 (52%)            | 482 (91%)          | 2,913       |
| imapclient                    | 17       | 3,531       | 2.81       | 9 (40%)             | 267 (80%)          | 3,810       |
| parsel                        | 5        | 1,128       | 2.60       | 5 (65%)             | 250 (95%)          | 1,522       |
| portalocker                   | 9        | 1,958       | 2.84       | 10 (58%)            | 71 (94%)           | 1,990       |
| pyjwt                         | 12       | 2,690       | 3.01       | 10 (53%)            | 294 (94%)          | 382         |
| python-hl7                    | 11       | 2,434       | 2.98       | 10 (56%)            | 100 (87%)          | 2,292       |
| rsa                           | 14       | 2,949       | 2.40       | 6 (73%)             | 100 (87%)          | 3,318       |
| simpy                         | 12       | 2,184       | 2.01       | 7 (60%)             | 149 (90%)          | 2,147       |
| tinydb                        | 10       | 2,170       | 1.76       | 10 (58%)            | 204 (95%)          | 947         |
| trailscraper                  | 13       | 890         | 2.01       | 4 (65%)             | 93 (92%)           | 3,415       |
| voluptuous                    | 7        | 3,100       | 2.55       | 11 (55%)            | 161 (90%)          | 1,221       |
| xmnlp                         | 24       | 1,504       | 3.47       | 8 (65%)             | 23 (81%)           | 3,105       |
| zxcvbn                        | 8        | 1,402       | 5.69       | 6 (81%)             | 31 (84%)           | 2,399       |
| **Avg.**                      | **12.7** | **2,388.6** | **3.03**   | **10 (63.4%)**      | **186 (90.7%)**    | **2,067**   |
| **Mid.**                      | **11.5** | **2,092**   | **2.76**   | **8.5 (61.5%)**     | **168.5 (91.5%)**  | **2,100**   |


**Each repository is supplemented with:**

- **docs/PRD.md:** provides detailed descriptions of a software system’s functional and non-functional requirements, guiding subsequent design and development.
- **docs/UML_pyreverse.md:** UML class diagram and package diagram generated by Pyreverse.
- **docs/architecture_design.md:** the directory tree of the repository and descriptions for each
  source file, accompanied by summaries of the classes and functions they contain.
- **check_tests/:** to provide initial verification during the code generation process.
- **unit_tests/:** executed upon completion of code generation to evaluate the overall quality and functional correctness of the generated projects.


#### Test Scripts

- **Similarity-based Evaluation (SketchBLEU)**

  We adopt SketchBLEU, a similarity-based metric originally introduced in the [CodeS framework](https://github.com/NL2Code/CodeS).
  This metric evaluates the structural similarity between the generated code and the reference implementation. To calculate SketchBLEU:

  ```
  cd datasets/evaluation
  python calc_sketchbleu.py
  ```

- **Unit Test–based Evaluation**

  For functional correctness evaluation, each repository contains a set of unit tests.
  To run the unit tests:

  ```
  cd datasets/evaluation
  python calc_passrate.py
  ```
