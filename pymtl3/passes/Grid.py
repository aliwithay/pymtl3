"""
#=========================================================================
# Grid.py
#=========================================================================
# everything in the same granularity should have the same height
# but probably different width (that will be aligned as much as
# possible).
#
# Author : Cheng Tan
#   Date : Oct 28, 2019
"""

class Grid( object ):
  def __init__( s, row_id = 0, col_id = 0, rows = 1, cols = 1, parent = None ):
    s.sub_grids = None
    s.parent = parent
    s.row_id = row_id
    s.col_id = col_id
    s.component = None
    s.x_ratio = 0.0
    s.y_ratio = 0.0
    s.w_ratio = 1.0
    s.h_ratio = 1.0
    s.dim_x = 0
    s.dim_y = 0
    s.dim_w = 0
    s.dim_h = 0
    s.isLeaf = False
    s.total_rows = rows
    s.total_cols = cols

  def bond( s, components ):
    if type(components) != list:
      s.setComponent( comonents )
    else:
      s.sub_grids = s.divide( 1, len(components) )
      for i in range( len(components) ):
        s.sub_grids[0][i].setComponent( components[i] )

  def divide( s, rows, cols ):
    s.sub_grids = [ [ Grid(i,j,rows,cols) for j in range(cols) ]
                      for i in range(rows) ]
    w_ratio = s.w_ratio/cols
    h_ratio = s.h_ratio/cols
    for r in range( rows ):
      for c in range( cols ):
        s.sub_grids[r][c].w_ratio = w_ratio
        s.sub_grids[r][c].h_ratio = h_ratio
        s.sub_grids[r][c].x_ratio = s.x_ratio + c*w_ratio
        s.sub_grids[r][c].y_ratio = s.y_ratio + r*h_ratio
        s.sub_grids[r][c].parent = s
    return s.sub_grids

  def updateChildDim( s, child_dim_w, child_dim_h ):
    rows = len( s.sub_grids )
    cols = len( s.sub_grids[0] )
    if s.dim_w < child_dim_w * cols:
      s.dim_w = child_dim_w * cols
    if s.dim_h < child_dim_h * rows:
      s.dim_h = child_dim_h * rows

  def setComponent( s, component ):
    s.component = component
    max_w = 0
    max_h = 0
    if hasattr( component, "dim_w" ):
      max_w = component.dim_w
    if hasattr( component, "dim_h" ):
      max_h = component.dim_h
    print( "now in ", component._dsl.my_name )
    if hasattr( component, "sub_grids" ):
      print( "there is sub_grids..." )
    else:
      s.dim_w = component.dim_w
      s.dim_h = component.dim_h
      print( "no sub_grids..." )
