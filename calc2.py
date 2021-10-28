
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, DIVIDE, MULTIPLY, EOF = 'INTEGER', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', '-', '/', '*' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        
        # self.pos is an index into self.text
        self.pos = 0
        
        # current token instance
        self.current_token = None
        
        #current character by position in the input stream
        self.current_char = self.text[self.pos]
        #print("Length of input string: " + str(len(self.text)))
        
    def error(self):
        raise Exception('Error parsing input')

    def lastcharacter(self):
        if (self.pos) > (len(self.text)-1):
            #print("Last character position: " + str(self.pos))
            return True
        else:
            return False
    
    def nextchar(self):
        #print("Current characterposition: " + str(self.pos))
        if self.pos >= (len(self.text) - 1):
            self.current_char = None  # Indicates end of input
        else:
            self.pos += 1
            #print("Next character position: " + str(self.pos))
            self.current_char = self.text[self.pos]
            
    def getnumber(self):
        number = ""
        while self.current_char is not None:
            if self.current_char.isdigit():
                number+=self.current_char
                self.nextchar()
            else:
                break
        #print("Get number: " + str(number))
        return number
                
    def nextspace(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.nextchar()
            else:
                break;
       # print("Next space (last) position: " + str(self.pos))
                
    def get_next_token(self):
        number = ""
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        #text = self.text
        self.nextspace()
        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.lastcharacter():
            return Token(EOF, None)
        
        # get a character at the position self.pos and decide
        # what token to create based on the single character
        #self.current_char = self.text[self.pos]
                
        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        
        number = self.getnumber()
        if number.isdigit():
            token = Token(INTEGER, number)
            return token
            
        if self.current_char == '+':
            token = Token(PLUS, self.current_char)
            self.nextchar()
            return token
            
        if self.current_char == '-':
            token = Token(MINUS, self.current_char)
            self.nextchar()
            return token
            
        if self.current_char == '/':
            token = Token(DIVIDE, self.current_char)
            self.nextchar()
            return token

        if self.current_char == '*':
            token = Token(MULTIPLY, self.current_char)
            self.nextchar()
            return token
            
        #self.error()
        return Token(EOF, None)

        
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        result = ""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        
        left = self.current_token
        self.eat(left.type)
        #print("Left element value:" + str(left.value))
        
        op = self.current_token
        self.eat(op.type)
        #print("Operator value: " + str(op.value))
        
        right = self.current_token
        self.eat(right.type)
        #print("Last right element: " + str(right.value))
        
        if (op.type == PLUS):
            result = int(left.value) + int(right.value) # eval(left.value + op.value + right.value) #
            
        if (op.type == MINUS):
            result = int(left.value) - int(right.value) # eval(left.value + op.value + right.value) #

        if (op.type == DIVIDE):
            if(right.value == '0'):
                print("Divide by zero not allowed")
                result = None
            else:
                result = int(left.value)/int(right.value)
                
        if (op.type == MULTIPLY):
            result = int(left.value) * int(right.value) # eval(left.value + op.value + right.value) #
        
        return result
            
def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
