
########################################################################
#  IMPORTS
# ######################################################################
from strings_with_arrows import *

########################################################################
#  CONSTANTS
# ######################################################################
DIGITS='0123456789'


########################################################################
#  ERRORS
# ######################################################################

class Error:
    """
    Deal with all errors in the code giving the position and details of the error
    """

    def __init__(self,pos_start, pos_end, error_name, details):
        self.pos_start=pos_start
        self.pos_end=pos_end
        self.error_name=error_name
        self.details=details

    def as_string(self):
        result=f'{self.error_name}: {self.details}'
        result+=f'\nFile {self.pos_start.fn}, line {self.pos_start.ln+1}'
        result+='\n\n'+string_with_arrows(self.pos_start.ftxt,self.pos_start,self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end,'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self,pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end,'Invalid Syntax', details)

class RTError(Error):
    def __init__(self,pos_start, pos_end, details,context):
        super().__init__(pos_start, pos_end,'Runtime Error', details)
        self.context=context

    def as_string(self):
        result=self.generate_traceback()
        result+=f'{self.error_name}: {self.details}'
        result+='\n\n'+string_with_arrows(self.pos_start.ftxt,self.pos_start,self.pos_end)
        return result


    def generate_traceback(self):
        result=''
        pos=self.pos_start
        ctx=self.context

        while ctx:
            result=f' File {pos.fn}, line  {str(pos.ln+1)}, in {ctx.display_name}\n '+ result
            pos= ctx.parent_entry_pos
            ctx=ctx.parent

        return 'Traceback (most recent call last):\n '+ result



########################################################################
#  POSITION
# ######################################################################

class Position():
    """
    Manage the position of different tokkens.
    Mostly to be able to give the position start and position end of eventual errors and the file and context
    idx: is the index of the specific position
    col: column associated
    ln : line associated
    fn : file name
    ftxt: context of the executed code

    The class has two modules, advance that goes to the next character and copy to save a position to an other variable to fixe it.
    """

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx=idx
        self.ln=ln
        self.col=col
        self.fn=fn
        self.ftxt=ftxt

    def advance(self, current_char=None):
        self.idx+=1
        self.col+=1
        if current_char=="\n":
            self.ln+=1
            self.col=0
        return self


    def copy(self):
        return(Position(self.idx, self.ln, self.col, self.fn, self.ftxt ))



########################################################################
#  TOKENS
# ######################################################################

#Are the different token types existing in our code
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

TT_EOF = 'EOF'


class Token:
    """
    This class will manage the small individual basic element of the program called tokens.
    A token has a type, a start position and a end position.
    and can have a value like for int or float tokens.
    """

    def __init__(self,type_,value=None,pos_start=None,pos_end=None):
        self.type=type_
        self.value=value

        if pos_start:
            self.pos_start=pos_start.copy()
            self.pos_end=self.pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end=pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


########################################################################
#  LEXER
# ######################################################################

class Lexer:
    """
    a class that convert the code providing in the variable "text" into
    a sequence of tokens for further processing by the parser.

    ex 12+32     will give:    [INT:12, PLUS, INT:32, EOF]
    ex: 12+34/6   will give:    [INT:12, PLUS, INT:34, DIV, INT:6, EOF]

    The lexer go through the text character by character with the module "advance()".
   The module make_tokens() gives the actual list of tokens

   proper way to run:

        fn='<stdin>',
        text=1+2+4
       lexer=Lexer(fn, text)
       tokens,error=lexer.make_tokens()
       if error: return None, error
       print(tokens)

    """

    def __init__(self,fn, text):
        self.fn=fn
        self.text=text
        self.pos=Position(-1,0,-1,fn,text)
        self.current_char=None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char=self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens=[]

        while self.current_char !=None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start=self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start, self.pos,"'"+ char +"'")

        tokens.append(Token(TT_EOF,pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str=''
        dot_count=0
        pos_start=self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count+=1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count==0:
            return Token(TT_INT,int(num_str), pos_start,self.pos)
        else:
            return Token(TT_FLOAT,float(num_str), pos_start,self.pos)

########################################################################
#  NODES
# ######################################################################

# are the basic elements of the abstract syntax tree (AST)  given by the parser

class NumberNode:
    def __init__(self, tok):
        self.tok=tok

        self.pos_start=self.tok.pos_start
        self.pos_end=self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node,op_tok,right_node):
        self.left_node=left_node
        self.op_tok=op_tok
        self.right_node=right_node

        self.pos_start=self.left_node.pos_start
        self.pos_end=self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node},{self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok,node):
        self.op_tok=op_tok
        self.node=node

        self.pos_start=self.op_tok.pos_start
        self.pos_end=self.node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

########################################################################
#  PARSER RESULT
# ######################################################################

class ParseResult:
    """
    Will help in the propagation of the error in the parser
    """
    def __init__(self):
        self.error=None
        self.node=None

    def register(self,res):
        if isinstance(res, ParseResult):
            if res.error: self.error=res.error
            return res.node
        return res

    def success(self,node):
        self.node=node
        return self

    def failure(self,error):
        self.error=error
        return self

########################################################################
#  PARSER
# ######################################################################

class Parser:

        """
        The Parser class is responsible for parsing a sequence of tokens generated by a lexer
        and constructing an abstract syntax tree (AST) from them. This AST represents the
        structure of the input code and is used for further processing such as interpretation
        or compilation.

        The Parser class uses a recursive descent parsing technique to handle the grammar of
        the language. It processes tokens sequentially and builds the AST by recognizing
        various syntactic constructs such as expressions, terms, and factors.
        THe AST will be a set of nodes like:
                    NumberNode for numbers,
                    UnaryOpNode for unitary operations like for -6 will give:  (MINUS, INT:6)
                    or
                    BinOpNode for binary operations like:  1+3.4  will give:   (INT:1,PLUS, FLOAT:3.4)

        You can read all the priority informations of the code in the document grammar.txt

        ex: 12+34/6        will give:    (INT:12,PLUS, (INT:34,DIV, INT:6))
        ex: 1.1/3+23/1.2   will give:    ((FLOAT:1.1,DIV, INT:3),PLUS, (INT:23,DIV, FLOAT:1.2))


        self.tok_idx correspond to the index of token
        advance(self): Moves to the next token in the token list and updates the current token "self.current_tok".

    - parse(self): Initiates the parsing process by calling the expr method


    - factor(self): Parses factors, which are the basic building blocks of expressions.
      Factors can be integers, floats, or expressions enclosed in parentheses. Handles unary
      operators (+ and -) and ensures proper matching of parentheses.

    - term(self): Parses terms, which consist of factors combined with multiplication or
      division operators. Uses the bin_op method to handle binary operations.

    - expr(self): Parses expressions, which consist of terms combined with addition or
      subtraction operators. Uses the bin_op method to handle binary operations.


proper way to run:

    fn='<stdin>',
    text=1+2+4
    lexer=Lexer(fn, text)
    tokens,error=lexer.make_tokens()
    if error: return None, error

    #Generate AST
    parser=Parser(tokens)
    ast= parser.parse()
    if ast.error: return None, ast.error
    print(ast)
    ...



        """


    def __init__(self, tokens):
        self.tokens=tokens
        self.tok_idx=-1
        self.advance()

    def advance(self):
        self.tok_idx +=1
        if self.tok_idx < len(self.tokens):
            self.current_tok=self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res=self.expr()
        if not res.error and self.current_tok.type !=TT_EOF:
            return res.failure(InvalidSyntaxError(
                                self.current_tok.pos_start,self.current_tok.pos_end,
                                "Expected '+', '-', '*' or '/' "
                                ))
        return res

    def factor(self):
        """
        get the next "factor" sequence of tokens
        can be a int (ex "34" or "+4"), a float (ex "-2.3") or any expressions between parenthesis  (ex "(12+5)"  )
        """

        res=ParseResult()
        tok=self.current_tok

        if tok.type in (TT_PLUS,TT_MINUS):
            res.register(self.advance())
            factor= res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok,factor))

        elif tok.type in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr= res.register(self.expr())
            if res.error: return res
            if self.current_tok.type== TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
                        tok.pos_start,tok.pos_end,
                        "Expected int or float"
                                      )
                    )


    def term(self):
        """
        get the next "term" sequence of tokens
        can be any factors separated by * or /  (ex "2 * 5 / (3+4)"  )
        """

        return self.bin_op(self.factor, (TT_MUL,TT_DIV))

    def expr(self):
        """
        get the next "expr" sequence of tokens
        can be any terms or factors separated by + or -  (ex "2 + 5 - 3*4*5"  )
        """

        return self.bin_op(self.term, (TT_PLUS,TT_MINUS))



    def bin_op(self,func ,ops ):
        res=ParseResult()
        left=res.register(func())
        if res.error: return res

        while(self.current_tok.type in ops):

            op_tok= self.current_tok
            res.register(self.advance())
            right=res.register(func())
            if res.error: return res
            left=BinOpNode(left,op_tok,right)

        return res.success(left)

########################################################################
#  RUNTIME RESULT
# ######################################################################

class RTResult:
    """
    Will help in the propagation of the error in the interpretor
    """

    def __init__(self):
        self.value=None
        self.error=None

    def register(self,res):
        if res.error: self.error=res.error
        return res.value

    def success(self,value):
        self.value=value
        return self

    def failure(self,error):
        self.error=error
        return self


########################################################################
#  VALUES
# ######################################################################

class Number:
    """
    will be the results of the propagation through the AST by the interpretor.
    """
    def __init__(self,value):
        self.value=value
        self.set_pos()
        self.set_context()

    def set_pos(self,pos_start=None,pos_end=None):
        self.pos_start=pos_start
        self.pos_end=pos_end
        return self

    def set_context(self,context=None):
        self.context=context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value+other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value-other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value*other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value==0:
                return None,RTError(
                        other.pos_start,other.pos_end, "Division by zero",
                        self.context
                )
            else:
                return Number(self.value/other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


########################################################################
#  CONTEXT
# ######################################################################

class Context:
    def __init__(self,display_name,parent=None,parent_entry_pos=None):
        self.display_name=display_name
        self.parent=parent
        self.parent_entry_pos=parent_entry_pos

########################################################################
#  INTERPRETER
# ######################################################################


class Interpreter:
    """
    The Interpreter class is responsible for interpreting the abstract syntax tree (AST)
    generated by the Parser. It traverses the AST and executes the operations defined in
    the nodes to compute the result of the input expression.

    The Interpreter uses the Visitor pattern to handle different types of nodes in the AST.
    Each type of node has a corresponding visit method that defines how the node should be
    processed. This allows for easy extension and maintenance of the interpreter as new node
    types can be added with their corresponding visit methods.

    Key methods in the Interpreter class include:

    - visit(self, node, context): Dispatches the node to the appropriate visit method based
      on the node's type. This method uses reflection to dynamically call the visit method
      corresponding to the node's class name.

proper way to run:

    fn='<stdin>',
    text=1+2+4
    lexer=Lexer(fn, text)
    tokens,error=lexer.make_tokens()
    if error: return None, error

    #Generate AST
    parser=Parser(tokens)
    ast= parser.parse()
    if ast.error: return None, ast.error

    #Run program
    interpreter=Interpreter()
    context=Context('<program>')
    result=interpreter.visit(ast.node,context)


    """

    def visit(self,node,context):
        method_name=f'visit_{type(node).__name__}'
        method=getattr(self,method_name,self.no_visit_method)
        return method(node,context)

    def no_visit_method(self,node,context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ################################

    def visit_NumberNode(self,node,context):
        return RTResult().success(
                        Number(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
        )


    def visit_BinOpNode(self,node,context):
        res=RTResult()
        left=res.register(self.visit(node.left_node,context))
        if res.error:return res
        right=res.register(self.visit(node.right_node,context))
        if res.error:return res

        if node.op_tok.type== TT_PLUS:
            result,error=left.added_to(right)

        elif node.op_tok.type== TT_MINUS:
            result,error=left.subbed_by(right)

        elif node.op_tok.type== TT_MUL:
            result,error=left.multed_by(right)

        elif node.op_tok.type== TT_DIV:
            result,error=left.dived_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start,node.pos_end))

    def visit_UnaryOpNode(self,node,context):
        res =RTResult()
        number=res.register(self.visit(node.node,context))
        if res.error:return res

        error=None
        if node.op_tok.type== TT_MINUS:
            number,error=number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))


########################################################################
#  RUN
# ######################################################################

def run(fn,text):
    lexer=Lexer(fn, text)
    tokens,error=lexer.make_tokens()
    if error: return None, error

    #Generate AST
    parser=Parser(tokens)
    ast= parser.parse()
    if ast.error: return None, ast.error

    #Run program
    interpreter=Interpreter()
    context=Context('<program>')
    result=interpreter.visit(ast.node,context)

    return result.value,result.error


if __name__ == "__main__":
    """ """
    print("ok")
