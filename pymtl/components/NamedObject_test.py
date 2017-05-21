from NamedObject import NamedObject
from pymtl.tools import recursive_tag_name
from collections import deque

class Chicken(NamedObject):
  def __init__( s ):
    s.protein = NamedObject()

class Dog(NamedObject):
  def __init__( s ):
    s.chicken = Chicken()

class Tiger(NamedObject):
  def __init__( s ):
    s.rooster = Chicken()

class Human(NamedObject):
  def __init__( s, nlunch=1, ndinner=1 ):

    if nlunch == 1: s.lunch = Tiger()
    else:           s.lunch = [ Tiger() for _ in xrange(nlunch) ]

    if ndinner == 1: s.dinner = Dog()
    else:            s.dinner = deque( [ Dog() for _ in xrange(ndinner) ] )

def test_NamedObject_normal():

  x = Human( nlunch=1, ndinner=1 )
  recursive_tag_name( x )

  assert x.full_name() == "top"

  assert x.lunch.full_name() == "top.lunch"
  assert x.dinner.full_name() == "top.dinner"

  assert x.lunch.rooster.full_name() == "top.lunch.rooster"
  assert x.dinner.chicken.full_name()== "top.dinner.chicken"

  assert x.lunch.rooster.protein.full_name() == "top.lunch.rooster.protein"
  assert x.dinner.chicken.protein.full_name()== "top.dinner.chicken.protein"

def test_NamedObject_deque():

  x = Human( nlunch=1, ndinner=5 )
  recursive_tag_name( x )

  assert x.full_name() == "top"

  assert x.lunch.full_name() == "top.lunch"
  assert x.dinner[2].full_name() == "top.dinner[2]"

  assert x.lunch.rooster.full_name() == "top.lunch.rooster"
  assert x.dinner[2].chicken.full_name()== "top.dinner[2].chicken"

  assert x.lunch.rooster.protein.full_name() == "top.lunch.rooster.protein"
  assert x.dinner[1].chicken.protein.full_name()== "top.dinner[1].chicken.protein"

def test_NamedObject_list():

  x = Human( nlunch=4, ndinner=1 )
  recursive_tag_name( x )

  assert x.full_name() == "top"

  assert x.lunch[3].full_name() == "top.lunch[3]"
  assert x.dinner.full_name() == "top.dinner"

  assert x.lunch[3].rooster.full_name() == "top.lunch[3].rooster"
  assert x.dinner.chicken.full_name()== "top.dinner.chicken"

  assert x.lunch[3].rooster.protein.full_name() == "top.lunch[3].rooster.protein"
  assert x.dinner.chicken.protein.full_name()== "top.dinner.chicken.protein"

