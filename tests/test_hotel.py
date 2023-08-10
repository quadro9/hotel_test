import subprocess
import os

def run_test(input_str):
    cmd = os.environ['COMMAND_RUN']
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    output, error = process.communicate(input=input_str)
    process.kill()
    return output


def test_case1():
    # Тест 1. Один отель, несколько клиентов:
    input_str = """\
9
BOOK 1000 hotel1 1 2
BOOK 1500 hotel1 2 3
BOOK 2000 hotel1 1 1
CLIENTS hotel1
ROOMS hotel1
CLIENTS hotel1
BOOK 3000 hotel1 3 2
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
2
6
2
3
8
"""
    assert run_test(input_str) == expected_output


def test_case2():
    # Тест 2. Несколько отелей с разными бронированиями:
    input_str = """\
10
BOOK 1000 hotel1 1 1
BOOK 1100 hotel1 2 1
BOOK 1200 hotel2 3 2
BOOK 1300 hotel2 2 1
CLIENTS hotel1
ROOMS hotel1
CLIENTS hotel2
ROOMS hotel2
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
2
2
2
3
2
2
"""
    assert run_test(input_str) == expected_output


def test_case3():
    # Тест 3. Бронирование в разные дни:
    input_str = """\
8
BOOK 1000000 hotel1 1 1
BOOK 1100000 hotel1 2 1
BOOK 1200000 hotel1 3 1
CLIENTS hotel1
ROOMS hotel1
BOOK 1300000 hotel1 1 1
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
1
1
1
1
"""
    assert run_test(input_str) == expected_output


def test_case4():
    # Тест 4. Сгорает первый заказ:
    input_str = """\
8
BOOK 1000000 hotel1 1 1
BOOK 1080000 hotel1 1 1
BOOK 1085000 hotel1 1 1
CLIENTS hotel1
ROOMS hotel1
BOOK 1086400 hotel1 2 1
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
1
3
2
3
"""
    assert run_test(input_str) == expected_output


def test_case5():
    # Тест 5. За секундку до сгорания:
    input_str = """\
8
BOOK 1000000 hotel1 1 1
BOOK 1080000 hotel1 1 1
BOOK 1085000 hotel1 1 1
CLIENTS hotel1
ROOMS hotel1
BOOK 1086399 hotel1 2 1
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
1
3
2
4
"""
    assert run_test(input_str) == expected_output


def test_case6():
    # Тест 6. Большие числа:
    input_str = """\
8
BOOK 9000000000000000000 hotel1 1 1
BOOK 9000000000000080000 hotel1 1 1
BOOK 9000000000000085000 hotel1 1 1
CLIENTS hotel1
ROOMS hotel1
BOOK 9000000000000086400 hotel1 2 1
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
1
3
2
3
"""
    assert run_test(input_str) == expected_output


def test_case7():
    # Тест 7. Пустой отель:
    input_str = """\
10
BOOK 1001000 hotel1 1 1
BOOK 1002000 hotel1 2 1
BOOK 1003000 hotel1 3 1
CLIENTS hotel1
ROOMS hotel1
BOOK 1100000 hotel2 1 1
CLIENTS hotel1
ROOMS hotel1
CLIENTS hotel2
ROOMS hotel2
"""
    expected_output = """\
3
3
0
0
1
1
"""
    assert run_test(input_str) == expected_output


def test_case8():
    # Тест 8. Отель который не бронировали вернет 0:
    input_str = """\
10
CLIENTS hotel1
ROOMS hotel1
BOOK 1001000 hotel1 1 1
BOOK 1002000 hotel1 2 1
BOOK 1003000 hotel1 3 1
CLIENTS hotel1
ROOMS hotel1
"""
    expected_output = """\
0
0
3
3
"""
    assert run_test(input_str) == expected_output


def test_case9():
    # Тест 9. Каждый день разный отель:
    input_str = """\
18
BOOK 1000000 hotel1 1 1
BOOK 1100000 hotel2 2 1
BOOK 1200000 hotel3 3 1
CLIENTS hotel1
ROOMS hotel1
CLIENTS hotel2
ROOMS hotel2
CLIENTS hotel3
ROOMS hotel3
BOOK 1300000 hotel4 1 1
CLIENTS hotel1
ROOMS hotel1
CLIENTS hotel2
ROOMS hotel2
CLIENTS hotel3
ROOMS hotel3
CLIENTS hotel4
ROOMS hotel4
"""
    expected_output = """\
0
0
0
0
1
1
0
0
0
0
0
0
1
1
"""
    assert run_test(input_str) == expected_output


def test_case10():
    # Тест 10. Тест от заказчика:
    input_str = """\
11
CLIENTS Marriott
ROOMS Marriott
BOOK 10 FourSeasons 1 2
BOOK 10 Marriott 1 1
BOOK 86409 FourSeasons 2 1
CLIENTS FourSeasons
ROOMS FourSeasons
CLIENTS Marriott
BOOK 86410 Marriott 2 10
ROOMS FourSeasons
ROOMS Marriott
"""
    expected_output = """\
0
0
2
3
1
1
10
"""
    assert run_test(input_str) == expected_output