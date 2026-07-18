from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    # get_files_info tests:
    # root_contents = get_files_info('calculator')
    # print(root_contents)
    #
    # pkg_contents = get_files_info('calculator', 'pkg')
    # print(pkg_contents)
    #
    # bin_contents = get_files_info('calculator', '/bin')
    # print(bin_contents)
    #
    # dots_contents = get_files_info('calculator', '../')
    # print(dots_contents)


    # get_file_content tests:
    # working_dir = 'calculator'
    #
    # print(get_file_content(working_dir, 'main.py'))
    # print(get_file_content(working_dir, 'pkg/calculator.py'))
    # print(get_file_content(working_dir, '/bin/cat'))

    # write_file tests:
    # print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    # print(write_file("calculator", "pkg2/temp.txt", "this should be allowed"))

    # run_python_file tests:
    # print(run_python_file("calculator", "main.py"))
    # print(run_python_file("calculator", "main.py", ["3 + 6"]))
    # print(run_python_file("calculator", "tests.py"))
    # print(run_python_file("calculator", "../main.py"))
    # print(run_python_file("calculator", "nonexistent.py"))
    print(run_python_file("calculator", "lorem.txt"))





main()