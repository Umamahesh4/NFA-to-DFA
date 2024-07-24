import graphviz

def create_nfa_image(states, alphabet, transitions, start_state, accept_states):
    nfa_graph = graphviz.Digraph('NFA', format='png', engine='dot')

    for state in states:
        nfa_graph.node(state, shape='circle', color='black')

    nfa_graph.node(start_state, shape='doublecircle', color='red')

    for accept_state in accept_states:
        nfa_graph.node(accept_state, shape='doublecircle', color='green')

    for (source, symbol), destinations in transitions.items():
        for destination in destinations:
            nfa_graph.edge(source, destination, label=symbol)

    nfa_graph.render('nfa_graph', cleanup=True, format='png', engine='dot')
    print("NFA Image generated and saved as 'nfa_graph.png'.")

def create_dfa_image(states, alphabet, transitions, start_state, accept_states):
    dfa_graph = graphviz.Digraph('DFA', format='png', engine='dot')

    for state in states:
        dfa_graph.node(str(state), shape='circle', color='black')

    dfa_graph.node(str(start_state), shape='doublecircle', color='red')

    for accept_state in accept_states:
        dfa_graph.node(str(accept_state), shape='doublecircle', color='green')

    for (source, symbol), destination in transitions.items():
        dfa_graph.edge(str(source), str(destination), label=symbol)

    dfa_graph.render('dfa_graph', cleanup=True, format='png', engine='dot')
    print("DFA Image generated and saved as 'dfa_graph.png'.")

def powerset(states):
    result = []
    for i in range(2 ** len(states)):
        subset = [states[j] for j in range(len(states)) if (i & (1 << j)) > 0]
        result.append(subset)
    return result


def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        epsilon_transitions = transitions.get((current_state, ''), frozenset())

        for next_state in epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return frozenset(closure)


def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions.get((state, symbol), frozenset()))
    return frozenset(result)


def nfa_to_dfa(nfa_states, alphabet, transitions, start_state, accept_states):
    dfa_states = set()
    dfa_transitions = {}

    # Start with the start state of the NFA
    dfa_start_state = frozenset({start_state})
    dfa_states.add(dfa_start_state)
    stack = [dfa_start_state]

    while stack:
        current_states = stack.pop()

        for symbol in alphabet:
            next_states = epsilon_closure(move(current_states, symbol, transitions), transitions)

            if next_states:
                if next_states not in dfa_states:
                    dfa_states.add(next_states)
                    stack.append(next_states)

                dfa_transitions[(current_states, symbol)] = next_states
            else:
                # Create a trap state
                trap_state = frozenset({'Trap'})
                dfa_states.add(trap_state)
                dfa_transitions[(current_states, symbol)] = trap_state

    # Get the accept states for the DFA
    dfa_accept_states = [state for state in dfa_states if any(s in accept_states for s in state)]

    return dfa_states, alphabet, dfa_transitions, dfa_start_state, dfa_accept_states


def display_transition_table(states, alphabet, transitions):
    print("\nTransition Table:")
    header = ["State"] + [str(symbol) for symbol in alphabet + ['']]
    print("\t".join(header))

    for state in states:
        row = [str(state)]
        for symbol in alphabet + ['']:
            next_states = transitions.get((state, symbol), frozenset())
            row.append(','.join(map(str, next_states)))
        print("\t".join(row))


def display_dfa(states, alphabet, transitions, start_state, accept_states):
    print("\nDFA:")
    print("States:", states)
    print("Alphabet:", alphabet)
    print("Transitions:")
    for (source, symbol), destination in transitions.items():
        print(f"  {source} --({symbol})--> {destination}")
    print("Start State:", start_state)
    print("Accept States:", accept_states)


# Input NFA from the user
nfa_states = input("Enter NFA states (comma-separated): ").split(',')
alphabet = input("Enter alphabet symbols (comma-separated): ").split(',')
transitions = {}
while True:
    transition_input = input("Enter transition (source,symbol,destination) or type 'done' to finish: ")
    if transition_input.lower() == 'done':
        break
    source, symbol, destination = transition_input.split(',')


#     transitions.get((source, symbol), frozenset()): This retrieves the value corresponding to the key (source, symbol) from the transitions dictionary. If the key is not present in the dictionary, it returns an empty frozenset().
# frozenset([destination]): This creates a frozenset containing only the destination state. The destination state is added to a frozenset to ensure immutability.
# ... | ...: This performs a set union operation between the frozenset obtained from the dictionary (or an empty frozenset if the key is not present) and the frozenset containing the destination state. This ensures that the new destination state is added to the set of states for the given source and symbol.
# transitions[(source, symbol)] = ...: This assigns the result of the set union operation back to the transitions dictionary at the key (source, symbol). If there were existing transitions for the same source and symbol, the new destination state is added to them.
# Essentially, this line adds or updates a transition in the transitions dictionary based on the parsed source, symbol, and destination from the input string.


    transitions[(source, symbol)] = transitions.get((source, symbol), frozenset()) | frozenset([destination])

start_state = input("Enter start state: ")
accept_states = input("Enter accept states (comma-separated): ").split('@@')

# Convert NFA to DFA
dfa_states, dfa_alphabet, dfa_transitions, dfa_start_state, dfa_accept_states = nfa_to_dfa(
    nfa_states, alphabet, transitions, start_state, accept_states
)

# Display NFA Transition Table
display_transition_table(nfa_states, alphabet, transitions)

# Display NFA Image
create_nfa_image(nfa_states, alphabet, transitions, start_state, accept_states)

# Display DFA Transition Table
display_transition_table(dfa_states, dfa_alphabet, dfa_transitions)

# Display DFA Image
create_dfa_image(dfa_states, dfa_alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

# Display DFA
display_dfa(dfa_states, dfa_alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)