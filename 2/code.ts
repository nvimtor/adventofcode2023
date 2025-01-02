type Parser<A> = (i: string) => [string, A]


// map :: f a -> (a -> b) -> f b
const map = <A>(p: Parser<A>) => <B>(ab: ((a: A) => B)): Parser<B> => {
  return (i: string) => {
    const [remaining, result] = p(i)
    return [remaining, ab(result)]
  }
}

// flatMap :: (f a) -> (a -> f b) -> f b
// this can be just join . map
const flatMap = <A>(p: Parser<A>) => <B>(afb: ((a: A) => Parser<B>)): Parser<B> => {
  return (i: string) => {
    const [remaining, result] = p(i)
    throw new Error('todo')
  }
}

const getRest = <X, Y>([_, ...rest]: [X, ...Y[]]): Y[] => rest

// NOTE shit implementation of pipe
// for a better, well-typed version, check fp-ts' pipe
const pipe = (...args: [string, ...((a: any) => any)[]]) => {
  const head: string = args[0]

  let acc: unknown = head
  for (const fn of getRest(args)) {
    acc = fn(acc)
  }
  return acc
}

const pipetest = () => {
  const input = 'hello'
  const x = (a: string) => {
    return a + ' world'
  }
  const y = (a: string) => {
    return a + ' you good?'
  }
  const out = pipe(input, x, y)

  console.log(out)
}

pipetest()

const main () => {

}
