# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Tudor Sclifos

----

## Theory
In formal language theory, a context-free grammar, G, is said to be in Chomsky normal form (first described by Noam Chomsky) if all of its production rules are of the form:

* A → BC,   or
* A → a,   or
* S → ε,

where A, B, and C are nonterminal symbols, the letter a is a terminal symbol (a symbol that represents a constant value), S is the start symbol, and ε denotes the empty string. Also, neither B nor C may be the start symbol, and the third production rule can only appear if ε is in L(G), the language produced by the context-free grammar G:

Every grammar in Chomsky normal form is context-free, and conversely, every context-free grammar can be transformed into an equivalent one which is in Chomsky normal form and has a size no larger than the square of the original grammar's size.

## Objectives:
1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description
### Step 1. Elimination of epsilon:
  #### The algorithm consists of three steps:
   1. Identify all non-terminals that derive epsilon. This is done by iterating over all non-terminals and their productions, and checking if any of them derive the empty string (''). If so, the non-terminal is added to a set called epsilons.
   2. Generate new productions that exclude epsilon productions. This is done by iterating over all productions, and for each production, checking if any of its symbols can be replaced with the empty string. If so, a new production is generated where that symbol is removed. If the resulting right-hand side is also the empty string and the left-hand side is not already in epsilons, the new production is discarded. Otherwise, the new production is added to the set of productions for the corresponding non-terminal.
   3. Remove epsilon productions. This is done by iterating over all productions for each non-terminal, and removing any production that contains the empty string on the right-hand side, unless all the symbols on the right-hand side are in epsilons.

   The resulting set of productions is returned as the output CFG. The method stores the new CFG with no epsilon productions in the eps_P variable and returns it when the method is called again without modifying the original CFG.

```jupyterpython
def eliminate_epsilon(self):
        if self.eps_P is None:
            # Step 1: Identify all non-terminals that derive epsilon
            epsilons = set()
            for A in VN:
                if '' in P.get(A, []):
                    epsilons.add(A)

            # Step 2: Generate new productions that exclude epsilon productions
            new_P = dict(P)
            for A in VN:
                for rhs in P.get(A, []):
                    if rhs == '':
                        continue
                    for i in range(len(rhs)):
                        if rhs[i] not in epsilons:
                            continue
                        # Replace epsilon with empty string
                        new_rhs = rhs[:i] + rhs[i+1:]
                        if new_rhs == '' and A not in epsilons:
                            continue
                        # Add new production to the grammar
                        if A not in new_P:
                            new_P[A] = []
                        if new_rhs not in new_P[A]:
                            new_P[A].append(new_rhs)

            # Step 3: Remove epsilon productions
            for A in VN:
                new_rhs = []
                for rhs in new_P.get(A, []):
                    if rhs == '':
                        continue
                    if not all(X in epsilons for X in rhs):
                        new_rhs.append(rhs)
                new_P[A] = new_rhs

            self.eps_P = new_P
            
        return self.eps_P
```
### Step 2. Elimination of renamings:
   #### The algorithm consists of three steps:

  1. Remove unit rules of the form A -> A. This is done by iterating over all non-terminals, and for each non-terminal, checking if it has a production of the form A -> A. If so, this production is removed from the set of productions for the non-terminal.
  2. Eliminate all other unit rules. This is done by iterating over all non-terminals, and for each non-terminal that does not have a production of the form A -> A, it is checked if it has any unit productions (productions of the form A -> B, where B is a non-terminal). If so, the production is removed from the set of productions for the non-terminal, and all productions for B are added to the set of productions for A.
  3. Remove duplicate productions. This is done by iterating over all non-terminals and removing any duplicate productions in their set of productions.

The resulting set of productions is returned as the output CFG. The method stores the new CFG with no unit productions in the unit_P variable and returns it when the method is called again without modifying the original CFG.

```jupyterpython
def eliminate_unit_rules(self):
        
        if self.unit_P is None:
            # Step 1: Remove unit rules of the form A -> A
            new_P = {}
            for A in VN:
                if A in P and A not in P[A]:
                    new_P[A] = P[A]

            # Step 2: Eliminate all other unit rules
            for A in VN:
                if A not in new_P:
                    new_P[A] = []
                for B in new_P[A]:
                    if B in new_P:
                        new_P[A].remove(B)
                        new_P[A].extend(new_P[B])

            # Step 3: Remove duplicate productions
            for A in VN:
                if A in new_P:
                    new_P[A] = list(set(new_P[A]))
            
            self.unit_P = new_P
        return self.unit_P
```

### Step 3. Elimination of non-productive symbols:
   #### The algorithm consists of three steps:

   1. Initialize the set of productive symbols as the set of terminals.
   2. Repeatedly update the set of productive symbols until it no longer changes. For each non-terminal A, if all the non-terminals in its productions are productive, then add A to the set of productive symbols.
   3. Construct a new set of productions using only the productive non-terminals.

The resulting set of productions is returned as the output CFG. The method stores the new CFG with only the productive non-terminals in the prod_P variable and returns it when the method is called again without modifying the original CFG.


```jupyterpython
    def find_productive_symbols(self):
        
        if self.prod_P is None:
            productive = set(VT)
            old_productive = set()

            while old_productive != productive:
                old_productive = productive.copy()
                for A in VN:
                    for production in P[A]:
                        if all((B in productive) for B in production):
                            productive.add(A)

            productive_P = { A: [production for production in P[A] if all((B in productive) for B in production)] for A in VN }
            
            self.prod_P = productive_P
            
        return self.prod_P
```

### Step 4. Elimination of inaccessible symbols:
   #### The algorithm consists of three steps:
   1. Initialize the set of accessible non-terminals with the start symbol.
   2. For each non-terminal in the accessible set, add any non-terminals that appear in its productions to the accessible set.
   3. Construct a new set of productions using only the accessible non-terminals.

The resulting set of productions is returned as the output CFG. The method stores the new CFG with only the accessible non-terminals in the acc_P variable and returns it when the method is called again without modifying the original CFG.

```jupyterpython
def get_accessible_symbols(self):
        
        if self.acc_P is None:
            accessible = []
            new_P = dict()
            for i in range(len(P)):
                for state, production in P.items():
                    for prod in production:
                        for var in prod:
                            if var in VN:
                                if var not in accessible:
                                    accessible.append(var)

            for el in accessible:
                new_P[el] = P[el]
            
            self.acc_P = new_P
            
        return self.acc_P
```

### Step 5. Obtain the Chomsky Normal Form:
   The function first initializes some variables with the current production rules and the set of nonterminal and terminal symbols. It then checks whether the grammar is already in Chomsky normal form; if so, it simply returns the current set of production rules.

If the grammar is not already in CNF, the function proceeds to iterate through the production rules, replacing any production rule of length greater than two with a series of productions in CNF. To do this, it creates new nonterminal symbols to represent any terminals, and replaces the original production rule with a sequence of production rules in which each right-hand side consists of either two nonterminal symbols or a single terminal symbol.

The function continues to iterate through the production rules until it has replaced all non-CNF production rules. Finally, it returns the resulting set of production rules and the set of nonterminal symbols in the CNF grammar.


```jupyterpython
def chomsky_norm_form(self):
       ...
            while changed == True:
                changed = False
                for state, production in new_production.items():
                    for ind, prod in enumerate(production):
                        if len(prod) <= 2:
                            if len(prod) == 1:
                                continue
                            else:
                                if prod[0] in new_VN and prod[1] in new_VN:
                                    continue
                                else:
                                    for ind_var, var in enumerate(prod):
                                        if var not in new_variables and var in VT:
                                            new_variables[var] = possible_variables[-1]
                                            new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind][ind_var], possible_variables[-1])      
                                            new_VN.append(possible_variables[-1])
                                            possible_variables.pop()
                                            changed = True
                                        elif var in new_variables and var in VT:
                                            new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind][ind_var], new_variables[new_production[state][ind][ind_var]])
                                            changed = True
                        elif len(prod) > 2:
                          ...
                          # (logic if the length of the produciton if larger than 2)
                          ...
                   
            for old_var, new_var in new_variables.items():
                new_production[new_var] = old_var
            
            self.chomsky_P = new_production
            self.chomsky_VN = new_VN
            
        return self.chomsky_VN, self.chomsky_P
```
### Final Transformation:
In the end there is a "transform" function that runs all the methods provided.
```jupyterpython
def transform(self):
        _ = self.eliminate_epsilon()
        _ = self.eliminate_unit_rules()
        _ = self.find_productive_symbols()
        _ = self.get_accessible_symbols()
        _ = self.chomsky_norm_form()
        return self.chomsky_VN, self.VT, self.chomsky_P
```

## Conclusions / Screenshots / Results

In conclusion, implementing Chomsky Normal Form conversion algorithm can be a complex task, as demonstrated by the code provided. However, the benefits of converting a context-free grammar to CNF include simplifying the grammar and facilitating parsing algorithms. The code provided appears to handle the conversion process effectively, utilizing a set of rules and heuristics to transform the grammar into CNF (said by ChatGPT :) ) That means my implementation should work for almost any context free grammar. Overall, this implementation serves as a useful tool for anyone working with context-free grammars and parsing algorithms.

<b>Results:</b>
Chomsky conversion test:

```jupyterpython
VN = ['S', 'A', 'B', 'C', 'E']
VT = ['a', 'b']
P = {'S': ['aB', 'AC', 'A'], 
     'A': ['a', 'ACSC', 'BC', 'ASC', 'ACS', 'B', 'AS'], 
     'B': ['b', 'aA'], 
     'C': ['', 'BA'], 
     'E': ['bB']}

chomsky = Chomsky(VN, VT, P, "S").transform()
print("VN = ", chomsky[0])
print("VT = ", chomsky[1])
print("P = ", chomsky[2])
```
Result:
```
VN =  ['S', 'A', 'B', 'C', 'E', 'Z', 'Y', 'X', 'W']
VT =  ['a', 'b']
P =  {'A': ['AS', 'WC', 'YA', 'b', 'a', 'ZS', 'XC', 'BC'], 'S': ['AS', 'WC', 'YA', 'b', 'YB', 'a', 'AC', 'XC', 'ZS', 'BC'], 'C': ['BA'], 'B': ['b', 'YA'], 'Z': 'AC', 'Y': 'a', 'X': 'AS', 'W': 'ZS'}
```

## References
* https://drive.google.com/file/d/19muyiabGeGaoNDK-7PeuzYYDe6_c0e-t/view
* https://jayd.ml/algorithms/chomsky.html
* https://else.fcim.utm.md/pluginfile.php/12810/mod_resource/content/0/Chomsky%20Normal%20Form%20Example.pdf
* https://github.com/DrVasile/FLFA-Labs/
* https://www.google.com/search?q=chomsky+normal+form++from+any+grammar&sxsrf=APwXEdejXer7saQAzzCiUN1qdlffDHSWoQ%3A1681563059715&ei=s506ZI-vK5SbkgW1somIBQ&ved=0ahUKEwjP1N3G9qv-AhWUjaQKHTVZAlEQ4dUDCA8&uact=5&oq=chomsky+normal+form++from+any+grammar&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAEyBQghEKABMgoIIRAWEB4QDxAdMgoIIRAWEB4QDxAdOgoIABBHENYEELADOggIIRAWEB4QHToHCCEQoAEQCkoECEEYAFCSDVi_JWD2J2gEcAF4AIABlAGIAbgHkgEDMS43mAEAoAEByAEIwAEB&sclient=gws-wiz-serp#fpstate=ive&vld=cid:550903ec,vid:eUlUzH9fmXQ
