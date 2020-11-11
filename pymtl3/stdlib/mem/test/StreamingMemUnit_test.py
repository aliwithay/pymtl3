#=========================================================================
# StreamingMemUnit_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : Nov 10, 2020

from pymtl3 import *
from pymtl3.stdlib.mem import mk_mem_msg, MagicMemoryCL

from pymtl3.passes.backends.verilog import VerilogTranslationImportPass, \
                                           VerilogVerilatorImportPass, \
                                           VerilogPlaceholderPass
from pymtl3.stdlib.test_utils import TestSinkCL, TestSrcCL

from .StreamingMemUnitHost import StreamingMemUnitHost
from ..StreamingMemUnit import StreamingMemUnit

class TestHarness( Component ):

  def construct( s, DataType, AddrType, StrideType, CountType,
                 src_base_addr, src_x_stride, src_x_count,
                 src_y_stride, src_y_count, dst_base_addr, dst_ack_addr,
                 sink_msgs ):

    s.addr_nbits = AddrType.nbits
    ReqMsgType, RespMsgType = mk_mem_msg( 1, AddrType.nbits, DataType.nbits )

    s.dut = StreamingMemUnit( DataType, AddrType, StrideType, CountType )
    s.mem = MagicMemoryCL( 1, [(ReqMsgType, RespMsgType)] )
    s.host = StreamingMemUnitHost( DataType, AddrType, StrideType, CountType,
                                   src_base_addr, src_x_stride,
                                   src_x_count, src_y_stride,
                                   src_y_count, dst_base_addr, dst_ack_addr )

    s.local_req_sink = TestSinkCL( ReqMsgType, sink_msgs )
    s.local_resp_src = TestSrcCL( RespMsgType, [] )

    s.dut.cfg //= s.host.cfg
    s.dut.remote //= s.mem.ifc[0]
    s.dut.local.req //= s.local_req_sink.recv
    s.dut.local.resp //= s.local_resp_src.send

  def load_mem_image( s ):
    for i in range(2**s.addr_nbits-1):
      s.mem.write_mem( i, [i%256] )

  def done( s ):
    return s.local_req_sink.done() and s.local_resp_src.done()

  def line_trace( s ):
    return s.dut.line_trace() + " || " + s.local_req_sink.line_trace()

def get_mem_word( addr ):
  data = 0
  for i in range(4):
    data = data << 8
    data += ( addr + 4-1-i ) % 256
  return Bits32(data)

def gen_sink_msgs( O, A, D, s_base, x_stride, x_count, y_stride, y_count,
                   d_base, d_ack_addr ):
  msgs = []
  dst_addr = d_base
  MsgType, _ = mk_mem_msg( O, A, D )

  row_addr = s_base
  for y in range(y_count):
    for x in range(x_count):
      addr = row_addr + x * x_stride
      word = get_mem_word( addr )

      msg = MsgType()
      msg.type_  = Bits4(1)
      msg.opaque = mk_bits(O)(0)
      msg.addr   = mk_bits(A)(dst_addr)
      msg.len    = mk_bits(clog2(D>>3))(0)
      msg.data   = mk_bits(D)(word)

      msgs.append( msg )
      dst_addr += 4

    row_addr += y_stride

  # Append ack message

  msg = MsgType()
  msg.type_  = Bits4(1)
  msg.opaque = mk_bits(O)(0)
  msg.addr   = mk_bits(A)(d_ack_addr)
  msg.len    = mk_bits(clog2(D>>3))(0)
  msg.data   = mk_bits(D)(1)

  msgs.append( msg )

  return msgs

def run_test( th, cmdline_opts ):
  th.elaborate()
  if cmdline_opts['test_verilog']:
    th.dut.set_metadata( VerilogTranslationImportPass.enable, True )
    if cmdline_opts['dump_vcd']:
      th.dut.set_metadata( VerilogVerilatorImportPass.vl_trace, True )
    th.apply( VerilogPlaceholderPass() )
    th.apply( VerilogTranslationImportPass() )
  th.apply( DefaultPassGroup() )
  th.sim_reset()

  th.load_mem_image()

  curT, maxT = 0, 300

  # DUT operation
  while not th.done() and curT < maxT:
    th.sim_tick()
    # print(th.dut.line_trace())
    curT += 1

  assert curT < maxT, "Time out!"

def test_simple( cmdline_opts ):
  O, D, A, S, C = Bits1, Bits32, Bits20, Bits10, Bits10
  Types = [ D, A, S, C ]

  src_base_addr = 0
  src_x_stride = 4
  src_x_count = 16
  src_y_stride = 64*4
  src_y_count = 16
  dst_base_addr = 0
  dst_ack_addr = 2048

  Params = [src_base_addr, src_x_stride, src_x_count,
            src_y_stride, src_y_count, dst_base_addr, dst_ack_addr]

  sink_msgs = gen_sink_msgs( O.nbits, A.nbits, D.nbits, src_base_addr,
                             src_x_stride, src_x_count,
                             src_y_stride, src_y_count,
                             dst_base_addr, dst_ack_addr )

  run_test( TestHarness( *Types, *Params, sink_msgs ), cmdline_opts )
