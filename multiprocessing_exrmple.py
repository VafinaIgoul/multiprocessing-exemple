# coding: utf-8
from multiprocessing import Process
from multiprocessing import Queue

from multiprocessing import current_process
from multiprocessing import cpu_count


def worker(input):
    """Обработчик рабочик процессов из очереди."""
    for func, args in iter(input.get, 'STOP'):
       calculate(func, args)


def calculate(func, args):
    """Функция вызывающая функцию с аргументами.
    Функция получает другую функцию и
    аргументы для нее.
    """
    result = func(*args)
    print u'{0} результат работы {1}{2} = {3}'.format(
        current_process().name, func.__name__, args, result)


def mul(a, b):
    return a * b


def plus(a, b):
    return a + b


def test_queue():
    u"""Связь процессов через очередь"""
    NUMBER_OF_PROCESSES = cpu_count()
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # Создаем очереди
    task_queue = Queue()

    # Добавляем задачи в очередь
    for task in TASKS1:
        task_queue.put(task)

    # Запуск рабочих процессов
    for i in range(NUMBER_OF_PROCESSES):
        p = Process(target=worker, args=(task_queue,))
        p.start()

    for task in TASKS2:
        task_queue.put(task)

    # Сигнал об окончании работы
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    task_queue.close()


if __name__ == '__main__':
    test_queue()
