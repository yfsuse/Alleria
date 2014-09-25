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
                    int_data = int(data)
                except ValueError as e:
                    int_data = data
                inner_data.append(int_data)
        else:
            try:
                int_dataset = int(dataset)
            except ValueError as e:
                int_dataset = dataset
            inner_data.append(int_dataset)
        int_seq.append(inner_data)
    return int_seq

if __name__ == '__main__':
    seq_a = [-12335284.477, -109006.006, -280.974, -0.201, -0.002, -0.001, 0.0, 0.0, 0.0, 0.0, 19.998, 39.994]
    seq_b = [-12335284.978, -109006.002, -280.974, -0.201, -0.002, -0.001, 0.0, 0.0, 0.0, 0.0, 19.998, 39.994]
    if conv_data(seq_a, "low") == conv_data(seq_b, "low"):
        print "success"