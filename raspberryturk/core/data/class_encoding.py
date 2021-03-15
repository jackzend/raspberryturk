#Creates new dictionary with mapped chess symbols
def _symbols_dict(symbols):
    return dict(zip(symbols, range(len(symbols))))

#Creates 5 new "symbols dicts" for different piece combinations
_COLOR_PIECE_SYMBOLS = _symbols_dict(['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K', None])
_COLOR_PIECE_SYMBOLS_NOEMPTY = _symbols_dict(['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K'])
_PIECE_SYMBOLS = _symbols_dict(['p', 'n', 'b', 'r', 'q', 'k', None])
_PIECE_SYMBOLS_NOEMPTY = _symbols_dict(['p', 'n', 'b', 'r', 'q', 'k'])
_PROMOTABLE_PIECE_SYMBOLS = _symbols_dict(['n', 'b', 'r', 'q'])

#Checks if piece symbol is empty
def _is_empty(piece_symbol):
    return piece_symbol == 'e' or piece_symbol is None

def _num_classes(n):
    def _num_classes_decorator(func):
        func.num_classes = n
        return func
    return _num_classes_decorator

#Looks up piece symbol in symbol dictionary
def _dict_lookup(symbols_dict, piece_symbol):
    return symbols_dict.get(piece_symbol, -1)

#Decorator functionality for if n = 2
@_num_classes(2)
def empty_or_not(piece_symbol):
    return int(_is_empty(piece_symbol))

#Decorator functionality for if n = 3
@_num_classes(3)
def white_or_black(piece_symbol):
    #piece_symbol is empty
    if piece_symbol == 'e':
        piece_symbol = None
    #piece_symbol is not in the dictionary
    if piece_symbol not in _COLOR_PIECE_SYMBOLS.keys():
        return -1
    else:
        if piece_symbol is None:
            return 0
        else:
            return int(not piece_symbol.islower()) + 1

#Decorator functionality for if n = 2
@_num_classes(2)
def white_or_black_noempty(piece_symbol):
    if piece_symbol not in _COLOR_PIECE_SYMBOLS_NOEMPTY.keys():
        return -1
    else:
        return int(not piece_symbol.islower())

#Decorator for number of different colored pieces on board
@_num_classes(len(_COLOR_PIECE_SYMBOLS.keys()))
def color_piece(piece_symbol):
    return _dict_lookup(_COLOR_PIECE_SYMBOLS, piece_symbol)

#Decorator for number of different colored pieces on board without empties
@_num_classes(len(_COLOR_PIECE_SYMBOLS_NOEMPTY.keys()))
def color_piece_noempty(piece_symbol):
    return _dict_lookup(_COLOR_PIECE_SYMBOLS_NOEMPTY, piece_symbol)

#Decorator for number of piece symbols
@_num_classes(len(_PIECE_SYMBOLS.keys()))
def piece(piece_symbol):
    return _dict_lookup(_PIECE_SYMBOLS, piece_symbol)

#Decorator for number of piece symbols without empties
@_num_classes(len(_PIECE_SYMBOLS_NOEMPTY.keys()))
def piece_noempty(piece_symbol):
    return _dict_lookup(_PIECE_SYMBOLS_NOEMPTY, piece_symbol)

#Number of piece symbols on board that can be promoted
@_num_classes(len(_PROMOTABLE_PIECE_SYMBOLS.keys()))
def promotable_piece(piece_symbol):
    return _dict_lookup(_PROMOTABLE_PIECE_SYMBOLS, piece_symbol)

ENCODING_FUNCTIONS = [empty_or_not, white_or_black, color_piece, color_piece_noempty, piece, piece_noempty, promotable_piece]
