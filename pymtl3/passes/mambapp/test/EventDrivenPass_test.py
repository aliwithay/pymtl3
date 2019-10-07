#=========================================================================
# EventDrivenPass_test.py
#=========================================================================
#
# Author : Shunning Jiang
# Date   : Oct 6, 2019

from pymtl3.dsl import *
from pymtl3.dsl.errors import UpblkCyclicError
from pymtl3.passes.mambapp.EventDrivenPass import EventDrivenPass
from pymtl3.passes.GenDAGPass import GenDAGPass
from pymtl3.passes.SimpleTickPass import SimpleTickPass


def _test_model( cls ):
  A = cls()
  A.elaborate()
  A.apply( GenDAGPass() )
  A.apply( EventDrivenPass() )
  A.lock_in_simulation()

  T = 0
  while T < 5:
    A.tick()
    print(A.line_trace())
    T += 1

def test_false_cyclic_dependency():

  class Top(Component):

    def construct( s ):
      s.a = Wire(int)
      s.b = Wire(int)
      s.c = Wire(int)
      s.d = Wire(int)
      s.e = Wire(int)
      s.f = Wire(int)
      s.g = Wire(int)
      s.h = Wire(int)
      s.i = Wire(int)
      s.j = Wire(int)
      s.k = Wire(int)

      @s.update
      def up1():
        s.a = 10 + s.i
        s.b = s.d + 1

      @s.update
      def up2():
        s.c = s.a + 1
        s.e = s.d + 1

      @s.update
      def up3():
        s.d = s.c + 1
        print("up3 prints out d =", s.d)

      @s.update
      def up4():
        s.f = s.d + 1

      @s.update
      def up5():
        s.g = s.c + 1
        s.h = s.j + 1
        print("up5 prints out h =", s.h)

      @s.update_on_edge
      def up6():
        s.i = s.i + 1

      @s.update
      def up7():
        s.j = s.g + 1
        s.k = s.e + 1

    def done( s ):
      return True

    def line_trace( s ):
      return "a {} | b {} | c {} | d {} | e {} | f {} | g {} | h {} | i {} | j {} | k {}" \
              .format( s.a, s.b, s.c, s.d, s.e, s.f, s.g, s.h, s.i, s.j, s.k )

  _test_model( Top )

def test_top_level_inport():

  class Top(Component):

    def construct( s ):
      s.in_ = InPort(int)
      s.i = Wire(int)
      s.a = Wire(int)

      @s.update
      def up1():
        s.a = s.in_

      @s.update_on_edge
      def up2():
        s.i = s.i + s.a

    def done( s ):
      return True

    def line_trace( s ):
      return "a {} | i {} | in_ {}" \
              .format( s.a, s.i, s.in_ )
  A = Top()
  A.elaborate()
  A.apply( GenDAGPass() )
  A.apply( EventDrivenPass() )
  A.lock_in_simulation()

  T = 10
  while T < 15:
    A.in_ = T
    A.tick()
    print(A.line_trace())
    T += 1

def test_very_deep_dag():

  class Inner(Component):
    def construct( s ):
      s.in_ = InPort(int)
      s.out = OutPort(int)

      @s.update
      def up():
        s.out = s.in_ + 1

    def done( s ):
      return True

    def line_trace( s ):
      return "{} > {}".format( s.a, s.b, s.c, s.d )

  class Top(Component):
    def construct( s, N=2000 ):
      s.inners = [ Inner() for i in range(N) ]
      for i in range(N-1):
        s.inners[i].out //= s.inners[i+1].in_

    def done( s ):
      return True
    def line_trace( s ):
      return ""

  _test_model( Top )
