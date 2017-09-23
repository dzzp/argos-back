from __future__ import division
import os
import av
import skvideo.io

#from video.models import Video
#from video.calculation import NumericStringParser

from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator

__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''


class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example
    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val




class FrameWorker:
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ) + '/assets/'

    def __init__(self, *arg):
        if arg:
            self.video = arg[0]
        else:
            self.video = ''
        self.running_time = 0
        self.frame = 0

    def extract_video_info(self, *arg):
        if arg:
            self.video = arg[0]
        
        metadata = skvideo.io.ffprobe(self.video)

        # fps
        self.frame = self.calculate_video_frame(
            metadata['video']['@r_frame_rate']
        )
        self.running_time = metadata['video']['@duration']    # duration

    def calculate_video_frame(self, data):
        num_str_parser = NumericStringParser()
        result = num_str_parser.eval(data)

        return result

    def extract_video_frame(self, interval, *arg):
        if arg:
            self.video = arg[0]
        
        container = av.open(self.video)
        pass_count = 0

        #folder_name = os.path.splitext(os.path.basename(self.video))[0]
        #full_path = self.BASE_DIR + folder_name
        full_path = self.BASE_DIR + 'google'
        
        try:
            os.mkdir(full_path)
        except:
            print('Folder already exists..')

        for frame in container.decode(video=0):
            if pass_count % interval == 0:
                frame.to_image().save(
                    full_path + '/%d.jpeg' % frame.index
                )
            pass_count += 1
            print(frame)
        

    def cut_video(self, start, end, *arg):
        pass

    def save_video_info(self, *arg):
        if arg:
            self.video = arg[0]
        '''
        info = Video.objects.get(video=self.video)
        info.frame = self.frame
        info.running_time = self.running_time
        info.save()
        '''
        Video.objects.create(
            video_path=self.video,
            frame=self.frame,
            running_time=self.running_time
        )

    # for testing
    def extract_random_frame(self, *arg):
        pass

    def new_extract_video_frame(self, *arg):
        if arg:
            self.video = arg[0]

        inputdict = {}
        outputdict = {}
        reader = skvideo.io.FFmpegReader(
            self.video,
            inputdict=inputdict,
            outputdict=outputdict
        )

        i = 0
        for frame in reader.nextFrame():
            i += 1
        print(i)


frametovideo = FrameWorker('/home/punk/dev/data_picker/assets/test.mp4')
#frametovideo.extract_video_frame(30)
frametovideo.new_extract_video_frame()
