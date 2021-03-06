"""
VirtualSample.py

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

class VirtualSample(object):

    def __init__(self, sample, nuclide, experiment):
        self.sample     = sample
        self.nuclide    = nuclide
        self.experiment = experiment

    def __contains__(self, key):
        keys = self.sample.properties_for_experiment(self.nuclide, self.experiment)
        return key in keys

    def __len__(self):
        keys = self.sample.properties_for_experiment(self.nuclide, self.experiment)
        return len(keys)

    def __iter__(self):
        keys = self.sample.properties_for_experiment(self.nuclide, self.experiment)
        return iter(sorted(keys))

    def __getitem__(self, key):
        if key == "experiment":
            return self.experiment
        self.sample.set_nuclide(self.nuclide)
        self.sample.set_experiment(self.experiment)
        return self.sample[key]

    def __setitem__(self, key, item):
        self.sample.set_nuclide(self.nuclide)
        self.sample.set_experiment(self.experiment)
        self.sample[key] = item

    def __delitem__(self, key):
        self.sample.set_nuclide(self.nuclide)
        self.sample.set_experiment(self.experiment)
        del self.sample[key]
        
    def keys(self):
        return self.sample.properties_for_experiment(self.nuclide, self.experiment)
        
    def remove_experiment(self):
        if self.experiment != "input":
            self.sample.remove_experiment(self.nuclide, self.experiment)
