import pytest
from src.robot.memory import Memory


@pytest.mark.parametrize(
    "initial_intervals, key, start, end, expected_intervals",
    [
        # no initial interval
        ([], 1, 5, 10, [(5, 10)]),
        # new interval added at start
        ([(15, 20)], 1, 5, 10, [(5, 10), (15, 20)]),
        # new interval added at end
        ([(5, 10)], 1, 15, 20, [(5, 10), (15, 20)]),
        # interval starts exactly after previous interval, making it one interval
        ([(5, 10)], 1, 11, 17, [(5, 17)]),
        # interval end exactly before next interval, making it one interval
        ([(5, 10)], 1, 1, 4, [(1, 10)]),
        # new interval merges two prev intervals
        ([(5, 10), (15, 20)], 1, 8, 17, [(5, 20)]),
        # new interval merges with next interval
        ([(5, 10)], 1, 1, 5, [(1, 10)]),
        # new interval merges with prev interval
        ([(5, 10)], 1, 10, 20, [(5, 20)]),
    ],
)
def test_add_interval(initial_intervals, key, start, end, expected_intervals):
    memory = Memory()
    memory.h_mov[key] = initial_intervals.copy()

    memory._add_interval(memory.h_mov, key, start, end)

    assert memory.h_mov[key] == expected_intervals


@pytest.mark.parametrize(
    "h_mov, v_mov, expected_visited",
    [
        # no overlap
        ({0: [(0, 5)]}, {10: [(0, 5)]}, 12),
        # full overlap
        ({0: [(0, 2)], 1: [(0, 2)]}, {0: [(0, 1)], 1: [(0, 1)], 2: [(0, 1)]}, 6),
        # partial overlap
        ({0: [(0, 5)], 1: [(1, 4)]}, {1: [(0, 5)]}, 14),
        # advanced movement
        ({0: [(0, 5)], 2: [(0, 5)]}, {2: [(0, 5)], 3: [(0, 2)]}, 17),
    ],
)
def test_calculate_visited(h_mov, v_mov, expected_visited):
    memory = Memory()

    memory.h_mov = h_mov
    memory.v_mov = v_mov

    assert memory.calculate_visited() == expected_visited
