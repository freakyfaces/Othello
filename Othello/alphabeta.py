import numpy as np

from player import Player


class AlphaBetaPlayer(Player):

    @staticmethod
    def is_move_valid(board, player_number, i, j):
        if i < 0 or j < 0 or i >= len(board) or j >= len(board) or board[i][j] != -1:
            return False
        for row_coeff in range(-1, 2):
            for column_coeff in range(-1, 2):
                k = 1
                row = i + row_coeff * k
                column = j + column_coeff * k
                is_valid = False
                while 0 <= row < len(board) and 0 <= column < len(board) and board[row][column] != -1:
                    if board[row][column] == player_number:
                        if is_valid:
                            return True
                        break
                    is_valid = True
                    k += 1
                    row = i + row_coeff * k
                    column = j + column_coeff * k
        return False

    def get_possible_moves(self, board, player_num):
        moves = set()
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                if self.is_move_valid(board, player_num, i, j):
                    moves.update([(i, j)])
        return moves

    def get_next_move(self):
        final_move = None
        best = -1e9
        depth = 4
        for move in self.get_possible_moves(self.board.get_board_grid(), self.player_number):
            self.board.start_imagination()
            self.board.imagine_placing_piece(self.player_number, move[0], move[1])
            score = self.min_alpha_beta(self.board.imaginary_board_grid, abs((self.player_number - 1) // 1), depth - 1,
                                        -1e9, 1e9)
            if score > best:
                best = score
                final_move = move
        return final_move

    def min_alpha_beta(self, given_board, player_num, depth, alpha, beta):
        if depth > 0:
            bestScore = 1e9
            for move in self.get_possible_moves(given_board, player_num):
                newBoard = np.copy(given_board)
                newBoard[move[0]][move[1]] = player_num
                score = self.max_alpha_beta(newBoard, abs((player_num - 1) // 1), depth - 1, alpha, beta)
                bestScore = min(score, bestScore)
                if bestScore <= alpha:
                    return bestScore
                beta = min(beta, bestScore)
            return bestScore
        return self.board_score(given_board, self.player_number)

    def max_alpha_beta(self, given_board, player_num, depth, alpha, beta):
        if depth > 0:
            bestScore = -1e9
            for move in self.get_possible_moves(given_board, player_num):
                new_board = np.copy(given_board)
                new_board[move[0]][move[1]] = player_num
                score = self.min_alpha_beta(new_board, abs((player_num - 1) // 1), depth - 1, alpha, beta)
                bestScore = max(score, bestScore)
                if bestScore >= beta:
                    return bestScore
                alpha = max(alpha, bestScore)
            return bestScore
        return self.board_score(given_board, self.player_number)

    @staticmethod
    def board_score(given_board, player_num):
        weights = [[5, -3, 2, 2, 2, 2, -3, 5],
                   [-3, -5, -1, -1, -1, -1, -5, -3],
                   [2, -1, 1, 0, 0, 1, -1, 2],
                   [2, -1, 0, 1, 1, 0, -1, 2],
                   [2, -1, 0, 1, 1, 0, -1, 2],
                   [2, -1, 1, 0, 0, 1, -1, 2],
                   [-3, -5, -1, -1, -1, -1, -5, -3],
                   [5, -3, 2, 2, 2, 2, -3, 5]]
        score = 0
        count = [0, 0]

        for i in range(0, 8):
            for j in range(0, 8):
                if given_board[i][j] == 0:
                    count[0] += 1
                elif given_board[i][j] == 1:
                    count[1] += 1
                if given_board[i][j] == player_num:
                    score += weights[i][j]
                elif given_board[i][j] == abs((player_num - 1) // 1):
                    score -= weights[i][j]

        if player_num == 0:
            count = count[0] - count[1]
        else:
            count = count[1] - count[0]

        return 2 * count + score
