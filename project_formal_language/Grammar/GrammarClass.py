import random as r
from FiniteAutomaton.FiniteAutomatonClass import FiniteAutomaton


class Grammar(FiniteAutomaton):
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.string = self.S

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

    def delete_string(self):
        self.string = self.S
        return self

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
    
    def check_grammar(self):
        type_0 = True
        type_1 = True
        type_2 = True
        type_3 = True

        type_3_left = True
        type_3_right = True

        for state, productions in self.P.items():
            for production in productions:
                # check if the grammar exist
                for char in production:
                    if char not in self.VT + self.VN:
                        type_0 = False
                        type_1 = False
                        type_3 = False
                        type_2 = False
                        type_3_left = False
                        type_3_right = False
                        return f"The {char} is not in grammar"

                for ch in state:
                    if ch not in self.VT + self.VN:
                        type_0 = False
                        type_1 = False
                        type_3 = False
                        type_2 = False
                        type_3_left = False
                        type_3_right = False
                        return f"The {char} is not in grammar"

                # check if type 1 or 0
                if (len(production) > 2 or len(state) > 1) and any([state_v in self.VN for state_v in state]):
                    type_2, type_3 = False, False
                    type_3_left = False
                    type_3_right = False

                # check type 1
                if any([ch in self.VN for ch in state]):
                    print("", end='')
                else:
                    type_1 = False
                    type_2, type_3 = False, False
                    type_3_left = False
                    type_3_right = False

                # type 2 or 3
                if len(production) <= 2 and len(state) == 1 and type_2:
                    if any([char_r in self.VN or len(char_r) == 0 for char_r in [production[1:]]]):
                        print("", end='')
                    else: type_3_right = False

                    if any([char_l in self.VN or len(char_l) == 0 for char_l in [production[0:1]]]):
                        print("", end='')
                    else: type_3_left = False

        if type_3_left or type_3_right:
            print(f"The grammar is type 3")
        elif type_2:
            print(f"The grammar is type 2")
        elif type_1:
            print(f"The grammar is type 1")
        elif type_0:
            print(f"The grammar is type 0")

