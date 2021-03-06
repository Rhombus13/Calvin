"""
Attributes.py

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

import os.path

class Attributes(object):

    BOOLEAN = "boolean"
    STRING  = "string"
    FLOAT   = "float"
    INTEGER = "integer"

    TYPES  = [STRING, FLOAT, INTEGER, BOOLEAN]

    def __init__(self):
        self.atts = {}

    def __len__(self):
        return len(self.atts)

    def __contains__(self, key):
        return key in self.atts

    def __iter__(self):
        return iter(sorted(self.atts.keys()))

    def add(self, att, att_type=STRING, output_att=False):
        assert att_type in self.TYPES
        self.atts[att] = (att_type,output_att)

    def clear(self):
        self.atts.clear()

    def get_att_type(self, att):
        assert att in self.atts.keys()
        return self.atts[att][0]

    def is_output_att(self, att):
        assert att in self.atts.keys()
        return self.atts[att][1]

    def names(self):
        return sorted(self.atts.keys())
        
    def output_atts(self):
        results = []
        for att in self.atts.keys():
            if self.is_output_att(att):
                results.append(att)
        return results
        
    def remove(self, att):
        assert att in self.atts.keys()
        del self.atts[att]

    def save(self, path):
        atts_path = os.path.join(path, 'atts.txt')
        f = open(atts_path, "w")
        f.write(repr(self.atts))
        f.write(os.linesep)
        f.flush()
        f.close()
    
    def load(self, path):
        atts_path = os.path.join(path, 'atts.txt')
        f = open(atts_path, "U")

        lines = f.readlines()

        f.close()

        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line != '']

        self.atts = eval(lines[0])
