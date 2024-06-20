import re

class NameFormatException(Exception):
    pass

class FunctionArgFormatException(Exception):
    pass

class ProbabilityFormatException(Exception):
    pass

class ProbabilityValueException(Exception):
    pass

constant_regex = '[a-z]+_[a-z]+|[a-z]+'
var_regex = '[A-Z]+[0-9]*'

def constant(name):
    """
    Returns a constant represented as a string - note that only strings of lowercase letters are accepted for simplicity.
    
    This does not return valid ProbLog code, it is to be used in combination with the other functions.
    """
    if re.fullmatch(constant_regex, name) is None:
        raise NameFormatException('Please only use lowercase letters (possibly with an underscore) to specify a name! {} contains non-lowercase letters'.format(name))
    return name

def function(name, *args):
    """
    Returns a function represented as a string 'name(*args)'. 

    Note that each arg must be a variable or a constant or a number.
    """
    args = [ str(arg) for arg in args ]
    for arg in args:
        if re.fullmatch(var_regex,arg) is None and re.fullmatch('[0-9]+',arg) is None and re.fullmatch(constant_regex, arg) is None and arg != '_':
            raise FunctionArgFormatException('Function arguments should be variables or constants or numbers! Which {} is not!'.format(arg))
    return "{f}({xs})".format(f=constant(name), xs=",".join(args))

def fact(term):
    """
    Returns a ProbLog fact. Input: term (constant or function).
    """
    return term + ".\n"

def probabilistic_fact(prob, f):
    """
    Returns a ProbLog probabilistic fact. Input should be probability + term (constant or function).
    """
    try:
        p = float(prob)
    except:
        raise ProbabilityFormatException('Please enter the probability as a float! {} is not a float.'.format(prob))
    if p < 0.0 or p > 1.0:
        raise ProbabilityValueException('Please enter a valid probability value! {} is not valid.'.format(p))
    return "{p} :: {f}".format(p=prob, f=fact(f)) 

def conj(*terms):
    """
    Returns conjunction of given terms (constant or function) as a string, which is not valid ProbLog.
    To be used with clause or probabilistic_clause.
    """
    # calling fact(t) is an ugly workaround to check that the terms are valid without making case distinctions
    return ", ".join([ fact(t)[:len(t)] for t in terms ]) 

def disj(*terms):
    """
    Returns disjunction of given terms (constant or function) as a string, which is not valid ProbLog.
    To be used with clause or probabilistic_clause.
    """
    return "; ".join([ fact(t)[:len(t)] for t in terms ])

def clause(head, body, constraint = ""):
    """
    Returns a ProbLog clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use conj or disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'.
    """
    if constraint != "":
        return "{h} :- {b}, {c}.\n".format(h=head, b=body, c=constraint) 
    else:
        return "{h} :- {b}.\n".format(h=head, b=body) 

def probabilistic_clause(head, body, prob, constraint = ""):
    """
    Returns a ProbLog probabilistic clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use conj or disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'.
    """
    if constraint != "":
        return "{p} :: {h} :- {b}, {c}.\n".format(p=prob, h=head, b=body, c=constraint) 
    else:
        return "{p} :: {h} :- {b}.\n".format(p=prob, h=head, b=body) 

def annotated_disjunction(*prob_facts):
    """
    Returns a ProbLog annotated disjunction.

    prob_facts should be a list of probabilistic facts; 
    this is to be used together with probabilistic_fact.
    """
    return "; ".join([ p_f[:-2] for p_f in prob_facts ]) + ".\n"

def annotated_disjunction_with_body(annotated_disj, body):
    return clause(annotated_disj[:len(annotated_disj)-2], body)

if __name__ == "__main__":
    reg1 = '[1-9][0-9]*'
    reg2 = '[a-z]+'
    print(probabilistic_fact(0.5, 'foo'))
    print(function('a', 1))
