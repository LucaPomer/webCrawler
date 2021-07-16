import csv


def write_multiple_lines(lines_array, file_name):
    with open(file_name, 'a') as fd:
        writer = csv.writer(fd)
        writer.writerows(lines_array)


def write_data(entry_array, file_name):
    with open(file_name, 'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(entry_array)
