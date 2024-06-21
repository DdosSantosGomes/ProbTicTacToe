import re

constant_regex = '[a-z]+|0|[1-9][0-9]*'
var_regex = '[A-Z]+[0-9]*'
term_regex = '[a-z]+_[a-z]+|[a-z]+|[a-z]+[0-9]*'

def variable(name):
    """
    Returns a variable represented as a string - note that only strings of uppercase letters, possibly followed by numbers, are accepted for simplicity.
    
    This does not return valid ProbLog code, it is to be used in combination with the other functions.
    """
    if re.fullmatch(var_regex, name) is None:
        raise NameFormatException('Please only use uppercase letters, followed possibly by numbers, to specify a variable! \
                                  {} is not it'.format(name))
    return name

def constant(name):
    """
    Returns a constant represented as a string - note that only strings of lowercase letters and numbers are accepted for simplicity.
    
    This does not return valid ProbLog code, it is to be used in combination with the other functions.
    """
    name = str(name)
    if re.fullmatch(constant_regex, name) is None:
        raise NameFormatException('Please only use lowercase letter to specify a name! \
                                  {} contains non-lowercase letters'.format(name))
    return name

def function(name, *args):
    """
    Returns a function represented as a string 'name(*args)'. 

    Note that each arg must be a variable or a constant or a number.
    """
    if re.fullmatch(term_regex, name) is None:
        raise FunctionNameException('Function names should consist of only lowercase letters, possibly with one underscore or numbers following! \
                                    {} is not that'.format(name))
    args = [ str(arg) for arg in args ]
    for arg in args:
        arg_regex = '{var}|{const}|_|0|[1-9][0-9]*'.format(var=var_regex, const=constant_regex)
        if re.fullmatch(arg_regex,arg) is None:
            raise FunctionArgFormatException('Function arguments should be variables or constants or numbers! \
                                             Which {} is not!'.format(arg))
    return "{f}({xs})".format(f=name, xs=",".join(args))

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
        raise ProbabilityFormatException('Please enter the probability as a float! \
                                         {} is not a float.'.format(prob))
    if p < 0.0 or p > 1.0:
        raise ProbabilityValueException('Please enter a valid probability value! \
                                        {} is not valid.'.format(p))
    return "{p} :: {f}".format(p=prob, f=fact(f)) 

def term_conj(*terms):
    """
    Returns conjunction of given terms (constant or function) as a string, which is not valid ProbLog. \n
    To be used with clause or probabilistic_clause. Please use it with function or constant.
    """
    return ", ".join(terms) 

def term_disj(*terms):
    """
    Returns disjunction of given terms (constant or function) as a string, which is not valid ProbLog. \n
    To be used with clause or probabilistic_clause. Please use it with function or constant.
    """
    return "; ".join(terms)

def simple_constraint(var1, var2):
    """
    Returns a constraint of the form 'var1 is var2+1'.
    """
    return '{A} is {B}+1'.format(A=var1, B=var2)

def clause(head, body, constraint = ""):
    """
    Returns a ProbLog clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use term_conj or term_disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'. Use simple_constraint for that
    """
    if constraint != "":
        return "{h} :- {b}, {c}.\n".format(h=head, b=body, c=constraint) 
    else:
        return "{h} :- {b}.\n".format(h=head, b=body) 

def probabilistic_clause(head, body, prob, constraint = ""):
    """
    Returns a ProbLog probabilistic clause. 

    Head: should be a term.
    Body: term, or conjunction or disjunction of terms (use term_conj or term_disj).
    Constraint: should be e.g. of the form 'B' is 'A+1'. Use simple_constraint for that
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
    """
    Returns a ProbLog annotated disjunction with the given body.

    Use in combination with annotated_disjunction for the head,
    and conj or disj of terms for the body.
    """
    return clause(annotated_disj[:-2], body)

def query(*qs):
    """
    Returns a string of ProbLog queries. 

    To be used with term or constant.
    """
    out = ''
    for q in qs:
        out += 'query({}).\n'.format(q)
    return out

def evidence(*es):
    """
    Returns a string of ProbLog evidence. 

    To be used with term or constant.
    """
    out = ''
    for e in es:
        out += 'evidence({}).\n'.format(e)
    return out

class NameFormatException(Exception):
    pass

class FunctionNameException(Exception):
    pass

class FunctionArgFormatException(Exception):
    pass

class ProbabilityFormatException(Exception):
    pass

class ProbabilityValueException(Exception):
    pass

if __name__ == "__main__":
    reg1 = '[1-9][0-9]*'
    reg2 = '[a-z]+'
    print(probabilistic_fact(0.5, 'foo'))
    print(function('a', 1))
