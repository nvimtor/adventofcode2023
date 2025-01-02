from functools import partial

# we know that a parser is just s -> (s, a)
'''
we know a parser is just a function s -> (s, a)

where s is the input, a is the result. the input will change over time

left side -> remaining
right side -> result

map :: f a -> (a -> b) -> f b
flatMap :: (f a) -> (a -> f b) -> f b

flatMap :: (s -> (s, a)) -> (s -> (s, a))
do:
a <- >
;; NOTE assume every result is a list
'''

class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)

def empty():
  def parse(inp):
    return inp, inp

  return parse

'''
NOTE
x -> f1 -> y,
y -> f2 -> z,
z -> f3 -> a
we want a reduce
'''
def mapr(f):
  def parse(p, inp):
    remaining, result = p(inp)
    return remaining, f(result)

  return partial(parse)

'''
(a -> b) bin (b -> a)
'''
def reduce(xs, id):
  if (len(xs) == 0):
    raise ValueError("expected non-empty list")

  acc = id
  for fn in xs:
    acc = fn(acc)[1]

  return acc

def pipe(*args):
  # TODO not sure this is needed
  fns = list(args)

  return reduce(fns[1:], fns[0])

def bind(key, p):
  def append(result):
    result[key] = result
    return result

  return pipe(p, mapr(append))

def flatMap(p, f):
  def parse(inp):
    result, remaining = p(inp)
    new_remaining = f(remaining)

def strp(inp):
  if not isinstance(inp, str):
    raise ParseError("Expected string")

  return inp, ''

def char(c):
  def parse2(inp):
    return None

  def parse(inp):
    # map(parse2,)
    if (inp.length == 0):
      raise ParseError(f"Expected non-empty string")

    return type(inp[0])

  return parse

def main():
  # print(char("a")("abc"))
  empty_parser = empty()
  acc = pipe(
    'abc',
    empty_parser,
    empty_parser,
  )

  acc2 = pipe(
    'abcd',
    empty_parser,
    mapr(lambda x: 2)
  )

  # print(acc)
  print(acc2)
  print("done")

main()
