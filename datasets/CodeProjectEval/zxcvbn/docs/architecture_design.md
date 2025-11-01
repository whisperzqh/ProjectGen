# Architecture Design

Below is a text-based representation of the file tree.

``` bash
└── zxcvbn
    ├── adjacency_graphs.py
    ├── feedback.py
    ├── frequency_lists.py
    ├── __init__.py
    ├── __main__.py
    ├── matching.py
    ├── scoring.py
    └── time_estimates.py
```

`__init__.py` :

- `zxcvbn(password, user_inputs=None)`: Analyzes the strength of a given password by estimating the number of guesses required to crack it, incorporating optional user-provided inputs (e.g., usernames, email addresses) as part of the dictionary used for pattern matching. Returns a detailed result object including score, feedback, and estimated attack times.

`__main__.py` :

- `cli()`: Command-line interface function that reads a password either from standard input (if available) or securely via `getpass`, evaluates its strength using the `zxcvbn` function with optional user-provided inputs, and outputs the result as formatted JSON to stdout.

- `JSONEncoder(o)`: A custom JSON encoder subclass that extends `json.JSONEncoder` to handle non-serializable objects by converting them to their string representation.

  - `default(self, o)`: Overrides the default serialization behavior to return `str(o)` for objects that are not natively JSON-serializable.

`feedback.py` :

- `get_feedback(score: int, sequence: list)`: Generates user-friendly feedback based on the password strength score and the matched patterns. Returns a dictionary containing a warning message and a list of actionable suggestions to improve password strength.

- `get_match_feedback(match: dict, is_sole_match: bool)`: Produces specific feedback for the longest or most significant pattern match in the password (e.g., dictionary words, keyboard sequences, repeats). Returns a dictionary with a contextual warning and tailored suggestions.

- `get_dictionary_match_feedback(match: dict, is_sole_match: bool)`: Provides detailed feedback for matches found in dictionary-based patterns (e.g., common passwords, names, English words). Evaluates capitalization, reversing, and leet substitutions to offer nuanced improvement suggestions and warnings based on match context and frequency.

`matching.py` :

- `build_ranked_dict(ordered_list)`: Converts an ordered list (e.g., frequency list) into a dictionary mapping each word to its 1-based rank.

- `add_frequency_lists(frequency_lists_)`: Populates the global `RANKED_DICTIONARIES` with ranked dictionaries derived from the provided frequency lists.

- `omnimatch(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Runs all matchers (dictionary, spatial, repeat, etc.) on the given password and returns a sorted list of all identified patterns.

- `dictionary_match(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Finds substrings of the password that appear in any of the provided ranked dictionaries (e.g., common passwords, English words).

- `reverse_dictionary_match(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Finds dictionary words that appear in the password when reversed (e.g., "dlrow" for "world").

- `relevant_l33t_subtable(password, table)`: Filters the global l33t substitution table to only include mappings whose substituted characters appear in the password.

- `enumerate_l33t_subs(table)`: Generates all valid combinations of l33t character substitutions from a given subtable.

- `translate(string, chr_map)`: Applies a character substitution map to a string, replacing l33t characters with their plain equivalents.

- `l33t_match(password, _ranked_dictionaries=RANKED_DICTIONARIES, _l33t_table=L33T_TABLE)`: Detects dictionary words in the password that use common l33t substitutions (e.g., "p@ssw0rd").

- `repeat_match(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Identifies repeated substrings (e.g., "abcabc") and recursively analyzes the base token for scoring.

- `spatial_match(password, _graphs=GRAPHS, _ranked_dictionaries=RANKED_DICTIONARIES)`: Detects sequences of adjacent keys on keyboard layouts (e.g., "qwerty", "1234").

- `spatial_match_helper(password, graph, graph_name)`: Helper function that finds spatial patterns on a specific keyboard graph.

- `sequence_match(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Detects monotonic character sequences with consistent Unicode deltas (e.g., "abcdef", "9753").

- `regex_match(password, _regexen=REGEXEN, _ranked_dictionaries=RANKED_DICTIONARIES)`: Matches password substrings against predefined regular expressions (e.g., recent years like "2023").

- `date_match(password, _ranked_dictionaries=RANKED_DICTIONARIES)`: Identifies likely date patterns in the password, with or without separators, and normalizes them into day/month/year components.

- `map_ints_to_dmy(ints)`: Attempts to interpret a 3-tuple of integers as a valid date (day, month, year), applying heuristics for two- and four-digit years.

- `map_ints_to_dm(ints)`: Tries to interpret a 2-tuple as a valid day-month or month-day pair.

- `two_to_four_digit_year(year)`: Converts a two-digit year into a four-digit year using a sliding window around the reference year (e.g., 15 → 2015, 87 → 1987).

`scoring.py` :

- `calc_average_degree(graph)`: Computes the average number of neighbors per key in a keyboard adjacency graph.

- `nCk(n, k)`: Efficiently computes the binomial coefficient "n choose k" using an iterative method.

- `most_guessable_match_sequence(password, matches, _exclude_additive=False)`: Uses dynamic programming to find the optimal non-overlapping sequence of matches that minimizes the estimated number of guesses required to crack the password.

- `estimate_guesses(match, password)`: Dispatches to the appropriate guess estimation function based on the match pattern type and enforces minimum guess thresholds for submatches.

- `bruteforce_guesses(match)`: Estimates the number of guesses for a bruteforce segment based on its length and a fixed character set cardinality.

- `dictionary_guesses(match)`: Computes guesses for dictionary-based matches by combining base rank with variations from capitalization, l33t substitutions, and reversal.

- `repeat_guesses(match)`: Estimates guesses for repeated patterns by multiplying the base token’s guess count by the number of repetitions.

- `sequence_guesses(match)`: Calculates guesses for monotonic character sequences (e.g., "abcd", "9876") based on starting character, direction, and length.

- `regex_guesses(match)`: Estimates guesses for regex-matched patterns such as recent years or character classes, using predefined cardinalities or year proximity heuristics.

- `date_guesses(match)`: Computes guesses for detected dates by considering year proximity to a reference year, day/month combinations, and optional separators.

- `spatial_guesses(match)`: Estimates the number of guesses for spatial keyboard patterns (e.g., "qwerty") using graph-based combinatorics that account for turns, length, and shifted keys.

- `uppercase_variations(match)`: Counts plausible uppercase transformations of a word (e.g., "Password", "PASSWORD") to estimate attacker trials.

- `l33t_variations(match)`: Calculates the number of possible l33t substitution combinations that could produce the matched token from a base dictionary word.

`feedback.py` :

- `estimate_attack_times(guesses)`: Estimates real-world password cracking times across four common attack scenarios (online throttled, online unthrottled, offline slow hashing, offline fast hashing) and returns both raw seconds and human-readable display strings, along with a strength score.

- `guesses_to_score(guesses)`: Maps the estimated number of guesses to an integer strength score from 0 to 4, where 0 is "too guessable" and 4 is "very unguessable", based on predefined thresholds.

- `display_time(seconds)`: Converts a duration in seconds into a human-readable string (e.g., "5 minutes", "2 years"), using rounded units and proper pluralization.

- `float_to_decimal(f)`: Accurately converts a Python float to a high-precision `Decimal` without floating-point representation error, by using the float’s exact integer ratio and adaptive precision.
