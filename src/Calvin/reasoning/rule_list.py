"""
rule_list.py

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

#this module defines all my rules (right at the moment)
#eventually these may get split up, if they're too hard to deal with as one file :P

#need to add a for-all that calls an argument. whee.

from rules import *
from conclusions import Conclusion
from confidence import *
from guards import *
import samples


def __minusFun(x, y):
    if type(x) == str or type(y) == str:
        print x, y
    return x-y

def __plusFun(x, y):
    return x+y

def __mulFun(x, y):
    return x*y

def __divFun(x, y):
    if y == 0:
        return x
    else:
        return float(x) / y

__minusFun.userDisp = {'infix':True, 'text':'-'}
__plusFun.userDisp = {'infix':True, 'text':'+'}
__mulFun.userDisp = {'infix':True, 'text':'*'}
__divFun.userDisp = {'infix':True, 'text':'/'}

"""
Construction of a rule:

conclusion,
[list of rhs items]
rule quality (may be a tuple. if so, it is (quality if true, quality if false)
guard (may be missing),
confidence template (may be missing)

both guards and templates should be referenced by name, to avoid problems 
    (guard=, template=)

Conclusions: conclusion name, [optional list of conclusion parameters]
Guards: information retrieval function (NOT function name), [function parameters],
        comparison value, optional comparison function (NOT function name)
Templates contain: 
        priority - whether the confidences in the RHS are combined AND-style or OR-style
        increment - which direction and how much the match closeness is incremented
        flip - whether the true/falseness of the RHS combination is flipped

rhs items:
Observation: function name (in observations.py), [function parameters]
Calculation: function name (in calculataion.py), [function parameters], variable name for rest of rule
Simulation: function name (in simulations.py), [function parameters], variable name for rest of rule (may be None)
Argument: conclusion name, [optional list of conclusion parameters]

if any function parameter is a tuple, it is interpreted as a function to be run. The first value
should be the function to run (NOT function name), the second value should be a tuple of parameters
to the function.
"""


#top-level conclusions
#no process

makeRule(Conclusion("no process"),  
         [Argument("ages line up")], 
         Validity.accept)

makeRule(Conclusion('no process'),
         [Calculation('calcMean', ['age'], 'mean age'),
          Argument('likely age', ['mean age'])],
         Validity.prob)

makeRule(Conclusion('no process'),
         [Calculation('calcMean', ['age'], 'mean age'),
          Argument('acceptable age', ['mean age'])],
         (Validity.prob, Validity.sound))

makeRule(Conclusion('no process'),
         [Simulation('chiSquaredTest', ['age'])],
         Validity.accept)

#exhumation
makeRule(Conclusion('exhumation'),
         [Argument('eroded cover')],
         (Validity.accept, Validity.prob))

makeRule(Conclusion('exhumation'),
         [Calculation('calcMax', ['age'], 'max age'),
          Argument('too young', ['max age'])],
          Validity.prob)

makeRule(Conclusion('exhumation'),
         [Simulation('longTail', [-1])],
         Validity.prob)
         
makeRule(Conclusion('exhumation'),
         [Argument('frost heaving')],
         (Validity.accept, Validity.plaus), template=Template(increment=-1))
         
makeRule(Conclusion('exhumation'),
         [Argument('vegetation upheaval')],
         (Validity.accept, Validity.plaus))

makeRule(Conclusion('exhumation'),
         [Observation('eqs', [(samples.getLandformField, ('type',)), 'alluvial fan'])],
         Validity.prob, template=Template(flip=True),
         guard=Guard(samples.getLandformField, ['type'], 'alluvial fan'))
            
makeRule(Conclusion('exhumation'),
         [Calculation('calcMax', ['age'], 'max age'),
          Observation('eqs', [(samples.getLandformField, ("type",)), "moraine"]),
          Observation('lte', ['max age', 5000])],
         Validity.plaus, template=Template(priority=True))

makeRule(Conclusion("exhumation"), 
         [Calculation("calcMaxSample", ["age"], "erosion choice"), 
          Argument("representative sample", ["erosion choice"])], 
         Validity.plaus)

makeRule(Conclusion("exhumation"), 
         [Calculation("calcMax", ["age"], "erosion age"), 
          Argument("acceptable age", ["erosion age"])], 
         (Validity.plaus, Validity.accept))

makeRule(Conclusion('exhumation'),
         [Observation('thereExists', ['observed', 'grucification'])],
         Validity.plaus)

makeRule(Conclusion('exhumation'),
         [Observation('majority', ['observed', 'grucification'])],
         (Validity.sound, Validity.plaus))

makeRule(Conclusion('too young', ['sample age']),
         [Observation('lt', ['sample age', (samples.getLandformField, ('estimated age',))]),
          Simulation('highConfidence', ['estimated age'])],
         Validity.prob, template=Template(priority=True))

makeRule(Conclusion('too young', ['sample age']),
         [Observation('lt', ['sample age', (samples.getLandformField, ('known minimum age',))])],
         Validity.accept, template=Template(priority=True))

makeRule(Conclusion('too young', ['sample age']),
         [Observation('lt', ['sample age', (samples.getLandformField, ('stratographic minimum age',))]),
          Simulation('highConfidence', ['stratographic minimum age'])],
         Validity.sound, template=Template(priority=True))

#exhumation (sample)
makeRule(Conclusion("exhumation", ["sample"]), 
         [Observation("observed", [(samples.extractField, ("sample", "in matrix"))])], 
         Validity.prob)

makeRule(Conclusion('exhumation', ['sample']),
         [Argument('cover', ['sample'])],
         Validity.accept)

makeRule(Conclusion('exhumation', ['sample']),
         [Argument('too young', [(samples.extractField, ("sample", "age"))])],
         Validity.plaus)

makeRule(Conclusion('cover', ['sample']),
         [Observation('lt', [(__divFun, 
                              [(samples.extractNuclideField, ('sample', '26Al', 'cosmogenic inventory')),
                               (samples.extractNuclideField, ('sample', '10Be', 'cosmogenic inventory'))]),
                             5.5])],
         Validity.sound,
         guard=Guard(samples.hasNuclides, ['sample', ('26Al', '10Be')], True))

makeRule(Conclusion('cover', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'grucification'))])],
         Validity.sound)

#inheritance
makeRule(Conclusion('inheritance'),
         [Simulation('inheritancePossible', [])],
         (Validity.plaus, Validity.sound))

makeRule(Conclusion("inheritance"), 
         [Calculation("calcMean", ["age uncertainty"], "mean uncertainty"), 
          Argument("all within range", [(__minusFun, ("mean uncertainty", 1000)), 
                                        (__plusFun, ("mean uncertainty", 1000)), "age uncertainty"])], 
         Validity.plaus, template=Template(increment=-1, flip=True))

makeRule(Conclusion('inheritance'),
         [Argument('cold based ice')],
         (Validity.sound, Validity.prob), template=Template(increment=-1),
         guard=Guard(samples.isGlacial, [], True))

makeRule(Conclusion("inheritance"), 
         [Calculation("calcMinSample", ["age"], "inheritance choice"), 
          Argument("representative sample", ["inheritance choice"])], 
         Validity.plaus)

makeRule(Conclusion("inheritance"), 
         [Calculation("calcMin", ["age"], "inheritance age"), 
          Argument("acceptable age", ["inheritance age"])], 
         Validity.plaus)

makeRule(Conclusion("inheritance"), 
         [Simulation("quantizedInheritance", [])], 
         (Validity.sound, Validity.prob))

makeRule(Conclusion('inheritance'),
         [Simulation('longTail', [+1])],
         Validity.sound)

makeRule(Conclusion("inheritance"),
         [Observation("eqs", [(samples.getLandformField, ("type",)), "moraine"])],
         Validity.plaus, 
         guard=Guard(samples.getLandformField, ["type"], "moraine"))

makeRule(Conclusion("inheritance"),
         [Observation("eqs", [(samples.getLandformField, ("type",)), "lava flow"])],
         Validity.sound,
         guard=Guard(samples.getLandformField, ["type"], "lava flow"),
         template=Template(flip=True))

makeRule(Conclusion('inheritance'),
         [Observation('observed', [(samples.isFluvial,)])],
         (Validity.prob, Validity.plaus))

#inheritance (sample)
makeRule(Conclusion('inheritance', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'bedrock'))])],
         (Validity.prob, Validity.plaus))

makeRule(Conclusion('inheritance', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', "glacial polish"))])],
         Validity.plaus)

makeRule(Conclusion('inheritance', ['sample']),
         [Argument('inheritance')],
         Validity.prob, template=Template(increment=-1))

makeRule(Conclusion('inheritance', ['sample']),
         [Calculation('calcMean', ['age'], 'mean age'),
          Observation('gt', [(samples.extractField, ('sample', 'age')), 'mean age'])],
         (Validity.prob, Validity.sound), template=Template(increment=-1))

makeRule(Conclusion('inheritance', ['sample']),
         [Observation('eq', [(samples.extractField, ('sample', 'nuclide'), '14C')])],
         Validity.sound, template=Template(flip=True),
         guard=Guard(samples.extractField, ['sample', 'nuclide'], '14C'))

#vegetation cover
makeRule(Conclusion("vegetation cover"), 
         [Simulation("correlated", ["elevation", "age", +1])], 
         Validity.sound, 
         guard=Guard(findRange, ["elevation"], 100, lambda x, y: x > y))

makeRule(Conclusion('vegetation cover'),
         [Calculation('calcMean', ['latitude'], 'latitude'),
          Calculation('calcMean', ['longitude'], 'longitude'),
          Observation('lt', ['latitude', 41]),
          Observation('gt', ['latitude', 35]),
          Observation('lt', ['longitude', -110]),
          Observation('gt', ['longitude', -124])],
         (Validity.prob, Validity.sound), template=Template(priority=True))

makeRule(Conclusion('vegetation cover'),
         [Argument('vegetation')],
         (Validity.plaus, Validity.sound))

#snow cover
makeRule(Conclusion('snow cover'),
         [Argument('cover')],
         (Validity.sound, Validity.prob), template=Template(increment=-1))

#rule added for eval
makeRule(Conclusion('snow cover'),
         [Observation('observed', [(samples.getLandformField, ['subject to prevailing winds'])])],
         (Validity.sound, Validity.plaus), template=Template(flip=True))

makeRule(Conclusion("snow cover"), 
         [Simulation("correlated", ["elevation", "age", -1])], 
         Validity.sound, 
         guard=Guard(findRange, ["elevation"], 500, lambda x, y: x > y))

makeRule(Conclusion("snow cover"), 
         [Argument('is cold')], 
         (Validity.plaus, Validity.sound))

makeRule(Conclusion("snow cover"), 
         [Argument('is very cold')], 
         Validity.prob)

#outlier (sample)
makeRule(Conclusion('outlier', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'acute geometry'))])],
         Validity.plaus)


makeRule(Conclusion('outlier', ['sample']),
         [Argument('acceptable age', [(samples.extractField, ('sample', 'age'))])],
         (Validity.prob, Validity.sound), template=Template(flip=True))

makeRule(Conclusion('outlier', ['sample']),
         [Observation('gt', [(samples.extractField, ('sample', 'boulder size')), 3])],
         Validity.plaus, template=Template(flip=True))

makeRule(Conclusion('outlier', ['sample']),
         [Observation('lt', [(samples.extractField, ('sample', 'boulder size')), 0.5])],
         Validity.plaus)

makeRule(Conclusion('outlier', ['sample']),
         [Calculation('calcDensity', [], 'my density'),
          Simulation('skewsField', ['sample', 'sample density'])],
          Validity.prob)

makeRule(Conclusion('outlier', ['sample']),
         [Simulation('centralAgreement', ['sample'])],
         (Validity.sound, Validity.plaus))

makeRule(Conclusion('outlier', ['sample']),
         [Simulation('skewsField', ['sample', 'boulder size'])],
         Validity.plaus)

makeRule(Conclusion("outlier", ["sample"]), 
         [Simulation("argueWithoutSample", ["sample", "no process"])], 
         (Validity.sound, Validity.plaus))

#?? should remove?
makeRule(Conclusion("outlier", ["sample"]), 
         [Simulation("skewsField", ["sample", "age uncertainty"])], 
         Validity.plaus, template=Template(increment=-1))

makeRule(Conclusion('outlier', ['sample']), 
         [Simulation('distantFromOthers', ['sample', 'age', 'age uncertainty'])],
         Validity.accept)

makeRule(Conclusion('outlier', ['sample']),
         [Argument('no process')],
         (Validity.accept, Validity.plaus), template=Template(increment=+1, flip=True))

makeRule(Conclusion('outlier', ['sample']),
         [Argument('explained variation', ['sample'])],
         Validity.prob, template=Template(increment=+1))



#ages line up
makeRule(Conclusion("ages line up"), 
         [Simulation("checkOverlap", ['age', 'age uncertainty'])], 
         Validity.accept, template=Template(increment=1))

makeRule(Conclusion('ages line up'),
         [Observation('lt', [(samples.numSamples,), 5]),],
         (Validity.prob, Validity.plaus), template=Template(flip=True))

makeRule(Conclusion("all within range", ["bottom", "top", "field"]), 
         [Observation("forAll", ["gt", "field", "bottom"]), 
          Observation("forAll", ["lt", "field", "top"])], 
         Validity.accept, template=Template(priority=True))


#erosion
makeRule(Conclusion('erosion'),
         [Argument('little weathering')],
         Validity.prob, template=Template(flip=True))

makeRule(Conclusion('erosion'),
         [Calculation('calcMax', ['age'], 'max age'),
          Argument('has matrix'),
          Observation('gte', ['max age', 15000])],
         (Validity.prob, Validity.plaus), template=Template(priority=True))

makeRule(Conclusion('erosion'),
         [Calculation('calcMax', ['age'], 'max age'),
          Observation('gte', ['max age', 40000])],
         (Validity.prob, Validity.plaus))

#eroded cover
makeRule(Conclusion("eroded cover"),  
         [Calculation('calcMax', ['age uncertainty'], 'max uncertainty'),
          Simulation("isLinearGrowth", ["age", 'max uncertainty'])], 
         Validity.sound)

makeRule(Conclusion('eroded cover'),
         [Argument('erosion')],
         Validity.sound)

makeRule(Conclusion('eroded cover'),  
         [Argument('visual matrix erosion')], 
         Validity.prob)

makeRule(Conclusion('eroded cover'),
         [Argument('cover')],
         (Validity.sound, Validity.prob))

#need a rule here that checks the likely erosion rate against boulder heights
#and max age and tells us if they might have been covered ever.


#clast erosion
makeRule(Conclusion('clast erosion', ['sample']),
         [Argument('erosion')],
         Validity.sound)

makeRule(Conclusion('clast erosion', ['sample']),
         [Observation('gt', [(samples.extractField, ('sample', 'production rate spallation')), 35]),
          Observation('lt', [(samples.extractField, ('sample', 'production rate spallation')), 75])],
         (Validity.sound, Validity.plaus), template=Template(flip=True, priority=True),
         guard=Guard(samples.extractField, ['sample', 'nuclide'], '36Cl'))

makeRule(Conclusion("clast erosion", ['sample']), 
         [Observation("gt", [(samples.extractField, ('sample', 'age')), 30000])], 
         (Validity.plaus, Validity.prob))

makeRule(Conclusion('clast erosion', ['sample']),
         [Argument('visual clast erosion', ['sample'])],
         Validity.sound)

makeRule(Conclusion('visual clast erosion', ['sample']),
         [Argument('original texture', ['sample'])],
         Validity.prob, template=Template(flip=True))

makeRule(Conclusion('original texture', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', "glacial polish"))])],
         Validity.sound, guard=Guard(samples.isGlacial, [], True))

makeRule(Conclusion('original texture', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', "fluvial smoothing"))])],
         Validity.sound, guard=Guard(samples.isFluvial, [], True))

makeRule(Conclusion('original texture', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', "diagnostic textures"))])],
         Validity.sound, guard=Guard(samples.getLandformField, ["type"], "lava flow"))

#visual clast erosion
makeRule(Conclusion('visual clast erosion', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'spalling debris'))])],
         Validity.sound)

makeRule(Conclusion('visual clast erosion', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'weathering rind'))])],
         Validity.sound)

makeRule(Conclusion("visual clast erosion", ['sample']), 
         [Observation("observed", [(samples.extractField, ('sample', "pitted"))])], 
         Validity.accept)

#cover
makeRule(Conclusion("cover"), 
         [Simulation("correlated", ["age", "boulder size", +1])],
         Validity.sound)

makeRule(Conclusion('cover'),
         [Calculation('calcMin', ['boulder size'], 'smallest boulder'),
          Observation('lt', ['smallest boulder', 2])],
         Validity.prob)
         

#matrix
makeRule(Conclusion("has matrix"), 
         [Observation("observed", [(samples.getLandformField, ("clast supported",))])],
         Validity.sound, template=Template(flip=True))

makeRule(Conclusion("has matrix"), 
         [Observation("eqs", [(samples.getLandformField, ('type',)), 'moraine']),
          Observation("eqs", [(samples.getLandformField, ('type',)), 'alluvial fan'])],
         Validity.prob)      

makeRule(Conclusion("visual matrix erosion"),
         [Observation("observed", [(samples.getLandformField, ("flat crested",))])], 
         Validity.sound, 
         guard=Guard(samples.getLandformField, ["type"], "moraine"))

#superglacial debris
makeRule(Conclusion('superglacial debris'),
         [Observation('lt', [(samples.getLandformField, ('glacier length',)), 1])],
         Validity.prob, guard=Guard(samples.isGlacial, [], True))

makeRule(Conclusion('superglacial debris'),
         [Observation('lt', [(samples.getLandformField, ('glacier length',)), 20])],
         Validity.plaus, guard=Guard(samples.isGlacial, [], True))

#frost and cold
makeRule(Conclusion('frost heaving'),
         [Argument('is cold')],
         Validity.prob)

makeRule(Conclusion('frost heaving'),
         [Argument('is very cold')],
         Validity.prob, template=Template(flip=True))

makeRule(Conclusion('frost shattering', ['sample']),
         [Argument('is cold')],
         Validity.plaus)

makeRule(Conclusion('cold based ice'),
         [Argument('is very cold')],
         Validity.sound)

makeRule(Conclusion('is cold'),
         [Calculation("calcMean", ["latitude"], "latitude"), 
          Calculation("calcMax", ["elevation"], "elevation"), 
          Argument("is cold", ["latitude", "elevation"])],
          Validity.accept)

makeRule(Conclusion("is cold", ["latitude", "elevation"]), 
         [Observation("gt", ["elevation", 1000]), 
          Observation("gt", ["latitude", 15]),
          Observation("lt", ["latitude", -15])], 
         Validity.sound)

makeRule(Conclusion('is very cold'),
         [Calculation("calcMean", ["latitude"], "latitude"), 
          Argument("is very cold", ["latitude"])], 
         Validity.accept)

makeRule(Conclusion('is very cold', ['latitude']),
         [Observation('gt', ['latitude', 65]),
          Observation('lt', ['latitude', -65])],
         Validity.sound)

#vegetation
makeRule(Conclusion('vegetation upheaval'),
         [Argument('vegetation')],
         (Validity.plaus, Validity.sound))

makeRule(Conclusion('vegetation'),
         [Argument('is very cold')],
         Validity.sound, template=Template(flip=True))


#different origin
#TEST
makeRule(Conclusion('different origin', ['sample']),
         [Argument('superglacial debris')],
         Validity.plaus)

makeRule(Conclusion("different origin", ["sample"]), 
         [Observation("observed", [(samples.extractField, ("sample", "in matrix"))])], 
         Validity.prob, 
         template=Template(flip=True))

makeRule(Conclusion("different origin", ["sample"]), 
         [Observation("observed", [(samples.extractField, ("sample", "bedrock"))])], 
         (Validity.accept, Validity.plaus), template=Template(flip=True))

makeRule(Conclusion("different origin", ["sample"]), 
         [Simulation("differentChemistry", ["sample"])], 
         Validity.prob,
         #single source landform -> single chemical composition
         guard=Guard(samples.getLandformField, ['type'], 'lava flow'))

makeRule(Conclusion('different origin', ['sample']),
         [Observation('lt', [(samples.extractField, ('sample', 'distance to rock wall')), 100])],
         Validity.plaus)

#explained variation
makeRule(Conclusion('explained variation', ['sample']),
         [Calculation('calcMean', ['age'], 'mean age'),
          Argument('explained variation', ['sample', 'mean age']),
          Argument('complex history', ['sample']),
          Argument("different origin", ["sample"])],
          Validity.accept)

makeRule(Conclusion('explained variation', ['sample', 'mean age']),
         [Argument('clast erosion', ['sample']),
          Argument('new exposure', ['sample'])],
         (Validity.sound, Validity.prob),
         guard=Guard(samples.extractField, ['sample', 'age'], 'mean age', lambda x,y: x < y))

makeRule(Conclusion('explained variation', ['sample', 'mean age']),
         [Argument('inheritance', ['sample'])],
         (Validity.sound, Validity.prob),
         guard=Guard(samples.extractField, ['sample', 'age'], 'mean age', lambda x,y: x > y))

makeRule(Conclusion('new exposure', ['sample']),
         [Argument('frost shattering', ['sample']),
          Argument('exhumation', ['sample']),
          Argument('turned', ['sample'])],
         (Validity.accept, Validity.plaus))

#misc sample stuff
makeRule(Conclusion('turned', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'in matrix'))])],
         (Validity.sound, Validity.plaus), template=Template(flip=True))

makeRule(Conclusion('turned', ['sample']),
         [Observation('observed', [(samples.extractField, ('sample', 'bedrock'))])],
         (Validity.sound, Validity.plaus), template=Template(flip=True))

makeRule(Conclusion('complex history', ['sample']),
         [Argument('cover', ['sample'])],
         (Validity.sound, Validity.plaus))




#representative sample
makeRule(Conclusion("representative sample", ["sample"]),
         [Simulation("skewsField", ["sample", "age"])], 
         Validity.sound, template=Template(increment=-1, flip=True))

makeRule(Conclusion('representative sample', ['sample']),
         [Argument('outlier', ['sample'])],
         Validity.sound, template=Template(flip=True))

makeRule(Conclusion('representative sample', ['sample']),
         [Argument('likely age', [(samples.extractField, ['sample', 'age'])])],
         Validity.prob)


#acceptable age
makeRule(Conclusion("acceptable age", ["sample age"]),
         [Argument('inside boundaries', ['sample age', 'known minimum age', 'known maximum age'])],
         Validity.accept)

makeRule(Conclusion('acceptable age', ['sample age']),
         [Argument('inside boundaries', ['sample age', 'stratographic minimum age',
                                         'stratographic maximum age'])],
         Validity.sound)

makeRule(Conclusion("acceptable age", ["sample age"]),
         [Argument('same as known', ['sample age'])],
         Validity.accept)

makeRule(Conclusion('inside boundaries', ['sample age', 'minimum', 'maximum']),
         [Argument('fits minimum', ['sample age', 'minimum']), 
          Argument('fits maximum', ['sample age', 'maximum'])],
         Validity.accept, template=Template(priority=True))

makeRule(Conclusion("inside boundaries", ["sample age", 'minimum', 'maximum']),
         [Argument('fits minimum', ['sample age', 'minimum'])],
         Validity.accept, 
         guard=Guard(samples.getLandformField, ['maximum'], True, exists, invert=True))

makeRule(Conclusion("inside boundaries", ["sample age", 'minimum', 'maximum']),
         [Argument('fits maximum', ['sample age', 'maximum'])],
         Validity.accept, 
         guard=Guard(samples.getLandformField, ['minimum'], True, exists, invert=True))

makeRule(Conclusion('fits minimum', ['sample age', 'minimum age']),
         [Observation('gt', ['sample age', (samples.getLandformField, ('minimum age',))]),
          Argument('invalid data', ['minimum age'])],
          Validity.accept)

makeRule(Conclusion('fits maximum', ['sample age', 'maximum age']),
         [Observation('lt', ['sample age', (samples.getLandformField, ('maximum age',))]),
          Argument('invalid data', ['maximum age'])],
          Validity.accept)

makeRule(Conclusion('same as known', ['sample age']),
         [Observation('neareq', ['sample age', (samples.getLandformField, ('known age',))]),
          Argument('invalid data', ['known age'])],
          Validity.accept)

#likely age
makeRule(Conclusion('likely age', ['sample age']),
         [Observation('sameMagnitude', ['sample age', (samples.getLandformField, ('estimated age',))]),
          Simulation('highConfidence', ['estimated age'])],
         Validity.sound, template=Template(priority=True))

makeRule(Conclusion('likely age', ['sample age']),
         [Observation('lt', [60000, 'sample age']),
          Observation('lt', ['sample age', 100000])],
         Validity.sound, template=Template(priority=True),
         guard=Guard(samples.getLandformField, ['type'], 'alluvial fan'))

makeRule(Conclusion('likely age', ['sample age']),
         [Observation('lt', ['sample age', 120000])],
         Validity.plaus,
         guard=Guard(samples.getLandformField, ['type'], 'moraine'))


#misc
makeRule(Conclusion('little weathering'),
         [Observation('observed', [(samples.getLandformField, ("arid",))])],
         Validity.prob)

makeRule(Conclusion('invalid data', ['field']),
         [Simulation('highConfidence', ['field'])],
         Validity.prob, template=Template(flip=True))


