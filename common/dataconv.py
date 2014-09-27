#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'




def conv_data(seq, check_level = "low"):
    if check_level == "high":
        return seq
    int_seq = []
    for dataset in seq:
        inner_data = []
        if isinstance(dataset, list):
            for data in dataset:
                try:
                    int_data = int(round(data, -1))
                except ValueError as e:
                    int_data = data
                inner_data.append(int_data)
        else:
            try:
                int_dataset = int(round(dataset, -1))
            except ValueError as e:
                int_dataset = dataset
            inner_data.append(int_dataset)
        int_seq.append(inner_data)
    return int_seq


def sub_list(seq):
    if len(seq) != 2:
        return None
    return abs(seq[0] - seq[1])

def sub_seq(seq_a, seq_b):
    if len(seq_a) != len(seq_b):
        return False
    difference = 0
    for enum in zip(seq_a, seq_b):
        difference += sub_list(enum)
    print difference
    if difference > 2:
        return False
    return True


if __name__ == '__main__':
    seq_a = [-12335285.477, -109006.006, -280.974, -0.201, -0.002, -0.001, 0.0, 0.0, 0.0, 0.0, 19.998, 39.994]
    seq_b = [-12335284.978, -109006.002, -280.974, -0.201, -0.002, -0.001, 0.0, 0.0, 0.0, 0.0, 19.998, 39.994]
    print sub_seq(seq_a, seq_b)

    # print seq_a - seq_b
    # if conv_data(seq_a, "low") == conv_data(seq_b, "low"):
    #     print "success"