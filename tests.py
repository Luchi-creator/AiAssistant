from functions.get_files_info import *

def run_tests():
    # print('--- Test 1 ---')
    # print(get_file_content("calculator", "lorem.txt"))
    # print()

    print('--- Test 1 ---')
    print(run_python_file("calculator", "main.py"))
    print()

    print('--- Test 2 ---')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print('--- Test 3 ---')
    print(run_python_file("calculator", "tests.py"))
    print()
    
    print('--- Test 4 ---')
    print(run_python_file("calculator", "../main.py"))
    print()

    print('--- Test 5 ---')
    print(run_python_file("calculator", "nonexistent.py"))
    print()


if __name__ == "__main__":
    run_tests()
