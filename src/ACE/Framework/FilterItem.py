"""
FilterItem.py

* Copyright (c) 2006-2009, University of Colorado.
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the University of Colorado nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF COLORADO ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF COLORADO BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import Operations

class FilterItem(object):

    def __init__(self, key, op, value):
        self.key = key
        self.op = op
        self.value = value

    def apply(self, s):
        try:
            return self.op(s[self.key], self.value)
        except:
            return False

    def save(self, f):
        f.write('BEGIN ITEM')
        f.write(os.linesep)
        f.write(self.key)
        f.write(os.linesep)
        f.write(Operations.nameForOp(self.op))
        f.write(os.linesep)
        f.write(repr(self.value))
        f.write(os.linesep)
        f.write('END ITEM')
        f.write(os.linesep)
        
    def copy(self):
        return FilterItem(eval(repr(self.key)), self.op, eval(repr(self.value)))
        
    def description(self):
        value = None
        if type(self.value) == int:
            value = "%d" % self.value
        elif type(self.value) == float:
            value = "%.2f" % self.value
        else:
            value = "%s" % self.value
        return self.key + " " + Operations.nameForOp(self.op) + " " + value

    def depends_on(self, filter_name):
        return False