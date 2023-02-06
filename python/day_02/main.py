from copy import copy
from enum import Enum
from dataclasses import dataclass


class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class Outcome(Enum):
    LOSS = "loss"
    DRAW = "draw"
    WIN = "win"


@dataclass
class Match:
    opponent_move: Move | None = None
    play: Move | Outcome | None = None

    outcomes = [
        [Move.ROCK, Move.ROCK, Outcome.DRAW],
        [Move.ROCK, Move.PAPER, Outcome.WIN],
        [Move.ROCK, Move.SCISSORS, Outcome.LOSS],
        [Move.PAPER, Move.ROCK, Outcome.LOSS],
        [Move.PAPER, Move.PAPER, Outcome.DRAW],
        [Move.PAPER, Move.SCISSORS, Outcome.WIN],
        [Move.SCISSORS, Move.ROCK, Outcome.WIN],
        [Move.SCISSORS, Move.PAPER, Outcome.LOSS],
        [Move.SCISSORS, Move.SCISSORS, Outcome.DRAW],
    ]

    def calculate_moves(self) -> None:
        if self.play.__class__ is Move:
            self.player_move = self.play
            self.outcome = [
                outcome
                for opponent_move, player_move, outcome in self.outcomes
                if opponent_move is self.opponent_move
                and player_move is self.player_move
            ][0]
        if self.play.__class__ is Outcome:
            self.outcome = self.play
            self.player_move = [
                player_move
                for opponent_move, player_move, outcome in self.outcomes
                if opponent_move is self.opponent_move and outcome is self.outcome
            ][0]

    def score(self) -> int:

        self.calculate_moves()

        match_scores = {Outcome.LOSS: 0, Outcome.DRAW: 3, Outcome.WIN: 6}
        move_scores = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}

        match_score = match_scores[self.outcome]
        move_score = move_scores[self.player_move]

        total_score = match_score + move_score

        return total_score


def convert_play(opponent_play: str, play: str) -> tuple[int, int]:

    match = Match()

    if opponent_play == "A":
        match.opponent_move = Move.ROCK
    if opponent_play == "B":
        match.opponent_move = Move.PAPER
    if opponent_play == "C":
        match.opponent_move = Move.SCISSORS

    match1 = copy(match)
    match2 = copy(match)

    if play == "X":
        match1.play = Move.ROCK
        match2.play = Outcome.LOSS
    if play == "Y":
        match1.play = Move.PAPER
        match2.play = Outcome.DRAW
    if play == "Z":
        match1.play = Move.SCISSORS
        match2.play = Outcome.WIN

    return match1.score(), match2.score()


def main(input_data: str) -> tuple[int, int]:

    # Split on line breaks to sepearate each match
    split_data = input_data.split("\n")

    move_data = [convert_play(*x.split(" ")) for x in split_data]

    return sum(x for x, _ in move_data), sum(y for _, y in move_data)
