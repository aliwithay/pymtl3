#=========================================================================
# ImportedObject_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : Jun 2, 2019
"""Test if the imported object works correctly."""

from pymtl3.passes.backends.verilog import TranslationImportPass, VerilogPlaceholderPass
from pymtl3.passes.backends.verilog.import_.test.ImportedObject_test import (
    test_adder,
    test_non_top_portmap,
    test_normal_queue_implicit_top_module,
    test_normal_queue_interface,
    test_normal_queue_params,
    test_param_pass_through,
    test_reg,
    test_reg_external_trace,
    test_reg_incomplete_portmap,
    test_reg_infer_external_trace,
    test_unpacked_port_array,
    test_unpacked_port_array_infer_clk_reset,
    test_vl_uninit,
)
from pymtl3.passes.rtlir.util.test_utility import do_test
from pymtl3.stdlib.test import TestVectorSimulator


def local_do_test( _m ):
  _m.elaborate()
  if not hasattr( _m, "_no_trans_import" ):
    _m.set_metadata( TranslationImportPass.enable, True )
  _m.apply( VerilogPlaceholderPass() )
  m = TranslationImportPass()( _m )
  sim = TestVectorSimulator( m, _m._test_vectors, _m._tv_in, _m._tv_out )
  sim.run_test()
  if hasattr( m, 'finalize' ):
    m.finalize()
