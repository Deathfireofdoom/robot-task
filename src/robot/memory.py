from collections import defaultdict


class Memory:
    def __init__(self) -> None:
        self.h_mov = defaultdict(list)
        self.v_mov = defaultdict(list)

    def add_movement(self, x_start: int, y_start: int, x_end: int, y_end: int):
        # horizontal movement
        if y_start == y_end:
            self._add_interval(self.h_mov, y_start, x_start, x_end)

        # vertical movement
        elif x_start == x_end:
            self._add_interval(self.v_mov, x_start, y_start, y_end)

    def _add_interval(self, movement_dict: dict, key: int, start: int, end: int):
        # crucial for later logic to have start before end
        if start > end:
            start, end = end, start

        intervals = movement_dict[key]
        new_intervals = []
        placed = False


        # TODO(oe): A potential improvement is to add early esacpe here,
        # when the interval has been placed we could in theory just append
        # the rest of the intervals, instead of looping them one by one.
        for i_start, i_end in intervals:
            if end < i_start - 1:
                # no overlap - place before current one
                if not placed:
                    new_intervals.append((start, end))
                    placed = True
                new_intervals.append((i_start, i_end))
            elif start > i_end + 1:
                # no overlap - place after the current one
                new_intervals.append((i_start, i_end))
            else:
                # overlap - update end and start
                start = min(start, i_start)
                end = max(end, i_end)

        # not placed yet, so the interval is in the end
        if not placed:
            new_intervals.append((start, end))

        # TODO(oe): This part is leveraging the fact that dicts are passed
        # by reference in Python, so updating this dict will update the 
        # original one (its the same).
        #
        # This may or may not be a good way to do it, since it can cause
        # confusion for devs not aware of this.
        movement_dict[key] = new_intervals

    def calculate_visited(self) -> int:
        total_visited = 0

        # unique visited horizontal
        for y, intervals in self.h_mov.items():
            for x_start, x_end in intervals:
                total_visited += x_end - x_start + 1

        # unique visited vertical
        for x, intervals in self.v_mov.items():
            for y_start, y_end in intervals:
                total_visited += y_end - y_start + 1

        # remove overlap
        total_visited -= self.calculate_overlap()

        return total_visited

    def calculate_overlap(self) -> int:
        overlap_count = 0

        # check for overlap between horizontal and vertical intervals
        for y, h_intervals in self.h_mov.items():
            # iterate over horizontal intervals for the current y
            for x_start, x_end in h_intervals:
                # check all vertical intervals for overlap
                for x, v_intervals in self.v_mov.items():
                    # check if the x is within the current horizontal interval
                    if x_start <= x <= x_end:
                        # iterate over vertical intervals for the current x
                        for y_start, y_end in v_intervals:
                            # check if the y is within the current vertical interval
                            if y_start <= y <= y_end:
                                # increment overlap count for each overlapping point
                                overlap_count += 1

        return overlap_count
