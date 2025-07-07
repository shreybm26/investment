Dolev-Strong Protocol Simulation for Byzantine Fault Tolerance

This Python program simulates a distributed consensus protocol inspired by the Dolev-Strong algorithm with the help of the book, "Foundations of Distributed Consensus and Blockchains" by Elaine Shi.

It is intended to depict a network of agents (nodes), some of which may be Byzantine (malicious), and demonstrates how honest agents can reach consensus on a single bit value despite the presence of faulty nodes.

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