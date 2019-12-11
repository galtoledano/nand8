#################################################imports#############################################################
import sys
import os
import re
import dicts as d

################################################consts################################################################
""" data location at the command list"""
DATA = 2

""" segment location at the command list"""
SEG = 1

""" the command location at the command list"""
CMD = 0

"""static segment"""
STATIC = "static"

"""temp segment"""
TEMP = "temp"

"""that segment"""
THAT = 'that'

"""this segment"""
THIS = 'this'

"""this 0 position"""
THIS_ZERO = "0"

"""pointer segment"""
POINTER = "pointer"

"""constant segment"""
CONSTANT = "constant"

"""pop command"""
POP = "pop"

"""push command"""
PUSH = "push"

"""the regex of comments"""
COMMENT = '(.*)(\/\/.*)'

##############################################functions##############################################################


def parse_line(command, counter, class_name):
    """
    parsing single line to asm code
    :param l: the line
    :param counter: current line number
    :return: the command at asm code
    """
    # command = l.split(" ")
    if command[CMD] == PUSH or command[CMD] == POP:
        if command[SEG] == CONSTANT:
            if command[CMD] == POP:  #  not supporting constant pop
                return
            return d.commands[command[CMD]+command[SEG]].format(command[DATA])
        elif command[SEG] == POINTER:
            if command[DATA] == THIS_ZERO:
                return d.commands[command[CMD]+command[SEG]].format(d.segments[THIS])
            return d.commands[command[CMD]+command[SEG]].format(d.segments[THAT])
        elif command[SEG] == TEMP:
            return d.commands[command[CMD] + command[SEG]].format(d.segments[command[SEG]], command[DATA])
        elif command[SEG] == STATIC:
            if class_name is not "":
                #  remove the class name
                return
            return d.commands[command[CMD] + command[SEG]].format(command[SEG] + command[DATA])
        return d.commands[command[CMD]].format(d.segments[command[SEG]], command[DATA])
    elif command[0] == "gt":
        return d.commands['make_same_sign'].format("gt", counter, "-1", "0") + d.commands['compare'].format(counter, "JLE")
    elif command[0] == "lt":
        return d.commands['make_same_sign'].format("lt", counter, "0", "-1") + d.commands['compare'].format(counter,
                                                                                                            "JGE")
    return d.commands[command[CMD]].format(counter)


def remove_invalid_syntax(line):
    """
    A function that remove invalid letter from the line (comments, line break
    etc)
    :param line: the line to check
    :return: the line without the irrelevant letter
    """
    com = re.compile(COMMENT)
    result = com.match(line)
    if result is not None:
        line = result.group(1)
    line = line.replace("\n", "")
    return line


def parse_cmd(line, counter, class_name):
    cmd = line.split(" ")
    comm = cmd[0]
    if comm == "label" or comm == "goto" or comm == "if-goto":
        return d.flow[cmd[0]].format("".join(cmd[1:])), class_name
    elif comm == 'call':
        return call_func(cmd, counter), class_name
    elif comm == 'function':
        return define_func(cmd), class_name
    elif comm == 'return':
        return return_val(cmd, class_name)
    else:
        return parse_line(cmd, counter, class_name), class_name


def single_file(original_file):
    """
    processing single file
    :param original_file: the file
    :param path: the file's folder
    :param single: flag that marks if the file came from folder or its a single file
    """
    parse_file = open_target_file(original_file)
    f = reading_original_file(original_file)
    parse_file = convert_lines_to_asm(f, parse_file)
    parse_file.close()


def convert_lines_to_asm(f, parse_file):
    counter = 0
    for l in f:
        if l is None:
            continue
        class_name = ""
        p_line, class_name = parse_cmd(l, counter, class_name)
        counter += 1
        if p_line is not None:
            parse_file.write(p_line)
    return parse_file


def reading_original_file(original_file):
    file = open(original_file, 'r')
    line = file.readline()
    f = []
    while line:
        l = remove_invalid_syntax(line)
        if l != '':
            f.append(l)
        line = file.readline()
    file.close()
    return f


def open_target_file(original_file):
    dir = os.path.dirname(original_file)
    name = os.path.basename(original_file)
    name = name.replace(".vm", ".asm")
    if dir is "":
        parse_file = open(name, 'w')
    else:
        parse_file = open(dir + os.path.sep + name, 'w')
    return parse_file


def call_func(cmd, counter):
    label = cmd[1] + str(counter)
    order = d.functions_dics['call'].format(cmd[2], label)
    order += d.flow['goto'].format(cmd[1])
    order += d.flow['label'].format(label + "_RET")
    return order


def return_val(cmd, class_name):
    # poped = d.commands['pop'].format('ARG', 0)
    index = cmd[1].find(".")
    if index != -1:
        class_name = cmd[1][:index]
    return d.functions_dics['return'], class_name



def define_func(cmd):
    k = int(cmd[2])
    func = d.flow["label"].format(cmd[1]) + "\n"
    for i in range(k):
        func += d.commands["pushconstant"].format("0") + "\n"
    return func


def is_sys(file_list):
    for file in os.listdir(file_list):
        if file == "Sys.vm":
            return True
    return False


def create_sys_file(path):
    name = os.path.basename(path)
    parse_file = open_target_file(name + os.sep + name + ".asm")
    parse_file.write(d.commands['init'])
    cmd = "call Sys.init 0".split(" ")
    parse_file.write(call_func(cmd, ""))
    for file in os.listdir(path):
        if file.endswith(".vm"):
            f = reading_original_file(path+os.sep+file)
            parse_file = convert_lines_to_asm(f, parse_file)
    parse_file.close()


def main():
    """
    the main function. translating the vm code to ams code
    """
    if len(sys.argv) != 2:
        print('Usage: ', sys.argv[0], '<input file or directory>')
    path = sys.argv[1]
    if os.path.isdir(path):
        if is_sys(path):
            create_sys_file(path)
        else:
            for file in os.listdir(path):
                if file.endswith(".vm"):
                    single_file(path + os.path.sep + file)
    else:
        single_file(path)


if __name__ == '__main__':
    main()

#todo handale with full path