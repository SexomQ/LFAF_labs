# Laboratory Work 1

### Course: Formal Languages & Finite Automata
### Author: Tudor Sclifos

----

## Theory
In this laboratory work we had to implement a finite automaton.The finite automaton is a simple machine that can be in one of a finite number of states and can transition from one state to another based on input.

A finite automaton has a set of states, a set of input symbols, a transition function that maps a state and input symbol to a new state, a start state, and a set of accept states. When given an input string, the finite automaton reads the input symbol by symbol and transitions from state to state according to the rules.


## Objectives:

1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that I will work on during this semester. Basically I need to do the following:

    a. Create a local && remote repository of a VCS hosting service;

    b. Choose a programming language;

    c. Create a separate folder where I will be keeping the report;

3. According to my variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
    
    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

* Firstly we had to generate strings based on the production rules. To get the string, the algorithm replaces the non-terminal variables with terminal ones, choosing randomly from the permited choices.
```
    def generate_string(self):
        list_string = list(self.string)
        final = not any(x in list_string for x in self.VN)

        if final is False:
            for letter in self.string:
                if letter in self.VN:
                    self.string = self.string.replace(letter, self.P[letter][r.randint(0, len(self.P[letter]) - 1)])
                    return self.generate_string()
        else:
            return self.string
```

* The string is saved, therefore, to generate another one, we need to reset it.
```
    def delete_string(self):
        self.string = self.S
        return self
```

* Now I need to transform the grammar to a finite automaton. To obtain it, I adapted the initial variables to ones compatible with the FiniteAutomaton class.
```
    def to_finite_automaton(self):
        Q = set(self.VN + ['END'])
        Sigma = set(self.VT)
        delta = self.P_to_delta()
        q0 = 'S'
        F = {'END'}
        finite_automaton = FiniteAutomaton(Q=Q, Sigma=Sigma, delta=delta, q0=q0, F=F)
        return finite_automaton

    def P_to_delta(self):
        delta = {}

        for state, productions in self.P.items():
            transitions = {}
            for production in productions:
                if len(production) == 1:
                    transitions[production] = 'END'
                else:
                    transitions[production[0]] = production[1:]
            delta[state] = transitions
        delta['END'] = {'END': ''}
        return delta
```

* The FiniteAutomaton has the method that checks if the word is compatible with the grammar. For that it parse the word and checks if it is compatible with delta.
```
    def check_automaton(self, word):
        q = self.q0
        for c in word:
            if c not in self.Sigma:
                return False
            q = self.delta[q].get(c)
            if q is None:
                return False
        return q in self.F
```


## Conclusions / Screenshots / Results

In conclusion, I managed to create a finite automaton that checks the word and return if it is a part of vocabulary or not.

<b>Results:</b>

* The generated 5 strings:
```
VN=['S', 'D', 'F']
VT=['a', 'b', 'c', 'd']
P={ 'S':['aS', 'bS', 'cD'], 'D':['dD', 'bF', 'a'], 'F':['bS', 'a'] }

grammar = Grammar(VN=VN, VT=VT, P=P, S='S')

for i in range(5):
    string = grammar.generate_string()
    print(string)
    grammar.delete_string()

-------------------------------------------------------------------------------------
aaaca
bacbbaacdda
abaabca
aca
acba
```

* The word checking:
```
# convert to finite automaton
fa = grammar.to_finite_automaton()
-------------------------------------------------------------------------------------
False

fa.check_automaton('aaaabbbbcba')
-------------------------------------------------------------------------------------
True
```

## References
https://github.com/DrVasile/FLFA-Labs
https://github.com/DrVasile/FLFA-Labs-Examples
https://www.dfki.de/compling/pdfs/SS06-fsa-presentation.pdf