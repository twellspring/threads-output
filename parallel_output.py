#!/usr/bin/env python3
# Class to facilitate running functions in parallel but keep the output separate

import io
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
import stdio_proxy


class Task:
    """Task definition for use by Parallel"""

    def __init__(self, label, function, args, kwargs):
        self.label = label
        self.function = function
        self.args = args
        self.kwargs = kwargs


class ParallelManager:
    """Run multiple functions in parallel and capture output"""

    def __init__(self):
        self.tasks = []
        self.labels = []
        self.return_values = {}
        self.outputs = {}

    def add(self, label, function, *args, **kwargs):
        """Add a Task"""
        if label in self.labels:
            sys.exit(f'label {label} is not unique')
        else:
            self.tasks.append(Task(label, function, args, kwargs))
            self.labels.append(label)

    def run(self, type='thread'):
        """Run all Tasks in parallel using ThreadPoolExecutor or ProcessPoolExecutor

        Returns:
            dict: containing 'return' and 'output' keys for each task label
        """
        count = len(self.tasks)
        executors = {}

        e = ThreadPoolExecutor(
            count) if type == 'thread' else ProcessPoolExecutor(count)
        with e as executor:
            for task in self.tasks:
                print(f'Staring {task.label}')
                executors[task.label] = executor.submit(
                    self.output_wrapper, task)
        wait(list(executors.values()))
        print('All Tasks Completed')

        for label, exec in executors.items():
            self.outputs[label] = exec.result()['output']
            self.return_values[label] = exec.result()['return']

    def output_wrapper(self, task):
        """Calls a function and captures its output

        Returns:
            dict: containing 'return' and 'output' keys
        """
        buf = io.BytesIO()
        with stdio_proxy.redirect_stdout(buf):
            results = task.function(*task.args, **task.kwargs)
        print(f'Completed {task.label}')
        return {'return': results, 'output': buf.getvalue().decode()}

    def get_return(self, label=None):
        """Get the return value for a task or all return values if label is not passed"""
        return self.return_values[label] if label else self.return_values

    def get_output(self, label):
        """Get the output for a task or all outputs if label is not passed"""
        return self.outputs[label] if label else self.outputs

    def get_labels(self):
        """Get a list of labels"""
        return self.labels

    def print_output(self):
        """Print the output of all tasks"""
        for label, output in self.outputs.items():
            print(f'\n*****{label}*****\n')
            print(output)
