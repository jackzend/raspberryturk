from raspberryturk import lib_path
#from raspberryturk.core.vision.helpers import possible_moves_for_board, \
                                              #pawn_board_from_colored_board_mask
from raspberryturk.core.game.stockfish_player import StockfishPlayer
from raspberryturk.embedded import game
#from raspberryturk.embedded.vision.chess_camera import ChessCamera
from raspberryturk.embedded.motion.coordinator import Coordinator

import io
import chess
import time
import logging

NUM_REQUIRED_MATCHING_CANDIDATES = 2

class Agent(object): # UNCOMMENT MOTION STUFF WHEN WE HAVE MOTION
    def __init__(self):
        #self._chess_camera = ChessCamera()
        self._motion_coordinator = None
        self._logger = logging.getLogger(__name__)
        self._player = StockfishPlayer()

    def __enter__(self):
        #self._motion_coordinator = Coordinator() # removing motion for now
        #self._motion_coordinator.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #self._motion_coordinator.close()
        self._motion_coordinator = None
        return False

    #def _candidate_move(self):
    #    cbm = self._chess_camera.current_colored_board_mask() # this is the current board state from camera
    #    b = game.get_board() # this is the last "known" board state ie prior to human move
    #    moves = possible_moves_for_board(b, cbm) # this returns the most likely move the human made
    #    return moves[0] if moves else None # return the human move

    def _next_move(self): # this is wear the turk determines the move the player makes IE Where we spoof!!
        # Spoof code
        user_move = raw_input("Please Play a Legal Chess Move and Input as UCI String:")
        ret_move = chess.Move.from_uci(user_move)
        return ret_move

        #candidates = []
        #for i in range(NUM_REQUIRED_MATCHING_CANDIDATES): # double check the move with the camera
        #    candidates.append(self._candidate_move())
        #    time.sleep(2)
        #return candidates[0] if len(set(candidates)) == 1 else None # only return if the camera returns the same move twice

    def _write_status(self):
        b = game.get_board()
        #cbm = self._chess_camera.current_colored_board_mask()
        #cbm_board = pawn_board_from_colored_board_mask(cbm)
        cbm_board = b
        pgn = game.pgn()
        formatted_datetime = time.strftime("%x %X")
        text = unicode("\n\n").join([formatted_datetime, unicode(cbm_board), unicode(b), pgn])
        with io.open(lib_path('status.txt'), 'w', encoding='utf8') as f:
            f.write(text)

    def perception_action_sequence(self):
        b = game.get_board()

        if b.is_game_over():
            self._logger.info("Game has ended, result: {}".format(b.result()))
            return False
            game.start_new_game()
        elif b.turn == chess.WHITE: # this is the players move so the camera has to pick up the difference
            print("Legal Moves: ")
            printt = []
            for move in b.legal_moves:
                printt.append(move.uci())
            print(printt)
            m = self._next_move() # we spoof the next move function with user input
            if m is not None: # we make sure the move is not a null move (it isnt)
                game.apply_move(m) # apply the move
        else: # this is the turks move
            m = self._player.select_move(b) # select move from stockfish
            #self._motion_coordinator.move_piece(m, b) # move the piece # uncomment this to move
            game.apply_move(m)
        self._write_status() # update to status.txt
        return True
