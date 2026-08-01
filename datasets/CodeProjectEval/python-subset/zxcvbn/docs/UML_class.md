## UML Class Diagram

```mermaid
classDiagram
    class zxcvbn_module {
        +zxcvbn(password, user_inputs, max_length) dict
    }
    
    class matching_module {
        +omnimatch(password, user_inputs) list
        +dictionary_match(password) list
        +reverse_dictionary_match(password) list
        +l33t_match(password) list
        +spatial_match(password) list
        +repeat_match(password) list
        +sequence_match(password) list
        +regex_match(password) list
        +date_match(password) list
        +build_ranked_dict(ordered_list) dict
        +get_ranked_dictionaries() dict
    }
    
    class scoring_module {
        +most_guessable_match_sequence(password, matches) dict
        +estimate_guesses(match, password) Decimal
        +bruteforce_guesses(match) int
        +dictionary_guesses(match) int
        +repeat_guesses(match) Decimal
        +sequence_guesses(match) int
        +regex_guesses(match) int
        +date_guesses(match) int
        +spatial_guesses(match) int
        +uppercase_variations(match) int
        +l33t_variations(match) int
        +nCk(n, k) int
    }
    
    class feedback_module {
        +get_feedback(score, sequence) dict
        +get_match_feedback(match, is_sole_match) dict
        +get_dictionary_match_feedback(match, is_sole_match) dict
    }
    
    class time_estimates_module {
        +estimate_attack_times(guesses) dict
        +guesses_to_score(guesses) int
        +display_time(seconds) str
        +float_to_decimal(f) Decimal
    }
    
    class adjacency_graphs_module {
        +ADJACENCY_GRAPHS dict
    }
    
    class frequency_lists_module {
        +FREQUENCY_LISTS dict
    }
    
    zxcvbn_module --> matching_module
    zxcvbn_module --> scoring_module
    zxcvbn_module --> feedback_module
    zxcvbn_module --> time_estimates_module
    matching_module --> scoring_module
    matching_module --> adjacency_graphs_module
    matching_module --> frequency_lists_module
    scoring_module --> adjacency_graphs_module
    feedback_module --> scoring_module
```

## UML Package Diagram

```mermaid
graph TD
    __init__["zxcvbn.__init__<br/>(Main Entry Point)"]
    matching["zxcvbn.matching<br/>(Pattern Matching)"]
    scoring["zxcvbn.scoring<br/>(Guess Estimation)"]
    feedback["zxcvbn.feedback<br/>(User Feedback)"]
    time_estimates["zxcvbn.time_estimates<br/>(Attack Time Estimation)"]
    adjacency_graphs["zxcvbn.adjacency_graphs<br/>(Keyboard Layout Data)"]
    frequency_lists["zxcvbn.frequency_lists<br/>(Dictionary Data)"]
    
    __init__ --> matching
    __init__ --> scoring
    __init__ --> feedback
    __init__ --> time_estimates
    matching --> scoring
    matching --> adjacency_graphs
    matching --> frequency_lists
    scoring --> adjacency_graphs
    feedback --> scoring
``` 



