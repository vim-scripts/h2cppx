#!/usr/bin/env python

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir)
sys.path.append(cur_dir+'/src')
sys.path.append(cur_dir+'/src/external')
sys.path.append(cur_dir+'/template')

import argparse
from Parser import *
from CodeGeneration import *
from StringIO import StringIO

version_description = \
"""
%(prog)s 1.0
"""

description = \
"""
    Parse C++ header file and generate c++ implement code. 
"""

usage= \
"""
    h2cppx header_file [-t templatefile] [-o outputfile] [-ln line_number] [-a] [-f] [[-auto] [-p] [--search-path] [--output-path]] [-v] 
    h2cppx -h to see the help.
"""

example = \
"""
example:
    h2cppx sample/sample.h
    h2cppx sample/sample.h -a -o sample.cpp -ln 21
    h2cppx sample/sample.h -f -o sample.cpp -t template/template2
    h2cppx sample/sample.h -auto 
    h2cppx sample/sample.h -auto -p cxx --search-path=src,src2 --output-path=src
"""

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage = usage,
        description=description,
        epilog = example,
        prog = 'h2cppx'
        )

parser.add_argument("header_file", help = "Specific the c++ header file")

parser.add_argument(
        "-t", 
        "--template",
        type = str,
        required = False,
        action  = "store",
        default = cur_dir+"/template/template1",
        help = "Spcific the template config file"
        )

parser.add_argument(
        "-o",
        "--output",
        type = str,
        required = False,
        action = "store",
        help = "Specific the cpp output file name, default is stdout"
        )
parser.add_argument(
        "-ln",
        "--line_number",
        type = int,
        required = False,
        action = "store",
        help = "Specific the line number what generate cpp code"
        )
#mutually exclusive optional
group = parser.add_mutually_exclusive_group()
group.add_argument(
        "-a",
        "--append",
        required = False,
        action = "store_true",
        default = False,
        help = "If the cpp file already exist, append to the end of the file."
        )
group.add_argument(
        "-f",
        "--force",
        required = False,
        action = "store_true",
        default = False,
        help = "If the cpp file already exist,will force overwrite the cpp file!!!"
        )
group.add_argument(
        "-auto",
        "--auto-handle",
        required = False,
        action = "store_true",
        default = False,
        help = "Auto Contrast header and implementation files, find function declarations in the header file and append the newly added to the implementation file, if the file does not exist to achieve a new file is created!"
        )
parser.add_argument(
        "-p",
        "--postfix",
        required = False,
        action = "store",
        default = "cpp",
        help = "Set to generate the implementation file extension(.c,.cc,.cxx,.cpp,...),the default value is .cpp(for -auto only)"
        )
parser.add_argument(
        "--search-path",
        required = False,
        action = "store",
        help = "Setting implement search directory list, the default is the directory where the header file(for -auto only)"
        )
parser.add_argument(
        "--output-path",
        required = False,
        action = "store",
        help = "Setting the implement file output directory,if the file search fails, it will generate a file in this directory.the default is the directory where the header file(for -auto only)"
        )
parser.add_argument(
        "-v",
        "--version",
        action = "version",
        version= version_description
        )

def get_search_list(s):
    if not s: return []
    if ':' in s:
        sep = ':'
    else:
        sep = ','
    return [ os.path.abspath(p) for p in s.split(sep) ]

def findpath(filename, search_list):
    ''' search file in search path list '''
    for _dir in search_list:
        path = _dir + os.sep + filename
        if os.path.exists(path):
            return path
    return None

def auto_handle(args):
    header_dir  = os.path.dirname(os.path.abspath(args.header_file))

    search_list = get_search_list(args.search_path)
    search_list.append(header_dir) #append the header files directory in the last of list

    buf = StringIO()
    header = Header(os.path.abspath(args.header_file))
    cppfilename = args.header_file[:args.header_file.rfind('.')] + '.' + args.postfix.lstrip('.')
    cppfilename = os.path.basename(cppfilename)

    out = None
    path = findpath(cppfilename, search_list)
    #maybe cppfile already exists in output_path
    if not path and args.output_path:
        tmp = os.path.abspath(args.output_path) + os.sep + cppfilename
        if os.path.exists(tmp):
            path = tmp

    if path:
        out = open(path, 'a')
        cppfile = Header(path)
        diff_node = different_node(header, cppfile)
        # generate implement code
        visitor= ImplementGenerationVisitor(buf)
        for node in diff_node:
            node.accept(visitor)
    else:
        if args.output_path:
            path = os.path.abspath(args.output_path) + os.sep + cppfilename
        else:
            path = header_dir + os.sep + cppfilename
        if not os.path.exists(os.path.dirname(path)):
            print >>sys.stderr,"The directory '"+os.path.dirname(path)+"' not exist!!!"
            sys.exit(2)
        # generate implement code
        out = open(path, 'w')
        visitor= ImplementGenerationVisitor(buf)
        header.accept(visitor)

    #output
    if buf.len:
        out.write(buf.getvalue().lstrip(os.linesep).rstrip(os.linesep))
    else:
        print >>sys.stderr, 'Nothing generation'
        sys.exit(1)
    out.write(2*os.linesep)

    print >>sys.stdout,"write file", path, "successful!"

    buf.close()
    out.close()
    sys.exit(0)


def do_action(args):
    Config.init(args.template)

    if not os.path.exists(args.header_file):
        print >>sys.stderr,'The header file not exist!!!'
        sys.exit(2)

    if args.auto_handle:
        auto_handle(args)

    buf = StringIO()
    node = Header(os.path.abspath(args.header_file))
    if not node.functions and not node.classes:
        print >>sys.stderr, 'Nothing generation,is this a header file?'
        sys.exit(1)

    if args.line_number:
        node = node.getNodeInLine(args.line_number)
        if not node:
            print >>sys.stderr,'Specific the line number have not declare was found'
            sys.exit(3)

    # generate implement code
    visitor= ImplementGenerationVisitor(buf)
    node.accept(visitor)

    out = None
    if not args.output:
        out = sys.stdout
    elif not os.path.exists(args.output):
        out = open(args.output,'w')
    elif args.append:
        out = open(args.output, 'a')
    elif args.force:
        out = open(args.output, 'w')
    else:
       print >>sys.stderr,'The output file already exist, please use "-a" arg to append to the end of the file  or "-f" to force overwrite.'
       sys.exit(4)

    #output
    if buf.len:
        out.write(buf.getvalue().lstrip(os.linesep).rstrip(os.linesep))
    else:
        print >>sys.stderr, 'Nothing generation'
        sys.exit(1)
    out.write(2*os.linesep)

    if out != sys.stdout:
        print >>sys.stdout,"write file", args.output, "successful!"

    buf.close()
    if type(out) == file:
        out.close()

if __name__=='__main__':
    args = parser.parse_args()
    try:
        do_action(args)
    except IOError,msg:
        print >>sys.stderr,"IOError: ", msg
        sys.exit(5)

