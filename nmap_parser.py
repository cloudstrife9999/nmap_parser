#!/usr/bin/python3

from argparse import ArgumentParser


def parse():
    src_file, additional_files_list, dst_file = __parse_args()

    with open(src_file, "r") as source:
        lines = source.readlines()

    for additional in __parse_additional_files(additional_files_list):
        with open(additional, "r") as source:
            for line in source.readlines():
                lines.append(line)

    clean_lines = __polish(lines)
    final_lines = __refine(clean_lines)

    with open(dst_file, "w") as dest:
        for line in final_lines:
            dest.write(line.replace("\n", "") + "\n")


def __parse_args():
    parser = ArgumentParser(description="Nmap output parser")
    parser.add_argument('-s', '--src', required=True, metavar='<source-file-path>', type=str, action='store',
                        help='Nmap output source file')
    parser.add_argument('-a', '--additional', required=False, metavar='<additional-comma-separated-source-files-paths>',
                        type=str, action='store', help='Additional comma separated Nmap output source files')
    parser.add_argument('-d', '--dst', required=True, metavar='<destination-file-path>', type=str, action='store',
                        help='Parsed output file')

    args = parser.parse_args()

    return args.src, args.additional, args.dst


def __parse_additional_files(additional_files_list):
    if additional_files_list is None:
        return []
    else:
        files = additional_files_list.split(",")

        return __remove_initial_and_final_spaces(files)


def __remove_initial_and_final_spaces(files):
    polished_list = []

    for f in files:
        while f.startswith(" ") and len(f) > 1:
            f = f[1:]

        while f.endswith(" ") and len(f) > 1:
            f = f[:-1]

        if not f.startswith(" ") and not f.endswith(" "):
            polished_list.append(f)

    return polished_list


def __refine(clean_lines):
    previous = ""
    final_lines = []

    for line in clean_lines:
        if "Nmap scan report" in previous and "Nmap scan report" not in line:
            final_lines.append("\n")
            final_lines.append(previous)
            final_lines.append(line)
        elif previous != "" and "Nmap scan report" not in line:
            final_lines.append(line)

        previous = line

    return final_lines[1:]


def __polish(lines):
    clean_lines = []

    for line in lines:
        if __allowed(line):
            clean_lines.append(line.replace("\n", "") + "\n")

    return clean_lines


def __allowed(line):
    if "Starting Nmap" in line:
        return False
    elif "Initiating Parallel" in line:
        return False
    elif "Completing Parallel" in line:
        return False
    elif "Completed Parallel" in line:
        return False
    elif "Initiating Connect" in line:
        return False
    elif "Scanning 64 hosts" in line:
        return False
    elif "Connect Scan Timing" in line:
        return False
    elif "Completed Connect" in line:
        return False
    elif "Increasing send delay" in line:
        return False
    elif "giving up on port" in line:
        return False
    elif "Host is up" in line:
        return False
    elif "Read data files" in line:
        return False
    elif "Not shown" in line:
        return False
    elif "SERVICE" in line:
        return False
    elif "All 1000" in line:
        return False
    elif "Discovered open" in line:
        return False
    elif "Nmap done" in line:
        return False
    elif line.startswith("\n"):
        return False
    elif " closed " in line:
        return False
    elif " filtered " in line:
        return False
    else:
        return True


if __name__ == "__main__":
    print("Begin parsing...")
    parse()
    print("Done.")
