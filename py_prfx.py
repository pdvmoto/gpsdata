# import some...

import os
import sys
from datetime import datetime, date, time, timezone

# constants, like data-directory, masks.

# take the filename, to use as prefix for print- and trace-stmnts
pyfile = os.path.basename(__file__)


# functions:
# f_prfx

# ------------------------------------------------
def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# end of f_prfx, set sourcefile and timestamp

