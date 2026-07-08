from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

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
    get_file_content_truncate = get_file_content('calculator', 'lorem.txt')
    print(get_file_content_truncate)

    get_file_content_result = get_file_content('calculator', 'main.py')
    print(get_file_content_result)

main()