import tracemalloc

'''
NOTE
some quick findings;
we don't really need a worker.current
because we can just calculte it from the trie.
however, we only store the current node in the trie.
what we can do instead is store only the letters.

I am not sure, but there is a possibility that storing the current node copies the current node (not just a pointer to it, but Python might create a copy). I'd like to verify that, not sure how to though
'''
strtodigit = {
  'zero': 0,
  'one': 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9
}

def createtrie(words):
  trie = {}

  for word in words:
    curr = trie

    for char in word:
      if char not in curr:
        curr[char] = {}
      curr = curr[char]

    curr['_end_'] = 1

  return trie

# TODO check if a copy happens here
'''
use `tracemalloc`
'''
class Finder:
  def __init__(self, words):
    self.trie = createtrie(words)
    self.last_worker_id = -1
    self.workers = {}

  def insert_char(self, char):
    self.last_worker_id += 1
    next_worker_id = self.last_worker_id

    worker = {
      'current': self.trie,
      'content': ''
    }

    self.workers[next_worker_id] = worker

    matches = []

    worker_ids_to_clean = []

    for id, worker in self.workers.items():
      if char in worker['current']:
        worker['content'] += char
        worker['current'] = worker['current'][char]
      else:
        worker_ids_to_clean.append(id)

      if '_end_' in worker['current']:
        matches.append(worker['content'])
        worker_ids_to_clean.append(id)
        continue

    for id in worker_ids_to_clean:
      del self.workers[id]

    return matches

def combinedigits(first, last):
  return (first * 10) + last

def getinput():
  with open('./input.txt', 'r') as input:
    lines = input.readlines()
    return lines

def run(input):
  finder = Finder(list(strtodigit.keys()))
  sum = 0

  for line in input:
    first = None
    last = None

    for char in line:
      if char.isdigit():
        if first is None:
          first = char

        last = char
      else:
        matches = finder.insert_char(char)

        if matches:
          digit = strtodigit[matches[-1]]

          if first is None and digit:
            first = digit

          last = digit

    sum += combinedigits(int(first), int(last))

  return sum

tracemalloc.start()
input = getinput()
sum = run(input)
print(sum)
tracemalloc.stop()

traced_mem = tracemalloc.get_traced_memory()

print(traced_mem)

'''
NOTE
this is how we can use tracemalloc
ideally we can just trace part of the code, where we cpy the current trie

or we can allocate the whle ccode (which i think it is better because the area impact is very small)
'''
