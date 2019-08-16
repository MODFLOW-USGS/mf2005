Data Set 1

ISUBCB ISUBOC NNDB NDB NMZ NN AC1 AC2 ITMIN IDSAVE IDREST [IDBIT]

IDBIT - is an optional flag

  + If IDBIT <= 1, the delay bed solution is not wrapped in an 
    iteration loop. This is the default approach and is identical
    to previous versions of MODFLOW-2005 (prior to 1.13) 
    
  + If IDBIT > 1, the delay bed solution is wrapped in an 
    iteration loop. This modification was made to solve example
    problem 1 in the documentation. Since the delay bed is bounded
    be constant heads the MODFLOW iterations converge before the
    delay bed solution is converged. Delay beds are also solved
    in terms of head rather than delta head to reduce roundoff
    errors.
    
         