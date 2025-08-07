from functions.get_files_info import *

def run_tests():
    # print('--- Test 1 ---')
    # print(get_file_content("calculator", "lorem.txt"))
    # print()

    print('--- Test 1 ---')
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print('--- Test 2 ---')
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print('--- Test 3 ---')
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print()


if __name__ == "__main__":
    run_tests()
