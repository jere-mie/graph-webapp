import networkx as nx
from myHHFunction import graph_exists

deg_seqs = [
    ([5, 1, 1, 1, 1, 1], True),
    ([6, 6, 5, 4, 3, 3, 3, 3, 2, 1, 0, 0, 0], True),
    ([4, 3, 2, 2, 1], True),
    ([4, 3, 2, 2, 2], False),
    ([5, 4, 4, 2, 2, 2], False),
    ([5, 4, 4, 2, 2, 1], False),
    ([7, 6, 5, 4, 4, 3, 2, 1], True),
    ([7, 6, 5, 4, 3, 2, 1], False)
]

for deg_seq, expected_result in deg_seqs:
    result = graph_exists(len(deg_seq), deg_seq)
    assert result == expected_result, f"For degree sequence {deg_seq}, expected {expected_result}, but got {result}"

print("All test cases passed!")
