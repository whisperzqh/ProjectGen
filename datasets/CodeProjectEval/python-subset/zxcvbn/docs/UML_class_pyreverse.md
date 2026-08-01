## UML Class Diagram

```mermaid
classDiagram
  class JSONEncoder {
    default(o)
  }

```
## UML Package Diagram

```mermaid
classDiagram
  class zxcvbn {
  }
  class __main__ {
  }
  class adjacency_graphs {
  }
  class feedback {
  }
  class frequency_lists {
  }
  class matching {
  }
  class scoring {
  }
  class time_estimates {
  }
  feedback --> scoring
  matching --> zxcvbn
  matching --> frequency_lists
  matching --> scoring
  scoring --> adjacency_graphs

```

