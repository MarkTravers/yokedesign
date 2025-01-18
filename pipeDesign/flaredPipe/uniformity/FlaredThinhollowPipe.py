#!python
reset
import sys
import string

from array import *

Length = 8 * 25.4
r_out = 21.0 / 2.0
r_in = 18.0 / 2.0

r_end = 24.0 / 2.0
Lend = 1.*25.4
Lbevel = 0.125 * 25.4
Lcent = Length - 2.0 * (Lend + Lbevel)
LFcoil = 39 / 2.0


circum = 2 * 3.14 * r_out

surfsize = r_out
LengSize = Length / 41.0

cubit.cmd('reset')

cubit.cmd('create cylinder height %f radius %f' %(Lcent,r_out))
cubit.cmd('create cylinder height %f radius %f' %(Lend,r_end))
cubit.cmd('move vol 2 z %f ' %((Lcent+Lend)*0.5 + Lbevel))
cubit.cmd('create cylinder height %f radius %f' %(Lend,r_end))
cubit.cmd('move vol 3 z %f ' %(-(Lcent+Lend)*0.5 - Lbevel))
cubit.cmd('create cylinder height %f radius %f' %(Lcent*2,r_in))

cubit.cmd('subtract volume 4 from volume 1 2 3 imprint') 
cubit.cmd('webcut volume all with plane xplane offset 0 noimprint nomerge')
cubit.cmd('create volume loft surface 51 24')
cubit.cmd('create volume loft surface 54 33')
cubit.cmd('create volume loft surface 30 45')
cubit.cmd('create volume loft surface 27 36')

cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(LengSize/2))
cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(-LengSize/2))
cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(LFcoil))
cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(-LFcoil))
cubit.cmd('merge all')
cubit.cmd('imprint all')
cubit.cmd('rotate Volume all angle 90  about Y include_merged')
cubit.cmd('surface 39 42 57 48 size %f' %(circum/10.))
cubit.cmd('mesh surface 39 42 57 48')
cubit.cmd('volume all size %f' %(LengSize))
cubit.cmd('mesh volume all')
cubit.cmd('group "MagneticMaterial" add volume all')
cubit.cmd('group "deMagCells" add volume 12 13')
cubit.cmd('group "coilRegion" add volume 12 13 14 15 16 17')
cubit.cmd('group "cellLine" add hex 358 363 368 373 378 383 388 393 398 403 408 262 263 264 238 288 293 298 128 129 130 131 132 133 134 135 136 137 138')
cubit.cmd('block 1 group MagneticMaterial')
cubit.cmd('block 1 element type HEX27')
fnme = 'FlaredThinHollowPipe' + '.unv'
cubit.cmd('export ideas "%s" block all overwrite' %(fnme))

