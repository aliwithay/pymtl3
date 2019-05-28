#=========================================================================
# BehavioralRTLIRVisualizationPass.py
#=========================================================================
"""Provide visualization for behavioral RTLIR AST.

Visualize Behavioral RTLIR using Graphviz packeage. The output graph is in PDF
format.  This file is automatically generated by BehavioralRTLIRImplGen.py.
"""

from __future__ import absolute_import, division, print_function

import os

from graphviz import Digraph

from pymtl3.passes.BasePass import BasePass
from pymtl3.passes.rtlir.rtype.RTLIRType import BaseRTLIRType

from .BehavioralRTLIR import BehavioralRTLIRNodeVisitor


class BehavioralRTLIRVisualizationPass( BasePass ):
  def __call__( s, model ):
    visitor = BehavioralRTLIRVisualizationVisitor()

    for blk in model.get_update_blocks():
      visitor.init( blk.__name__ )
      visitor.visit( model._pass_behavioral_rtlir_gen.rtlir_upblks[ blk ] )
      visitor.dump()

class BehavioralRTLIRVisualizationVisitor( BehavioralRTLIRNodeVisitor ):
  def __init__( s ):
    s.output = 'unamed'
    s.output_dir = 'rast-viz'
    s.table_header = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"> '
    s.table_trail = ' </TABLE>>'

  def init( s, name ):
    s.g = Digraph(
      comment = 'BehavioralRTLIR Visualization of ' + name,
      node_attr = { 'shape' : 'plaintext' }
    )
    s.blk_name = name
    s.cur = 0

  def gen_table_opt( s, node ):
    ret = ''
    if isinstance( node.Type, BaseRTLIRType ):
      ret = ' <TR><TD COLSPAN="2">Type: ' + node.Type.__class__.__name__ + '</TD></TR>'
      for name, obj in vars(node.Type).iteritems():
        obj_str = str(obj).replace('<', '&lt;').replace('>', '&gt;')
        if not isinstance( obj, dict ):
          ret += ' <TR><TD>' + name + '</TD><TD>' + obj_str + '</TD></TR>'
        else:
          ret += ' <TR><TD>' + name + '</TD><TD>{' + obj_str + '}</TD></TR>'
    return ret

  def dump( s ):
    if not os.path.exists( s.output_dir ):
      os.makedirs( s.output_dir )
    s.g.render( s.output_dir + os.sep + s.blk_name )

  def visit_CombUpblk( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">CombUpblk</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name)
    s.g.node( str( s.cur ), label = label )
    for i, f in enumerate(node.body):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'body[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_SeqUpblk( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">SeqUpblk</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name)
    s.g.node( str( s.cur ), label = label )
    for i, f in enumerate(node.body):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'body[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_Assign( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Assign</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'target' )
    s.visit( node.target )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_AugAssign( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">AugAssign</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'target' )
    s.visit( node.target )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_If( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">If</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'cond' )
    s.visit( node.cond )
    for i, f in enumerate(node.body):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'body[{idx}]'.format(idx = i) )
      s.visit( f )
    for i, f in enumerate(node.orelse):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'orelse[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_For( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">For</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'var' )
    s.visit( node.var )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'start' )
    s.visit( node.start )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'end' )
    s.visit( node.end )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'step' )
    s.visit( node.step )
    for i, f in enumerate(node.body):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'body[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_Number( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Number</TD></TR> <TR><TD>value</TD><TD>{value}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(value=node.value)
    s.g.node( str( s.cur ), label = label )

  def visit_Concat( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Concat</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    for i, f in enumerate(node.values):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'values[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_ZeroExt( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">ZeroExt</TD></TR> <TR><TD>nbits</TD><TD>{nbits}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(nbits=node.nbits)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_SignExt( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">SignExt</TD></TR> <TR><TD>nbits</TD><TD>{nbits}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(nbits=node.nbits)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_Reduce( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Reduce</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_SizeCast( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">SizeCast</TD></TR> <TR><TD>nbits</TD><TD>{nbits}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(nbits=node.nbits)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_StructInst( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">StructInst</TD></TR> <TR><TD>struct</TD><TD>{struct}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(struct=node.struct)
    s.g.node( str( s.cur ), label = label )
    for i, f in enumerate(node.values):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'values[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_IfExp( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">IfExp</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'cond' )
    s.visit( node.cond )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'body' )
    s.visit( node.body )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'orelse' )
    s.visit( node.orelse )

  def visit_UnaryOp( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">UnaryOp</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'operand' )
    s.visit( node.operand )

  def visit_BoolOp( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">BoolOp</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    for i, f in enumerate(node.values):
      s.g.edge( str(local_cur), str(s.cur+1), label = 'values[{idx}]'.format(idx = i) )
      s.visit( f )

  def visit_BinOp( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">BinOp</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'left' )
    s.visit( node.left )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'right' )
    s.visit( node.right )

  def visit_Compare( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Compare</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'left' )
    s.visit( node.left )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'op' )
    s.visit( node.op )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'right' )
    s.visit( node.right )

  def visit_Attribute( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Attribute</TD></TR> <TR><TD>attr</TD><TD>{attr}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(attr=node.attr)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )

  def visit_Index( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Index</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'idx' )
    s.visit( node.idx )

  def visit_Slice( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Slice</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'value' )
    s.visit( node.value )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'lower' )
    s.visit( node.lower )
    s.g.edge( str(local_cur), str(s.cur+1), label = 'upper' )
    s.visit( node.upper )

  def visit_Base( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Base</TD></TR> <TR><TD>base</TD><TD>{base}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(base=node.base)
    s.g.node( str( s.cur ), label = label )

  def visit_LoopVar( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">LoopVar</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name)
    s.g.node( str( s.cur ), label = label )

  def visit_FreeVar( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">FreeVar</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR> <TR><TD>obj</TD><TD>{obj}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name, obj=node.obj)
    s.g.node( str( s.cur ), label = label )

  def visit_TmpVar( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">TmpVar</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR> <TR><TD>upblk_name</TD><TD>{upblk_name}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name, upblk_name=node.upblk_name)
    s.g.node( str( s.cur ), label = label )

  def visit_LoopVarDecl( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">LoopVarDecl</TD></TR> <TR><TD>name</TD><TD>{name}</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail).format(name=node.name)
    s.g.node( str( s.cur ), label = label )

  def visit_Invert( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Invert</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Not( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Not</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_UAdd( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">UAdd</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_USub( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">USub</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_And( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">And</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Or( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Or</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Add( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Add</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Sub( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Sub</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Mult( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Mult</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Div( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Div</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Mod( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Mod</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Pow( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Pow</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_ShiftLeft( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">ShiftLeft</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_ShiftRightLogic( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">ShiftRightLogic</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_BitAnd( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">BitAnd</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_BitOr( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">BitOr</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_BitXor( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">BitXor</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Eq( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Eq</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_NotEq( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">NotEq</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Lt( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Lt</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_LtE( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">LtE</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_Gt( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">Gt</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )

  def visit_GtE( s, node ):
    s.cur += 1
    local_cur = s.cur
    table_body = '<TR><TD COLSPAN="2">GtE</TD></TR>'
    table_opt = s.gen_table_opt( node )
    label = (s.table_header + table_body + table_opt + s.table_trail)
    s.g.node( str( s.cur ), label = label )
