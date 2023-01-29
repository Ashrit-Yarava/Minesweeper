#!/usr/bin/env wolframscript
(* ::Package:: *)

(* BOARD FUNCTIONS *)

(*-----------------------------------------------------------------------------*)

generateBoard[l_, w_, b_] :=
    Return[ArrayReshape[ReplacePart[ConstantArray[-1, {l * w}], ArrayReshape[
        RandomSample[Range[l * w], b], {b, 1}] -> -100], {l, w}]]

reveal[board_, x_, y_] :=
    Block[{l = Dimensions[board][[1]], w = Dimensions[board][[2]], b 
        = board},
        revealSquare[xi_, yi_] :=
            Block[{},
                If[1 <= xi <= l && 1 <= yi <= w && b[[xi, yi]] == -1,
                    
                    b[[xi, yi]] = Count[neighbors[b, xi, yi], -100, 2
                        ];
                    If[b[[xi, yi]] == 0,
                        revealSquare[xi - 1, yi - 1];
                        revealSquare[xi - 1, yi];
                        revealSquare[xi - 1, yi + 1];
                        revealSquare[xi, yi - 1];
                        revealSquare[xi, yi + 1];
                        revealSquare[xi + 1, yi - 1];
                        revealSquare[xi + 1, yi];
                        revealSquare[xi + 1, yi + 1];
                    ]
                ];
            ];
        revealSquare[x, y];
        Return[b];
    ]

(* Utility function to display a board with colors. *)

display[board_] :=
    Block[{color = Gray},
        ArrayPlot[board, ColorRules -> {-100 -> Black, -1 -> White, 0
             -> color, 1 -> Darker[color, 0.1], 2 -> Darker[color, 0.2], 3 -> Darker[
            color, 0.3], 4 -> Darker[color, 0.4], 5 -> Darker[color, 0.5], 6 -> Darker[
            color, 0.6], 7 -> Darker[color, 0.7], 8 -> Darker[color, 0.8]}]
    ]

neighbors[board_, x_, y_] :=
    (
        l = Dimensions[board][[1]];
        w = Dimensions[board][[2]];
        Return[board[[Max[1, x - 1] ;; Min[l, x + 1], Max[1, y - 1] ;;
             Min[w, y + 1]]]]
    )

(*-----------------------------------------------------------------------------*)

(* Solver Functions *)

(*-----------------------------------------------------------------------------*)

(* Get a list of all the squares that are viable for the next turn. *)

selectableSquares[board_] :=
    (
        toChoose = ConstantArray[0, Dimensions[board]];
        l = Dimensions[board][[1]];
        w = Dimensions[board][[2]];
        neighborIndex[idx_] := (ContainsAny[neighbors[board, idx[[1]],
             idx[[2]]], {-100, -1}]);
        nearest[idx_] :=
            (
                x = idx[[1]];
                y = idx[[2]];
                {{x - 1, y - 1}, {x - 1, y}, {x - 1, y + 1}, {x, y - 
                    1}, {x, y + 1}, {x + 1, y - 1}, {x + 1, y}, {x + 1, y + 1}}
            );
        selectedPositions = Position[Map[# > 0&, board, {2}], True];
        n = Map[nearest, selectedPositions];
        n = ArrayReshape[n, {Dimensions[n][[1]] * Dimensions[n][[2]],
             2}];
        DeleteDuplicates[Cases[n, {x_, y_} /; (1 <= x <= l && 1 <= y 
            <= w && board[[x, y]] < 0)]]
    )

(* Check if a given board is valid or not. *)

isValid[board_]:=Block[
{results},
isValidHelper[idx_]:=(x=idx[[1]];y=idx[[2]];Count[neighbors[board,x,y],-100, {2}]==board[[x,y]]);
results=AllTrue[Position[Map[#>0&,board,{2}], True],isValidHelper];
results
]

(* Find valid combinations of bombs. *)

findValidPositions[board_, possibleBombs_, updateIndicies_] :=
    Block[{validLocations = {}, b},
        For[i = 1, i <= Length[possibleBombs], i++,
            b = ReplacePart[board, Thread[Rule[updateIndicies, possibleBombs
                [[i]]]]];
            If[isValid[b],
                validLocations = Append[validLocations, possibleBombs
                    [[i]]];
            ]
        ];
        validLocations
    ]

(* Extrapolate the probabilities of each of the squares based on frequency. *)

makeGuess[board_] :=
    Block[{selectable, possibleBombs, validBombs, probability, maxProb,
         bestChoices},
        selectable = selectableSquares[board];
        possibleBombs = Tuples[{-100, -1}, Length[selectable]];
        validBombs = findValidPositions[board, possibleBombs, selectable
            ] /. {-100 -> 0, -1 -> 1};
        probability = Total[validBombs, {1}] / Length[validBombs];
        maxProb = Max[probability];
        bestChoices = selectable[[ArrayReshape[Position[probability, 
            maxProb], {Length[Position[probability, maxProb]]}]]];
        {bestChoices, maxProb}
    ]


board :=
    generateBoard[6, 6, 7];

gameRunning = True;
moveCount=1;

board = reveal[board, 3, 3];
history = {};
display[board]


While[
    gameRunning && Count[board, -1, 2] != 0
    ,
    Print[moveCount];
    output = makeGuess[board];
    guesses = output[[1]];
    probability = output[[2]];
    If[probability == 1,
        For[i = 1, i <= Length[guesses], i++,
            guess = guesses[[i]];
            board = reveal[board, guess[[1]], guess[[2]]];
        ]
        ,
        guess = RandomSample[guesses, 1][[1]];
        Print[guess];
        If[board[[guess[[1]], guess[[2]]]] == -100 || !gameRunning,
            gameRunning = False;
            ,
            board = reveal[board, guess[[1]], guess[[2]]];
        ];
    ];
    graphic = display[board];
    history = Append[history, graphic];
    moveCount++;
]


SetDirectory["~/Desktop/Minesweeper/"];
Export["game.gif",history];


display[board]
