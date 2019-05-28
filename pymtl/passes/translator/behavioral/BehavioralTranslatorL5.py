#=========================================================================
# BehavioralTranslatorL5.py
#=========================================================================
# Author : Peitian Pan
# Date   : March 22, 2019
"""Provide L5 behavioral translator."""
from __future__ import absolute_import, division, print_function

from pymtl.passes.rtlir.behavioral.BehavioralRTLIRGenL5Pass import (
    BehavioralRTLIRGenL5Pass,
)
from pymtl.passes.rtlir.behavioral.BehavioralRTLIRTypeCheckL5Pass import (
    BehavioralRTLIRTypeCheckL5Pass,
)

from .BehavioralTranslatorL4 import BehavioralTranslatorL4


class BehavioralTranslatorL5( BehavioralTranslatorL4 ):
  def __init__( s, top ):
    super( BehavioralTranslatorL5, s ).__init__( top )

  #-----------------------------------------------------------------------
  # _gen_behavioral_trans_metadata
  #-----------------------------------------------------------------------

  # Override
  def _gen_behavioral_trans_metadata( s, m ):
    m.apply( BehavioralRTLIRGenL5Pass() )
    m.apply( BehavioralRTLIRTypeCheckL5Pass() )
    s.behavioral.rtlir[m] = m._pass_behavioral_rtlir_gen.rtlir_upblks
    s.behavioral.freevars[m] =\
        m._pass_behavioral_rtlir_type_check.rtlir_freevars
    s.behavioral.tmpvars[m] =\
        m._pass_behavioral_rtlir_type_check.rtlir_tmpvars

    # Visit the whole component hierarchy because now we have subcomponents
    for child in m.get_child_components():
      s._gen_behavioral_trans_metadata( child )

  #-----------------------------------------------------------------------
  # translate_behavioral
  #-----------------------------------------------------------------------

  # Override
  def translate_behavioral( s, m ):
    super( BehavioralTranslatorL5, s ).translate_behavioral( m )
    for child in m.get_child_components():
      s.translate_behavioral( child )