from typing import List
from pynars.Narsese import Term, Statement, Compound, VarPrefix, Variable
from pynars.utils.IndexVar import IntVar

from .Substitution import Substitution
from pynars.utils.tools import find_pos_with_pos, find_var_with_pos


class Introduction(Substitution):
    '''
    the substitution of const-to-var
    '''
    def __init__(self, term_src: Term, term_tgt: Term, term_common: Term) -> None:
        self.term_common = term_common
        self.term_src = term_src
        self.term_tgt = term_tgt


    def apply(self, term_src: Term=None, term_tgt: Term=None, var_type=VarPrefix.Independent):
        '''
        e.g.
        Input:
            term_src: <robin --> bird>
            term_tgt: <robin --> animal>
            term_common: robin
        Ouput:
            <$x --> bird>
            <$x --> animal>
        '''
        term_src = term_src if term_src is not None else self.term_src
        term_tgt = term_tgt if term_tgt is not None else self.term_tgt

        if var_type is VarPrefix.Independent:
            variables1 = term_src.index_var.var_independent
            variables2 = term_tgt.index_var.var_independent
        elif var_type is VarPrefix.Dependent:
            variables1 = term_src.index_var.var_dependent
            variables2 = term_tgt.index_var.var_dependent
        elif var_type is VarPrefix.Query:
            variables1 = term_src.index_var.var_query
            variables2 = term_tgt.index_var.var_query
        else: raise TypeError("Inalid type")
        id_var = max((*variables1, *variables2, -1)) + 1
        var = Variable(var_type, str(id_var))

        # replace const with var
        def replace(term: 'Term|Statement|Compound', term_r: Term) -> Term:
            '''
            replace constant term with variable
            
            term_r should be a constant
            '''
            nonlocal var
            if term.identical(term_r):
                ''''''
                return var
            
            if term.is_statement:
                if term_r not in term.components: # term.components is not None
                    return term
                stat: Statement = term
                predicate = replace(stat.predicate, term_r)
                subject = replace(stat.subject, term_r)
                return Statement(subject, term.copula, predicate, is_input=True)
            elif term.is_compound:
                if term_r not in term.components: # term.components is not None
                    return term
                cpmd: Compound = term
                terms = (component for component in cpmd.terms)
                return Compound(cpmd.connector, *terms, is_input=True)
            elif term.is_atom:
                return term

        term1 = replace(term_src, self.term_common)
        term2 = replace(term_tgt, self.term_common)
        return term1, term2
        


def get_introduction__const_var(term1: Term, term2: Term, term_common: Term) -> Introduction:
    ''''''
    return Introduction(term1, term2, term_common)

