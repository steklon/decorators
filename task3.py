import datetime
import types


def logger(path):
    def __logger(old_function):

        def new_function(*args, **kwargs):

            result = old_function(*args, **kwargs)
            watch = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            name = old_function.__name__

            message = f"время: {watch}, имя: {name}, аргументы: {args, kwargs}, результат: {result}\n"

            with open(path, "a", encoding="utf-8") as file:
                file.write(message)
            return result

        return new_function
    return __logger


@logger(path='main.log')
def flat_generator(list_of_list):

    for element_ in list_of_list:
        if isinstance(element_, list):
            yield from flat_generator(element_)
        else:
            yield element_


def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_4()
