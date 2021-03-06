# -*- coding: utf-8 -*-

"""
***************************************************************************
    Help2Html.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
import re

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import pickle
from processing.tools.system import *
import os
import codecs

ALG_DESC = 'ALG_DESC'
ALG_CREATOR = 'ALG_CREATOR'
ALG_HELP_CREATOR = 'ALG_HELP_CREATOR'

exps = [(r"\*(.*?)\*", r"<i>\1</i>"),
        ("``(.*?)``", r'<FONT FACE="courier">\1</FONT>'),
        ("(.*?)\n==+\n+?", r'<h2>\1</h2>'),
        ("(.*?)\n--+\n+?", r'<h3>\1</h3>'),
        (r"::(\s*\n(\s*\n)*((\s+).*?\n)(((\4).*?\n)|(\s*\n))*)",r"<pre>\1</pre>"),
        ("\n+", "</p><p>")]


def getHtmlFromRstFile(rst):
    with open(rst) as f:
        lines = f.readlines()
    s = "".join(lines)
    for exp, replace in exps:
        p = re.compile(exp)
        s = p.sub(replace, s)
    print s
    return s

def getHtmlFromHelpFile(alg, helpFile):
    if not os.path.exists(helpFile):
        return None
    alg = alg
    f = open(helpFile, 'rb')
    descriptions = pickle.load(f)
    s = '<html><body><h2>Algorithm description</h2>\n'
    s += '<p>' + getDescription(ALG_DESC, descriptions) + '</p>\n'
    s += '<h2>Input parameters</h2>\n'
    for param in alg.parameters:
        s += '<h3>' + param.description + '</h3>\n'
        s += '<p>' + getDescription(param.name, descriptions) + '</p>\n'
    s += '<h2>Outputs</h2>\n'
    for out in alg.outputs:
        s += '<h3>' + out.description + '</h3>\n'
        s += '<p>' + getDescription(out.name, descriptions) + '</p>\n'
    s += '<br>'
    s += '<p align="right">Algorithm author: ' + getDescription(ALG_CREATOR, descriptions) + '</p>'
    s += '<p align="right">Help author: ' + getDescription(ALG_HELP_CREATOR, descriptions) + '</p>'
    s += '</body></html>'
    return s

def getDescription(name, descriptions):
    if name in descriptions:
        return descriptions[name].replace("\n", "<br>")
    else:
        return ''
