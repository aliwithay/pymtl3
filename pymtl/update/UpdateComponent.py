import re, inspect, ast
p = re.compile('( *(@|def))')
from collections import defaultdict, deque

class TS:
  def __init__( self, func ):
    self.func = func
  def __lt__( self, other ):
    return (self.func, other.func)
  def __gt__( self, other ):
    return (other.func, self.func)
  def __call__( self ):
    self.func()

class UpdateComponent( object ):

  def __new__( cls, *args, **kwargs ):
    inst = object.__new__( cls, *args, **kwargs )
    inst._blkid_upblk = {}
    inst._name_upblk = {}
    inst._upblks = []

    inst._constraints = []
    inst._schedule_list = []
    return inst

  def update( s, blk ):
    s._blkid_upblk[ id(blk) ] = blk
    s._name_upblk[ blk.__name__ ] = blk
    s._upblks.append( blk )
    return TS(blk)

  def get_update_block( s, name ):
    return TS(s._name_upblk[ name ])

  def add_constraints( s, *args ):
    s._constraints.extend( [ x for x in args ] )

  def _elaborate( s, model ):

    for name, obj in model.__dict__.iteritems():
      if   isinstance( obj, UpdateComponent ):
        s._elaborate( obj )

        model._blkid_upblk.update( obj._blkid_upblk )
        model._upblks.extend( obj._upblks )

  def _schedule( s ):

    N = len( s._upblks )
    edges = [ [] for _ in xrange(N) ] 
    InDeg = [ 0  for _ in xrange(N) ]
    Q     = deque()

    # Discretize in O(NlogN), to avoid later O(logN) lookup

    id_vtx = dict()
    for i in xrange(N):
      id_vtx[ id(s._upblks[i]) ] = i

    # Prepare the graph

    for (x, y) in s._constraints:
      vtx_x = id_vtx[ id(x) ]
      vtx_y = id_vtx[ id(y) ]
      edges[ vtx_x ].append( vtx_y )
      InDeg[ vtx_y ] += 1

    # Perform topological sort in O(N+M)

    for i in xrange(N):
      if InDeg[i] == 0:
        Q.append( i )

    while Q:
      import random
      random.shuffle(Q)

      u = Q.popleft()
      s._schedule_list.append( s._upblks[u] )
      for v in edges[u]:
        InDeg[v] -= 1
        if InDeg[v] == 0:
          Q.append( v )

    if len(s._schedule_list) < len(s._upblks):
      raise Exception("Update blocks have cyclic dependencies.")

  def elaborate( s ):
    s._elaborate( s )
    s._schedule()
    print

  def cycle( s ):
    for blk in s._schedule_list:
      blk()

  def print_schedule( s ):
    for blk in s._schedule_list:
      print blk.__name__