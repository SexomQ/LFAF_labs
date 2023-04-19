class Chomsky:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.eps_P = None
        self.unit_P = None
        self.prod_P = None
        self.acc_P = None
        self.chomsky_P = None
        self.chomsky_VN = None
    
    def eliminate_epsilon(self):
        VN = self.VN
        VT = self.VT
        P = self.P
        S = self.S
        
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

    def eliminate_unit_rules(self):
        VN = self.VN
        VT = self.VT
        P = self.eps_P
        S = self.S
        
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
    
    def find_productive_symbols(self):
        VN = self.VN
        VT = self.VT
        P = self.unit_P
        S = self.S
        
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
    
    def get_accessible_symbols(self):
        VN = self.VN
        VT = self.VT
        P = self.prod_P
        S = self.S
        
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
    
    def chomsky_norm_form(self):
        VN = self.VN
        VT = self.VT
        P = self.acc_P
        S = self.S
        
        if self.chomsky_P is None:
            new_production = {}
            new_variables = {}
            new_VN = []

            new_production = P.copy()
            possible_variables = ['G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            new_VN = VN.copy()
            changed = True

            while changed == True:
                changed = False
        #         print(new_production)
                for state, production in new_production.items():
        #             print(state)
        #             print(new_variables)
                    for ind, prod in enumerate(production):
                        if len(prod) <= 2:
                            if len(prod) == 1:
                                continue
                            else:
        #                         print("passed")
                                if prod[0] in new_VN and prod[1] in new_VN:
                                    continue
                                else:
                                    for ind_var, var in enumerate(prod):
        #                                 print(var, "---------------------")
                                        if var not in new_variables and var in VT:
        #                                     print(var, "found")
                                            new_variables[var] = possible_variables[-1]
                                            new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind][ind_var], possible_variables[-1])      
                                            new_VN.append(possible_variables[-1])
                                            possible_variables.pop()
                                            changed = True
                                        elif var in new_variables and var in VT:
                                            new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind][ind_var], new_variables[new_production[state][ind][ind_var]])
                                            changed = True
                        elif len(prod) > 2:
        #                     print(prod)
        #                     print(new_VN)
                            if prod[0] in new_VN and prod[1] in new_VN and (prod[0] + prod[1]) not in new_variables:
                                new_variables[new_production[state][ind][:2]] = possible_variables[-1] # This is the first
                                new_production[state][ind] = new_production[state][ind].replace(prod[0] + prod[1], possible_variables[-1])
                                new_VN.append(possible_variables[-1])
                                possible_variables.pop()
                                changed = True
        #                         print("here")

                            elif prod[0] in new_VN and prod[1] in new_VN and (prod[0] + prod[1]) in new_variables:
                                new_production[state][ind] = new_production[state][ind].replace(prod[0] + prod[1], new_variables[prod[0] + prod[1]])
                                changed = True

                            elif prod[0] in new_VN and prod[1] not in new_VN and prod[1] not in new_variables:
        #                         print("this")
                                new_variables[new_production[state][ind][1]] = possible_variables[-1]
                                new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind], prod[1] + possible_variables[-1]) 
                                new_VN.append(possible_variables[-1])
                                possible_variables.pop()
                                changed = True

                            elif prod[0] in new_VN and prod[1] not in new_VN and prod[1] in new_variables:
        #                         print("that")
                                new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind], prod[0] + new_variables[prod[1]])
                                changed = True

                            elif prod[1] in new_VN and prod[0] not in new_VN and prod[0] not in new_variables:
        #                         print("this_2")
                                new_variables[new_production[state][ind][0]] = possible_variables[-1]
                                new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind], possible_variables[-1] + prod[1]) 
                                new_VN.append(possible_variables[-1])
                                possible_variables.pop()
                                changed = True

                            elif prod[1] in new_VN and prod[0] not in new_VN and prod[0] in new_variables:
        #                         print("this_3")
                                new_production[state][ind] = new_production[state][ind].replace(new_production[state][ind], new_variables[prod[1]] + prod[1])
                                changed = True          
                            else:
                                continue
                                changed = False

            for old_var, new_var in new_variables.items():
                new_production[new_var] = old_var
            
            self.chomsky_P = new_production
            self.chomsky_VN = new_VN
            
        return self.chomsky_VN, self.chomsky_P
        
    def transform(self):
        _ = self.eliminate_epsilon()
        _ = self.eliminate_unit_rules()
        _ = self.find_productive_symbols()
        _ = self.get_accessible_symbols()
        _ = self.chomsky_norm_form()
        return self.chomsky_VN, self.VT, self.chomsky_P