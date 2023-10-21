
import pytest
from parallel_output import ParallelManager, Task
from unittest import mock

def my_function(positional1, keyword1=None):
    print(f'positional {positional1} keyword {keyword1}')
    return positional1

def test_add():
    parallel = ParallelManager()
    parallel.add('label1', my_function, 'some_value')
    assert parallel.tasks[0].__str__() == Task('label1', my_function, ('some_value',), {}).__str__()

    parallel.add('label2', my_function, 'some_value', keyword1='dummy')
    assert parallel.tasks[1].__str__() == Task('label2', my_function, ('some_value',), {'keyword1': 'dummy'}).__str__()


def test_add_duplicate_labels():
    with pytest.raises(ValueError):
        parallel = ParallelManager()
        parallel.add('label1', my_function, 'some_value')
        parallel.add('label1', my_function, 'some_value')


def test_run_return_output():
    parallel = ParallelManager()
    parallel.add('label1', my_function, 'some_value')
    parallel.add('label2', my_function, 'another_value', keyword1='locksmith')
    parallel.run()

    assert parallel.return_values['label1'] == 'some_value'
    assert parallel.return_values['label2'] == 'another_value'
    assert parallel.outputs['label1'] == 'positional some_value keyword None\n'
    assert parallel.outputs['label2'] == 'positional another_value keyword locksmith\n'

    assert parallel.get_labels() == ['label1', 'label2']
    assert parallel.get_return('label1') == 'some_value'
    assert parallel.get_return() == {'label1': 'some_value', 'label2': 'another_value'}
    assert parallel.get_output('label2') == 'positional another_value keyword locksmith\n'
    assert parallel.get_output() == {'label1': 'positional some_value keyword None\n', 'label2': 'positional another_value keyword locksmith\n'}
    
def my_exception_function(positional1, keyword1=None):
    print(f'positional {positional1} keyword {keyword1}')
    raise ValueError('Value Error')
    return positional1

def test_run_exception():
    parallel = ParallelManager()
    parallel.add('label1', my_exception_function, 'some_value')
    parallel.run()

    assert type(parallel.get_return('label1')) == ValueError
    assert parallel.get_output('label1') == 'positional some_value keyword None\nEXCEPTION: Value Error\n'














