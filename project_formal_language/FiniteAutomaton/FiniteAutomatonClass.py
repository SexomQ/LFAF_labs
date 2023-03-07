from collections import deque

class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def check_automaton(self, word):
        q = self.q0
        for c in word:
            if c not in self.Sigma:
                return False
            q = self.delta[q].get(c)
            if q is None:
                return False
        return q in self.F
    
    def finite_automaton_to_regular_grammar(self):
        # Initialize the productions of the regular grammar
        productions = {}
        for state in self.Q:
            productions[state] = []

        # Add the productions for each transition
        for (state, symbol, order), next_states in self.delta.items():
            for next_state in next_states:
                productions[state].append(symbol + next_state)

        VN = self.Q
        VT = self.Sigma
        P = productions
        
        # Return the VN, VT, and P variables separately
        return VN, VT, P
    
    def is_deterministic(self):
        # Create a set to keep track of the next states for each state and input symbol
        next_states = set()

        # Iterate over all transitions
        for (state, symbol, val), next_state in self.delta.items():
            # Check if there is already a transition for the same state and input symbol
            if (state, symbol) in next_states:
                return False
            else:
                # Add the current transition to the set of next states
                next_states.add((state, symbol))

        # If no duplicate transitions were found, the automaton is deterministic
        return True
    
    

    # Define the DFA transition function
    def nfa_to_dfa(self):
        def epsilon_closure(state, transitions):
            closure = {state}
            queue = deque([state])
            while queue:
                current_state = queue.popleft()
                for (s, c, t), next_ in transitions.items():
                    if s == current_state and c == "" and next_[0] not in closure:
                        closure.add(next_[0])
                        queue.append(next_[0])
            return closure
    
        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = []
        queue = deque([epsilon_closure(self.q0, self.delta)])
        dfa_states.append(queue[0])
        while queue:
            current_state = queue.popleft()
            for symbol in self.Sigma:
                next_state = set()
                for nfa_state in current_state:
                    for (s, c, t), next_ in self.delta.items():
                        if s == nfa_state and c == symbol:
                            next_state.update(epsilon_closure(next_[0], self.delta))
                if next_state:
                    if next_state not in dfa_states:
                        dfa_states.append(next_state)
                        queue.append(next_state)
                    dfa_transitions[(tuple(current_state), symbol)] = tuple(next_state)
            if any(nfa_state in self.F for nfa_state in current_state):
                dfa_final_states.append(tuple(current_state))
        return dfa_states, self.Sigma, dfa_transitions, dfa_final_states