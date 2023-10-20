#!/usr/bin/env python3

from time import sleep
from parallel_output import ParallelManager


def cpu_function(seconds=20):
    d = {}
    i = 0
    for i in range(0, 50000000):
        d[i] = 'A' * 1024
        if i % 10000 == 0:
            print(i)


def my_function(sleep_time, header):
    print(f'OUTPUT {header}')
    print(f'OUTPUT2 {header}')
    sleep(sleep_time)
    #raise ValueError('A very specific bad thing happened.')
    #x = 1 + 'x'
    print(f'OUTPUT3 {header}')
    return f'RETURN {header}'


def main():
    # tmanager = ParallelManager()
    # tmanager.add('task1', cpu_function, 10)
    # tmanager.add('task2', cpu_function, 10)
    # results = tmanager.run(type="thread")
    # task1_return = tmanager.get_return('task1')
    # tmanager.print_output()

    tmanager = ParallelManager()
    tmanager.add('task1', my_function, 7, header="thing 1")
    tmanager.add('task2', my_function, 5, "thing 2")
    tmanager.add('task3', my_function, 3, "thing 3")
    results = tmanager.run(exec_type="thread")
    # tmanager.print_output()

    # task1_return = tmanager.get_return('task1')
    # print(type(task1_return))


if __name__ == "__main__":
    main()