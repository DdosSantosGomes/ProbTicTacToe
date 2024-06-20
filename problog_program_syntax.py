import re

class NameFormatException(Exception):
    pass

class FunctionArgFormatException(Exception):
    pass

class ProbabilityFormatException(Exception):
    pass

class ProbabilityValueException(Exception):
    pass

def constant(name):
    """
    Returns a constant represented as a string - note that only strings of lowercase letters are accepted for simplicity.
    
    This does not return valid ProbLog code, it is to be used in combination with the other functions.
    """
    regex = '[a-z]+'
    if re.match(regex, name) != name:
        raise NameFormatException('Please only use lowercase letters to specify a name!')
    return name

def function(name, *args):
    """
    Returns a function represented as a string name(*args). 

    Note that each arg must be a variable or a number.
    """
    for arg in args:
        if re.match('[A-Z]',arg) != arg or re.match('[1-9][0-9]*',arg) != arg:
            raise FunctionArgFormatException('Function arguments should be variables or numbers!')
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
        raise ProbabilityFormatException('Please enter the probability as a float!')
    if p < 0.0 or p > 1.0:
        raise ProbabilityValueException('Please enter a valid probability value!')
    return "{p} :: {f}".format(p=prob, f=fact(f)) 

def conj(*terms):
    """
    Returns conjunction of given terms (constant or function) as a string, which is not valid ProbLog.
    To be used with clause or probabilistic_clause.
    """
    return ",".join([ fact(t[:len(t)-2]) for t in terms ])

def disj(*terms):
    """
    Returns disjunction of given terms (constant or function) as a string, which is not valid ProbLog.
    To be used with clause or probabilistic_clause.
    """
    return ";".join([ fact(t[:len(t)-2]) for t in terms ])

def clause(head, body, constraint = ""):
    """
    Returns a ProbLog clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use conj or disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'.
    """
    return "{h} :- {b}, {c}.\n".format(h=head, b=body, c=constraint)

def probabilistic_clause(head, body, prob, constraint = ""):
    """
    Returns a ProbLog probabilistic clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use conj or disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'.
    """
    return "{p} :: {h} :- {b}, {c}.\n".format(p=prob, h=head, b=body, c=constraint)

def annotated_disjunction(prob_facts):
    """
    Returns a ProbLog annotated disjunction.

    prob_facts should be a list of probabilistic facts; 
    this is to be used together with probabilistic_fact.
    """
    return "; ".join([ p_f[:len(p_f)-2] for p_f in prob_facts ]) + ".\n"

if __name__ == "__main__":
    c = constant('a')
    print(c)
