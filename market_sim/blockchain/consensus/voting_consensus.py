"""
Dolev-Strong Protocol Simulation for Byzantine Fault Tolerance

This Python program simulates a distributed consensus protocol inspired by the Dolev-Strong algorithm with the help of the book, "Foundations of Distributed Consensus and Blockchains" by Elaine Shi.

It is intended to depict a network of agents (nodes), some of which may be Byzantine (malicious), and demonstrates how
honest agents can reach consensus on a single bit value despite the presence of faulty nodes.

Key Components:
---------------
- `Msg`: Represents a message containing a value and a list of signatures from the nodes it has been forwarded.
- `Agent`: Simulates an agent in the system, which may be honest or Byzantine. Handles sending, receiving, and deciding on a final value based on received messages.
- `VotingSim`: This is the function responsible for the simulation of the voting amongst the agents, message rounds, and agent interaction.
- `visualize()`: Uses NetworkX and Matplotlib libraries to visualize the message flow between agents as a weighted directed graph.
- `test_consensus()`: Verifies that all honest agents reach the same decision and that Byzantine agents return valid bits.
- `run_all_tests()`: Runs multiple test scenarios with varying configurations of agents and Byzantine faults.

Notes:
------
- The `visualize()` function inside the `VotingSim` class has been commented out because it opens a graph window. It works correctly and is best used for debugging or inspecting individual test cases visually.

"""


import random

#To run the visualization function, these libraries are required to be installed using pip, if not already installed.
import networkx as nx
import matplotlib.pyplot as plt

bits = ["0", "1"] 

class Msg:
    def __init__(self, value, signs):
        self.value = value
        self.signs = signs

    def add_sign(self, agent_id):
        if agent_id not in self.signs: #To prevent redundancy 
            self.signs.append(agent_id)

    def copy(self):
        return Msg(self.value, self.signs[:])

    def __repr__(self):
        return f"<{self.value}, signs={self.signs}>"

class Agent:
    def __init__(self, agent_id, isByzantine=False):
        self.id = agent_id
        self.isByzantine = isByzantine
        self.inbox = []
        self.final_msgs = []

    def receive(self, msg):
        if len(set(msg.signs)) != len(msg.signs): #A check for duplicate signatures
            return
        
        key = (msg.value, tuple(msg.signs))
        inbox_keys = {(m.value, tuple(m.signs)) for m in self.inbox}
        
        if key not in inbox_keys:
            self.inbox.append(msg)

    def send(self, round_num, agents):
        if round_num == 0:
            if self.isByzantine: #If the node (agent) is byzantine then send random bits to all other nodes
                val = random.choice(bits) 
            else:
                val="1" #If the node is an honest node, then send an honest bit (1) to all other nodes
            for agent in agents:
                agent.receive(Msg(val, [self.id]))
        else:
            #For subsequent rounds after the initial round, forward the messages from the inbox that have exactly "round_num" signatures
            for msg in self.inbox:
                if len(msg.signs) == round_num:
                    new_msg = msg.copy()
                    new_msg.add_sign(self.id)
                    for agent in agents:
                        if not self.isByzantine:
                            agent.receive(new_msg)

    def decide(self, f):
        if self.isByzantine:
            return random.choice(bits)
        extr = set() #The set of extracted bits as used in the Dolev-Strong Protocol
        for msg in self.inbox:
            if len(msg.signs) == f + 1:
                extr.add(msg.value)
        if len(extr) == 1:
            return list(extr)[0]
        return "0"

class VotingSim:
    def __init__(self, n, f, bad_ids):
        self.f = f
        self.agents = [Agent(i, isByzantine=(i in bad_ids)) for i in range(n)]

    def run(self):
        for r in range(self.f + 1):
            for agent in self.agents:
                agent.send(r, self.agents)

        result = {}
        for agent in self.agents:
            result[agent.id] = agent.decide(self.f)
        return result
    
    # def visualize(self):
    #     G = nx.DiGraph()
    #     for agent in self.agents:
    #         G.add_node(agent.id)
    #     for agent in self.agents:
    #         for msg in agent.inbox:
    #             # For each signature except the receiver, add an edge signer -> receiver
    #             for signer in msg.signs:
    #                 if signer != agent.id:
    #                     G.add_edge(signer, agent.id, label=msg.value)
    #     pos = nx.circular_layout(G)
    #     nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, arrowsize=20)
    #     edge_labels = nx.get_edge_attributes(G, 'label')
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #     plt.title("Message passing in VotingSim")
    #     plt.show()

def test_consensus(n, f, byz):
    print(f"Results for test: n={n}, f={f}, byzantine={byz}")
    sim = VotingSim(n, f, byz)
    results = sim.run()

    honest_decisions = []
    byz_decisions = []

    for A_id, val in results.items():
        if A_id not in byz:
            honest_decisions.append(val)
        else:
            byz_decisions.append(val)

    #A check to see if all honest agents agree on a single bit
    unique_honest = []
    for val in honest_decisions:
        if val not in unique_honest:
            unique_honest.append(val)
    assert len(unique_honest) == 1, "Honest agents disagree"

    #A check to see that all Byzantine agents' outputs are valid bits
    for val in byz_decisions:
        assert val in bits, "Invalid output from Byzantine agents"

    for A_id, val in results.items():
        print(f"Agent {A_id}: {val}")
    print("Test passed: honest agents agree, Byzantine agents outputs are valid.\n")


def run_all_tests():
    print("\n===== RUNNING ALL TESTS =====\n")

    # Test 1: No Byzantine agents
    print("----- Test 1: No Byzantine agents -----")
    test_consensus(n=5, f=0, byz=[])

    # Test 2: Maximum tolerated Byzantine agents
    print("----- Test 2: Max Byzantine tolerated (n=7, f=2) -----")
    test_consensus(n=7, f=2, byz=[1, 3])

    # Test 3: Byzantine agents in different positions
    print("----- Test 3: Byzantine agents at start and end -----")
    test_consensus(n=7, f=2, byz=[0, 6])

    # Test 4: Larger network
    print("----- Test 4: Larger network (n=10, f=3) -----")
    test_consensus(n=10, f=3, byz=[2, 5, 7])

    # Test 5: All agents honest with even higher n
    print("----- Test 5: All honest agents (n=9, f=0) -----")
    test_consensus(n=9, f=0, byz=[])

    print("===== ALL TESTS COMPLETED =====\n")


if __name__ == "__main__":
    #Default setup
    n = 7
    f = 2
    byz = [1, 3]
    sim = VotingSim(n, f, byz)
    out = sim.run()
    for agent in sim.agents:
        extr = set()
        for msg in agent.inbox:
            if len(msg.signs) == f + 1:
                extr.add(msg.value)
        print(f"Agent {agent.id} extr with f+1 signs: {extr}")

    print("Final decisions:")
    for A_id, val in out.items():
        print(f"Agent {A_id}: {val}")

    # sim.visualize()

    run_all_tests()