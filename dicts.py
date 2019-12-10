""" Dictionary with all of the commands and it's asm code"""
commands = \
    {
        'add': """
        @SP
        A=M-1
        D=M
        A=A-1
        M=M+D
        @SP
        M=M-1""",

        'sub': """
        @SP
        A=M-1
        D=M
        A=A-1
        M=M-D
        @SP
        M=M-1""",

        'neg': """
        @SP
        A=M-1
        M=-M""",

        'eq': """
        @SP
        A=M-1
        D=M
        A=A-1
        D=M-D
        M=0
        @SP
        M=M-1
        @END_EQ_{0}
        D;JNE
        @SP
        A=M-1
        M=-1  
        (END_EQ_{0})""",

        'lt': """
        @SP
        A=M-1
        D=M
        A=A-1
        D=M-D
        M=0
        @SP
        M=M-1
        @END_LT_{0}
        D;JLE
        @SP
        A=M-1
        M=-1
        (END_LT_{0})""",

        'gt': """
        @SP
        A=M-1
        D=M
        A=A-1
        D=M-D
        M=0
        @SP
        M=M-1
        @END_GT_{0}
        D;JLE
        @SP
        A=M-1
        M=-1
        (END_GT_{0})""",


        'and': """
        @SP
        A=M-1
        D=M
        A=A-1
        M=M&D
        @SP
        M=M-1""",

        'or': """
        @SP
        A=M-1
        D=M
        A=A-1
        M=M|D
        @SP
        M=M-1""",

        'not': """
        @SP
        A=M-1
        D=-1
        M=D-M""",

        #  todo : 3rd line, need to correct D=A
        'push': """
        @{0}
        A=M
        D=A
        @{1}
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1""",

        'pushconstant': """
        @{0}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1""",

        'pushtemp': """
        @{0}
        D=A
        @{1}
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1""",

        'pushpointer': """
        @{0}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1""",

        'pop': """
        @{0}
        A=M
        D=A
        @{1}
        A=D+A
        D=A
        @address
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @address
        A=M
        M=D""",

        'pushstatic': """
        @static.{0}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1""",

        'poptemp': """
        @{0}
        D=A
        @{1}
        A=D+A
        D=A
        @address
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @address
        A=M
        M=D""",

        'poppointer': """
        @SP
        M=M-1
        A=M
        D=M
        @{0}
        M=D""",

        'popstatic': """
        @SP
        M=M-1
        A=M
        D=M
        @static.{0}
        M=D""",
        'init': """
        @256
        D=A
        @SP
        M=D
        """

    }

""" Dictionary with all of the segments and it's asm values"""
segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', 'temp': "5"}

flow = {"label": """
        ({0})""",
        "goto": """
        @{0}
        0;JMP
        """,
        "if-goto": """
        @SP
        M=M-1
        A=M
        D=M
        @{0}
        D;JNE
        """}

functions_dics = {'call': """
        //push return value
        @{1}_RET
        D=A
        @SP
        A=M
        M=A-D
        @SP
        M=M+1
        //push LCL
        @LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push ARG
        @ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push THIS
        @THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //push THAT
        @THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        //ARG=SP-n-5
        @5
        D=A
        @{0}
        D=A+D
        @SP
        D=M-D
        @ARG
        M=D
        //LCL = SP
        @SP
        D=M
        @LCL
        M=D
        """,

        'return': """
        @LCL
        D=M
        @frame
        M=D
        @5
        D=D-A
        @temp
        A=D
        D=M
        @ret
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D
        @ARG
        D=M
        @SP
        M=D+1
        @frame
        A=M-1
        D=M
        @THAT
        M=D
        @2
        D=A
        @frame
        A=M-D
        D=M
        @THIS
        M=D
        @3
        D=A
        @frame
        A=M-D
        D=M
        @ARG
        M=D
        @4
        D=A
        @frame
        A=M-D
        D=M
        @LCL
        M=D
        @ret
        A=M
        0;JMP
        """}
