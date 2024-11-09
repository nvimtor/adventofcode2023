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

  def return_collected(self):
    return self.collected


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
        # we can assume it is only one match for now
        matches = finder.insert_char(char)

        if matches:
          digit = strtodigit[matches[-1]]

          if first is None and digit:
            first = digit

          last = digit

    sum += combinedigits(int(first), int(last))

  return sum

input = getinput()
sum = run(input)
