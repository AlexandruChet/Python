import chess
import chess.engine

class ChessAnalyzer:
    def __init__(self, engine_path):
        self.engine_path = engine_path
        self.board = chess.Board()

    def load_moves(self):
        moves_input = input("Enter a list of moves (eg 'e4 e5 Nf3'): ")
        self.board = chess.Board()
        for move in moves_input.split():
            try:
                self.board.push_san(move)
            except ValueError:
                print(f"Incorrect move: {move}")

    def run_stockfish_analysis(self, time_limit=0.1):
        try:
            with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
                result = engine.play(self.board, chess.engine.Limit(time=time_limit))
                
                info = engine.analyse(self.board, chess.engine.Limit(time=time_limit))
                score = info["score"].relative.score(mate_score=10000)
                best_move = info["pv"][0] if "pv" in info else None
                
                print(f"Current position (FEN): {self.board.fen()}")
                print(f"Best Move: {best_move}")
                print(f"Position rating: {score / 100.0 if score is not None else 'N/A'} pawns")
                
        except FileNotFoundError:
            print(f"The engine was not found on the way {self.engine_path}")
            
        except Exception as e:
            print(f"Error: {e}")