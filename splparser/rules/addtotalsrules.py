#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.addtotalslexer import tokens

start = 'cmdexpr'

def p_cmdexpr_addtotals(p):
    """cmdexpr : addtotalscmd"""
    p[0] = p[1]

def p_cmdexpr_addtotals_single(p):
    """addtotalscmd : ADDTOTALS"""
    p[0] = ParseTreeNode('ADDTOTALS')

def p_cmdexpr_addtotals_field(p):
    """addtotalscmd : ADDTOTALS wc_stringlist fieldlist"""
    p[0] = ParseTreeNode('ADDTOTALS')
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_addtotalscmd_addtotals(p):
    """addtotalscmd : ADDTOTALS wc_stringlist
                    | ADDTOTALS fieldlist"""
    p[0] = ParseTreeNode('ADDTOTALS')
    p[0].add_children(p[2].children)

def p_addtotals_opt(p):
    """wc_string : ADDTOTALS_OPT EQ value"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper())
    p[0].add_children([p[1],p[3]])

def p_addtotals_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_addtotals_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in addtotals parser input!")
