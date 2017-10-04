import numpy as np
import pandas as pd
import copy


def initial_maps():
    maps = []
    for _ in range(3):
        row_maps = []
        for __ in range(3):
            row_maps.append([0 for _ in range(9)])
        maps.append(row_maps)
    return maps


def get_neighbour(index, maps):
    row_i = index // 3
    col_i = index % 3
    if row_i == 0:
        col_map1 = maps[row_i + 1][col_i]
        col_map2 = maps[row_i + 2][col_i]
    elif row_i == 1:
        col_map1 = maps[row_i - 1][col_i]
        col_map2 = maps[row_i + 1][col_i]
    else:
        col_map1 = maps[row_i - 1][col_i]
        col_map2 = maps[row_i - 2][col_i]

    if col_i == 0:
        row_map1 = maps[row_i][col_i + 1]
        row_map2 = maps[row_i][col_i + 2]
    elif col_i == 1:
        row_map1 = maps[row_i][col_i - 1]
        row_map2 = maps[row_i][col_i + 1]
    else:
        row_map1 = maps[row_i][col_i - 1]
        row_map2 = maps[row_i][col_i - 2]

    row = pd.concat([pd.DataFrame(np.array(row_map1).reshape(3, 3)),
                     pd.DataFrame(np.array(row_map2).reshape(3, 3))], axis=1)
    col = pd.concat([pd.DataFrame(np.array(col_map1).reshape(3, 3)).transpose(),
                     pd.DataFrame(np.array(col_map2).reshape(3, 3)).transpose()], axis=1)
    return row, col


def display_maps(maps):
    def display_row(rows):
        for each in rows:
            print(each, end='  ')
        print()

    def display_row_maps(row_maps):
        for _i in range(0, 9, 3):
            rows = []
            for part in row_maps:
                rows.append(part[_i:_i+3])
            display_row(rows)
    print('The Sudoku Matrix')
    print('-' * 30)
    for i, row_maps in enumerate(maps):
        display_row_maps(row_maps)
        if i != 2:
            print()
        else:
            print('-' * 30)


class SudokuB:
    # much better way:
    # this guy take each number that from 1 to 9 one by one and put it into each 3 * 3 sub map.
    # when the dead way encountered, it will return to the last step and try again.
    def __init__(self):
        # this container holds all generated maps
        self.maps = []

    def generate(self, howmany=1):
        cur = len(self.maps)
        while len(self.maps) < cur + howmany:
            init_map = initial_maps()
            # starting number from 1
            number = 1
            while number <= 9:
                ret_num, init_map = self.put_number(number, init_map)
                number = ret_num + 1
            self.maps.append(init_map)

    def put_number(self, num, maps, off=0):
        for idx in range(9):
            row, col = get_neighbour(idx, maps)
            seq = list(range(9))
            while True:
                # if this condition triggered, that means there is no way to finish the maps.
                # it starts to clear current and last number from maps, and go to another try.
                if not seq:
                    maps = self.clear_numbers(num, maps)
                    maps = self.clear_numbers(num - 1, maps)
                    num, maps = self.put_number(num - 1, maps)
                    # if off <= 9:
                    #     num, maps = self.put_number(num, maps, off+1)
                    # else:
                    #     maps = self.clear_numbers(num - 1, maps)
                    #     num, maps = self.put_number(num - 1, maps)
                    return num, maps
                # if off == 0:
                #     pos = self.get_random_pos(seq)
                # else:
                #     pos = self.get_seq_pos(seq, off)
                pos = self.get_random_pos(seq)
                # this is magic way to get a numbers list that should avoid.
                restricts = row.iloc[pos // 3].tolist() + col.iloc[pos % 3].tolist()
                # check what if the number in that avoiding list, and the position is available.
                if num not in restricts and maps[idx//3][idx%3][pos] == 0:
                    maps[idx//3][idx%3][pos] = num
                    break
        return num, maps

    @staticmethod
    def get_random_pos(seq):
        # get a random positon to fill.
        pos = np.random.randint(0, len(seq))
        return seq.pop(pos)
    #
    # @staticmethod
    # def get_seq_pos(seq, off):
    #     seq = seq[off-1:] + seq[:off-1]
    #     return seq.pop(0)

    @staticmethod
    def clear_numbers(num, maps):
        for idx in range(9):
            try:
                pos = maps[idx // 3][idx % 3].index(num)
                maps[idx // 3][idx % 3][pos] = 0
            except ValueError:
                continue
        return maps

    def display(self):
        if self.maps:
            for each in self.maps:
                display_maps(each)


class SudokuA:
    # inefficient way:
    # this guy fill first sub map then depend on the numbers order in first map place remain sub maps one by one.
    # when the dead way encountered, this stupid guy will kick entire maps off and try a new one.
    # some times madly fast depend on lucky.

    def __init__(self):
        self.maps = []

    def generate_sudoku_map(self, howmany=1):
        cur = len(self.maps)
        while len(self.maps) < cur + howmany:
            maps = initial_maps()
            maps[0][0] = self.random_list()
            maps = self.maps_machine_level1(1, maps)
            if maps:
                self.maps.append(maps)

    @staticmethod
    def random_list():
        base = list(range(1, 10))
        ret = []
        while base:
            N = np.random.randint(0, len(base))
            ret.append(base.pop(N))
        return ret

    def maps_machine_level1(self, index, maps):
        rows, cols = get_neighbour(index, maps)
        result = self.maps_machine_level2(rows, cols)
        if result:
            ret = copy.deepcopy(maps)
            ret[index // 3][index % 3] = result
            if index == 8:
                return ret
            else:
                return self.maps_machine_level1(index+1, ret)
        else:
            return False

    def maps_machine_level2(self, row, col):
        ret = [0 for _ in range(9)]
        count = 0
        while 0 in ret:
            count += 1
            ran_list = self.random_list()
            for i in range(9):
                for X in ran_list:
                    restricts = row.iloc[i//3].tolist() + col.iloc[i%3].tolist()
                    if X not in restricts:
                        ret[i] = X
                        ran_list.remove(X)
                        break
            if count >= 20:
                return False
        return ret

    def display(self):
        if self.maps:
            for each in self.maps:
                display_maps(each)


if __name__ == '__main__':
    import time
    n = 5
    start = time.time()
    s = SudokuB()
    s.generate(n)
    s.display()
    time2cost = time.time() - start
    print('{:.2f} sec totally cost.\n {:.2f} sec each cost.'.format(time2cost, time2cost / n))

