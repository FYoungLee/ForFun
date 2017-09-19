def puzzle_1():
    '''
         好 是 好
    +    要 做 好
    ------------
      要 做 好 事

      ?  ?  ?  ?
    '''
    for x in range(100, 1000):
        for y in range(100, 1000):
            A = x // 100
            B = x % 100 // 10
            C = x % 10
            D = y // 100
            E = y % 100 // 10
            F = y % 10
            left = x + y
            right = D * 1000 + E * 100 + A * 10 + B
            if A == C == F and  left == right:
                print(D, E, A, B)
