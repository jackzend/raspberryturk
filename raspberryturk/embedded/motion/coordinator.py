import numpy as np
import chess
import logging
import time
from raspberryturk.embedded.motion.gripper import Gripper
from raspberryturk.embedded.motion.arm import Arm

# Perform a castle move
def _castling(move, board):
    return move.from_square in [chess.E1, chess.E8] \
           and move.to_square in [chess.C1, chess.G1, chess.C8, chess.G8] \
           and board.piece_at(move.from_square).piece_type == chess.KING

# Converts the square number to an x, y point
def _sq_to_pt(sq):
    i = 63 - sq
    return np.array([i % 8, i / 8]) * 2.25 + 1.125

class Coordinator(object):
    def __init__(self):
        self.gripper = Gripper()    #May need modifying
        self.arm = Arm()
        self._logger = logging.getLogger(__name__)

    def move_piece(self, move, board):
        # Checks if the move is a castle and performs the unique move
        if _castling(move, board):
            a_side = chess.file_index(move.to_square) < chess.file_index(move.from_square)
            from_file_index = 0 if a_side else 7
            to_file_index = 3 if a_side else 5
            rank_index = 0 if board.turn is chess.WHITE else 7
            rook_from_sq = chess.square(from_file_index, rank_index)
            rook_to_sq = chess.square(to_file_index, rank_index)
            self._execute_move(_sq_to_pt(rook_from_sq), \
                               _sq_to_pt(rook_to_sq), \
                               chess.ROOK)
        # If the move is not a castle, then perform a normal move
        else:
            captured_piece = board.piece_at(move.to_square)
            # If there is a piece that needs to be captured, capture piece first
            if captured_piece is not None:
                self._execute_move(_sq_to_pt(move.to_square), [20, 13.5], \
                                   captured_piece.piece_type)
        piece = board.piece_at(move.from_square)
        self._execute_move(_sq_to_pt(move.from_square), \
                           _sq_to_pt(move.to_square), \
                           piece.piece_type)

    # Executes move
    def _execute_move(self, origin, destination, piece_type):
        self._logger.info("Moving piece {} at {} to {}...".format(piece_type, origin, destination))
        t0 = time.time()
        self.arm.move_to_point(origin)
        self.gripper.pickup(piece_type)     #Needs modifying
        self.arm.move_to_point(destination)
        self.gripper.dropoff(piece_type)    #Needs modifying
        self.arm.return_to_rest()
        elapsed_time = time.time() - t0
        self._logger.info("Done moving piece (elapsed time: {}s).".format(elapsed_time))

    def reset(self):
        self.gripper.calibrate()    #Needs modifying
        self.arm.return_to_rest()

    def close(self):
        self.gripper.cleanup()
