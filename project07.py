#################################################imports#############################################################
import sys
import os
import re
import dicts as d

################################################consts################################################################
"""A constant that represent the valid number of arguments"""
NUM_OF_ARG = 2

"""The Sys commend call"""
SYS_COMMEND = "call Sys.init 0"

"""the initiation cammand"""
INIT = 'init'

"""A constant that represent the name of the Sys file"""
SYS = "Sys.vm"

"""The number to push when defending function"""
PUSH_0 = "0"

"""the commend to push constant number"""
PUSH_CONSTANT = "pushconstant"

"""The end of return label"""
RET = "_RET"

"""The end of asm file"""
ASM_END = ".asm"

"""The end of vm file"""
VM_END = ".vm"

"""A constant that represent the return commend"""
RETURN = 'return'

"""A constant that represent the defind function commend"""
FANCTION = 'function'

"""A constant that represent the call function commend"""
CALL = 'call'

"""A constant that represent the if-goto commend"""
IF_GOTO = "if-goto"

"""A constant that represent the goto commend"""
GOTO = "goto"

"""A constant that represent the add label commend"""
LABEL = "label"

"""A constant that represent the index of the commend in the commend line"""
COMMAND = 0

"""The string to split the commend string by"""
SPLIT_CMD = " "

"""Dot to add"""
DOT = "."

"""the end line string"""
END_LINE = "\n"

"""A constant that represent the JGE commend"""
JGE = "JGE"

"""A constant that represent the JLE commend"""
JLE = "JLE"

"""A constant that represent the compare commend"""
COMPARE = 'compare'

"""False value"""
FALSE = "0"

"""True value"""
TRUE = "-1"

"""space value"""
SPACE = "_"

"""A constant that represent the commend that check if the number are with the same sign"""
MAKE_SAME_SIGN = 'make_same_sign'

"""A constant that represent the lt commend"""
LT = "lt"

"""A constant that represent the gt commend"""
GT = "gt"

"""A constant that represent empty string"""
EMPTY_STR = ""

"""A constant that represent the neg commend"""
NEG = 'neg'

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
    if command[CMD] == PUSH or command[CMD] == POP:
        if command[SEG] == CONSTANT:
            if command[CMD] == POP:  #  not supporting constant pop
                return
            if int(command[DATA]) < 0:
                return d.commands[command[CMD]+command[SEG]].format(command[DATA][1:]) + "\n" + d.commands[NEG]
            return d.commands[command[CMD] + command[SEG]].format(command[DATA])
        elif command[SEG] == POINTER:
            if command[DATA] == THIS_ZERO:
                return d.commands[command[CMD]+command[SEG]].format(d.segments[THIS])
            return d.commands[command[CMD]+command[SEG]].format(d.segments[THAT])
        elif command[SEG] == TEMP:
            return d.commands[command[CMD] + command[SEG]].format(d.segments[command[SEG]], command[DATA])
        elif command[SEG] == STATIC:
            if class_name is not EMPTY_STR:
                return d.commands[command[CMD] + command[SEG]].format(class_name + command[DATA])
            else :
                return d.commands[command[CMD] + command[SEG]].format(command[DATA])
        return d.commands[command[CMD]].format(d.segments[command[SEG]], command[DATA])
    elif command[0] == GT:
        return d.commands[MAKE_SAME_SIGN].format(GT, class_name + SPACE + str(counter), TRUE, FALSE) + \
               d.commands[COMPARE].format(class_name + SPACE + str(counter), JLE)
    elif command[0] == LT:
        return d.commands[MAKE_SAME_SIGN].format(LT, class_name + SPACE + str(counter), FALSE, TRUE) + \
               d.commands[COMPARE].format(class_name + SPACE + str(counter), JGE)
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
    line = line.replace(END_LINE, EMPTY_STR)
    line = line.rstrip()
    return line


def check_name(name, class_name):
    """
    A function that check if the name contain the class name or not
    :param name: the name to check
    :param class_name: the class name
    :return: the name with the class  name
    """
    check = name.split(DOT)
    if len(check) == 1:
        return class_name + DOT + name
    return name


def parse_cmd(line, counter, class_name):
    """
    A function that parse the given line according to the command
    :param line: the line to parse
    :param class_name: the name of the calss of the function
    :return: the asm command as string
    """
    cmd = line.split(SPLIT_CMD)
    comm = cmd[COMMAND]
    if comm == LABEL or comm == GOTO or comm == IF_GOTO:
        name = check_name(EMPTY_STR.join(cmd[1:]), class_name)
        return d.flow[cmd[COMMAND]].format(name)
    elif comm == CALL:
        return call_func(cmd, counter, class_name)
    elif comm == FANCTION:
        return define_func(cmd, class_name)
    elif comm == RETURN:
        return return_val()
    else:
        return parse_line(cmd, counter, class_name)


def single_file(original_file):
    """
    processing single file
    :param original_file: the file
    """
    parse_file = open_target_file(original_file)
    class_name = os.path.splitext(os.path.basename(original_file))[0]
    f = reading_original_file(original_file)
    parse_file = convert_lines_to_asm(f, parse_file, class_name)
    parse_file.close()


def convert_lines_to_asm(f, parse_file, class_name):
    """
    A function that take file and convert it to asm file
    :param f: the file to convert
    :param parse_file: the asm file
    :param class_name: the name of the class
    :return: the parse file as asm file
    """
    counter = 0
    for l in f:
        if l is None:
            continue
        p_line = parse_cmd(l, counter, class_name)
        counter += 1
        if p_line is not None:
            parse_file.write(p_line)
    return parse_file


def reading_original_file(original_file):
    """
    A function that read the original file
    :param original_file: the file to read
    :return: the open file
    """
    file = open(original_file, 'r')
    line = file.readline()
    f = []
    while line:
        l = remove_invalid_syntax(line)
        if l != EMPTY_STR:
            f.append(l)
        line = file.readline()
    file.close()
    return f


def open_target_file(original_file):
    """
    A function that open the target file
    :param original_file: the file to read from
    :return: target file
    """
    dir = os.path.dirname(original_file)
    name = os.path.basename(original_file)
    name = name.replace(VM_END, ASM_END)
    if dir is EMPTY_STR:
        parse_file = open(name, 'w')
    else:
        parse_file = open(dir + os.path.sep + name, 'w')
    return parse_file


def call_func(cmd, counter, class_name):
    """
    A function that return the asm code of call to function
    :param cmd: the commend line
    :param class_name: the name of the class of the function
    :return: the asm commend as string
    """
    label = check_name(cmd[SEG], class_name) + str(counter)
    order = d.functions_dics[CALL].format(cmd[DATA], label)
    order += d.flow[GOTO].format(check_name(cmd[SEG], class_name))
    order += d.flow[LABEL].format(label + RET)
    return order


def return_val():
    """
    A function that returns the return asm commend
    :return: the asm commend as string
    """
    return d.functions_dics[RETURN]


def define_func(cmd, class_name):
    """
    A function that returns the definition of function as asm commend
    :param cmd: the commend to translate
    :param class_name: the name of the class of the function
    :return: the asm commend as string
    """
    k = int(cmd[DATA])
    func = d.flow[LABEL].format(check_name(cmd[SEG], class_name)) + END_LINE
    for i in range(k):
        func += d.commands[PUSH_CONSTANT].format(PUSH_0) + END_LINE
    return func


def is_sys(file_list):
    """
    A function taht check if there is Sys file in dirlist
    :param file_list: the dirlist
    :return: boolean value
    """
    for file in os.listdir(file_list):
        if file == SYS:
            return True
    return False


def create_sys_file(path):
    """
    A function that create the asm file if there Sys file
    :param path: the path of the file
    :return: the parse file
    """
    name = os.path.basename(path)
    parse_file = open_target_file(name + os.sep + name +ASM_END)
    parse_file.write(d.commands[INIT])
    cmd = SYS_COMMEND.split(SPLIT_CMD)
    parse_file.write(call_func(cmd, EMPTY_STR, "Sys"))
    for file in os.listdir(path):
        if file.endswith(VM_END):
            f = reading_original_file(path+os.sep+file)
            class_name = os.path.splitext(os.path.basename(file))[0]
            parse_file = convert_lines_to_asm(f, parse_file, class_name)
    parse_file.close()


def main():
    """
    the main function. translating the vm code to ams code
    """
    if len(sys.argv) != NUM_OF_ARG:
        print('Usage: ', sys.argv[0], '<input file or directory>')
    path = sys.argv[1]
    if os.path.isdir(path):
        if is_sys(path):
            create_sys_file(path)
        else:
            for file in os.listdir(path):
                if file.endswith(VM_END):
                    single_file(path + os.path.sep + file)
    else:
        single_file(path)


if __name__ == '__main__':
    main()
