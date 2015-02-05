#!/usr/bin/env python

'''
    Parse c++ header file and generate c++ implement code
'''

import os
import sys
import yaml

sys.path.append('external')

import visitor
from Parser import *
from Cheetah.Template import Template

class Config(object):

    # template key-value 
    template = {}
    # keyword 
    #keyword = [ 'TYPE', 'FULLNAME']

    @staticmethod
    def init(filename):
        data = file(filename).read()
        inside = False
        raw_content = ''
        #replace \n to \\n in " "
        for c in data:
            if c=='"':
                inside = not inside
            if inside and c=='\n':
                raw_content += '\\n'
            else:
                raw_content += c
        content = yaml.load(raw_content)
        for k in content:
            v = content[k]
            if type(v) == type(''): 
                k = k.lstrip('\n ').rstrip('\n ')
                v = v.lstrip('\n ').rstrip('\n ')
            Config.template[k] = v
            #dynamic create class attribute
            setattr(Config, k, v)


class ImplementGenerationVisitor(object):

    def __init__(self, stream=sys.stdout):
        '''
            stream parame specify code output stream,
            you can set it as stdxxx, StringIO or any file object
        '''
        self._stream = stream

    @property
    def stream(self):
        return self._stream

    @visitor.on('node')
    def visit(self, node):
        """
        This is the generic method that initializes the
        dynamic dispatcher.
        """
        pass

    @visitor.on('node')
    def startNode(self, node):
        pass

    @visitor.on('node')
    def endNode(self, node):
        pass

    @visitor.when(Node)
    def visit(self, node):
        """
        Will run for nodes that do specifically match the
        provided type.
        """
        print 'Unrecognized node', node

    @visitor.when(Variable)
    def visit(self, node):
        """ Matches nodes of type variable. """
        if (not node['static']) or (not node['owner']):
            return None
        doxy_comment = ''
        if Config.DOXYGEN: doxy_comment = node['doxygen'] + os.linesep
        var_def = str(Template(Config.VARIABLE, searchList=[{
            'variable': node,
            }]))
        self._stream.write( doxy_comment + var_def)

    @visitor.when(Function)
    def visit(self, node):
        """ Matches nodes that contain function. """ 
        if not self.funcNeedDefine(node): 
            return None

        doxy_comment = ''
        if Config.DOXYGEN: doxy_comment = node['doxygen'] + os.linesep

        fun_def = str(Template(Config.FUNCTION, searchList=[{
            'function': node
            }]))
        if node['const']:
            fun_def = fun_def.replace(')', ') const')
        self._stream.write( doxy_comment + fun_def) 

    @visitor.when(Class)
    def visit(self, node):
        """ Matches nodes that contain class. """
        for attr in node.attributes:
            attr.accept(self)
        for method in node.methods:
            method.accept(self)

    @visitor.when(Header)
    def visit(self, node):
        """ Matches nodes that contain header. """
        for function in node.functions:
            function.accept(self)
        for cls in node.classes:
            cls.accept(self)

    @visitor.when(Variable)
    def startNode(self, node):
        if node['static'] and node['owner']:
            var_start = ''
            if Config.VARIABLE_START: 
                var_start = str(Template(Config.VARIABLE_START, searchList=[{
                    'variable': node
                    }]))
                self._stream.write(var_start+os.linesep)

    @visitor.when(Variable)
    def endNode(self, node):
        if node['static'] and node['owner']:
            var_end = ''
            if Config.VARIABLE_END: 
                var_end = str(Template(Config.VARIABLE_END, searchList=[{
                    'variable': node
                    }]))
                self._stream.write(os.linesep+var_end)
            self._stream.write(Config.VARIABLE_INTERVAL * os.linesep)

    @visitor.when(Function)
    def startNode(self, node):
        if not self.funcNeedDefine(node): 
            return None

        func_start = ''
        if Config.FUNCTION_START: 
            func_start = str(Template(Config.FUNCTION_START, searchList=[{
                'function': node
                }]))
            self._stream.write(func_start+os.linesep)

    @visitor.when(Function)
    def endNode(self, node):
        if not self.funcNeedDefine(node): 
            return None

        func_end = ''
        if Config.FUNCTION_END: 
            func_end = str(Template(Config.FUNCTION_END, searchList=[{
                'function': node
                }]))
            self._stream.write(os.linesep + func_end)
        self._stream.write( Config.FUNCTION_INTERVAL * os.linesep)

    @visitor.when(Class)
    def startNode(self, node):
        class_start = ''
        if Config.CLASS_START: 
            class_start = str(Template(Config.CLASS_START, searchList=[{
                'class': node
                }]))
            self._stream.write(class_start+2*os.linesep)

    @visitor.when(Class)
    def endNode(self, node):
        class_end = ''
        if Config.CLASS_END:
            class_end = str(Template(Config.CLASS_END, searchList=[{
                'class': node
                }]))
            self._stream.write(class_end+2*os.linesep)

    @visitor.when(Header)
    def startNode(self, node):
        head_start = ''
        if Config.HEADER_START:
            head_start = str(Template(Config.HEADER_START, searchList=[{
                'header': node
                }]))
            self._stream.write(head_start)
            #self._stream.write('\n\n#include "' + \
            #    os.path.basename(node['header_file']) + '"\n\n')
        self._stream.write(2*os.linesep)

    @visitor.when(Header)
    def endNode(self, node):
        head_end = ''
        if Config.HEADER_END:
            head_end = str(Template(Config.HEADER_END, searchList=[{
                'header': node
                }]))
            self._stream.write(head_end+os.linesep)

    def funcNeedDefine(self, node):
        if node['defined'] or node['inline'] or node['extern'] or \
           node['pure_virtual'] or node['friend']:
            return False
        # fix : Misconception that the macro as a constructor
        if node['constructor'] and node['name'] != node['owner']:
            return False
        return True

# for test
if __name__=='__main__':
    Config.init('../template/template1')
    head=Header('../sample/sample.h')
    print 'Generate all head file implement: '
    head.accept(ImplementGenerationVisitor())
    print 'Generate special line_number %d implement: \n' % 15
    head.getNodeInLine(15).accept(ImplementGenerationVisitor())

