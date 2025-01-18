#!python
#!python
import sys
import string

from array import *

Length = 8 * 25.4
r_out = 21.0 / 2.0
r_in = 18.0 / 2.0

r_end = 24.0 / 2.0
Lend = 1.125*25.4
Lbevel = 0.125 * 25.4
Lcent = Length - 2.0 * (Lend + Lbevel)
LFcoil = 39.0 / 2.0


circum = 2.0 * 3.14 * r_out

surfsize = r_out
LengSize = Length / 91.0

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

cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(0))
cubit.cmd('webcut volume all with plane zplane offset %f imprint merge' %(LFcoil))
cubit.cmd('webcut volume all with plane yplane offset 0 noimprint nomerge')
cubit.cmd('delete volume with x_coord > 0')
cubit.cmd('delete volume with y_coord < 0')
cubit.cmd('delete volume with z_coord < 0')
cubit.cmd('merge all')
cubit.cmd('imprint all')
cubit.cmd('rotate Volume all angle 90  about Y include_merged')
cubit.cmd('volume all size %f' %(LengSize))
cubit.cmd('mesh volume all')
cubit.cmd('group "MagneticMaterial" add volume all')
cubit.cmd('group "coilRegion" add volume 29')
cubit.cmd('group "Mhex" add hex 315')
cubit.cmd('group "Mline" add hex with y_coord < 2.33647')

cubit.cmd('block 1 group MagneticMaterial')
cubit.cmd('block 1 element type HEX27')
fnme = 'FlaredThinHollowPipe_3planeSym' + '.unv'
#cubit.cmd('export ideas "%s" block all overwrite' %(fnme))




