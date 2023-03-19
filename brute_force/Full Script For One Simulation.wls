#!/usr/bin/env wolframscript
(* ::Package:: *)

(* Generate a new board with the indicies around the (x,y) not bombs. *)

generate[l_, w_, b_, x_, y_] :=
  Block[{},
    board = ConstantArray[-1, {l, w}];
    indicies = Position[board, -1];
    selectedIndicies = {{x - 1, y - 1}, {x - 1, y}, {x - 1, y + 1}, {
      x, y - 1}, {x, y}, {x, y + 1}, {x + 1, y - 1}, {x + 1, y}, {x + 1, y 
      + 1}};
    indicies = Complement[indicies, selectedIndicies];
    board = ReplacePart[board, RandomSample[indicies, b] -> -100];
    board
  ]

(* Display the board graphically. *)

display[board_] :=
  ArrayPlot[board, ColorRules -> {-100 -> Darker[Red], -99 -> Black, 
    -1 -> White, 0 -> Gray, 1 -> Darker[Gray, 0.1], 2 -> Darker[Gray, 0.2
    ], 3 -> Darker[Gray, 0.3], 4 -> Darker[Gray, 0.4], 5 -> Darker[Gray, 
    0.5], 6 -> Darker[Gray, 0.6], 7 -> Darker[Gray, 0.7], 8 -> Darker[Gray,
     0.8]}, Mesh -> True]

(* Gets the neighbors of the selected square. *)

neighbors[board_, x_, y_] :=
  Return[board[[Max[1, x - 1] ;; Min[Dimensions[board][[1]], x + 1], 
    Max[1, y - 1] ;; Min[Dimensions[board][[2]], y + 1]]]]

(* Reveal a square. *)

reveal[board_, x_, y_] :=
  Block[{l = Dimensions[board][[1]], w = Dimensions[board][[2]], b = 
    board},
    revealSquare[xi_, yi_] :=
      Block[{},
        If[1 <= xi <= l && 1 <= yi <= w && b[[xi, yi]] == -1,
          b[[xi, yi]] = Count[neighbors[b, xi, yi], -100, {2}] + Count[
            neighbors[b, xi, yi], -99, {2}];
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

(* Mark a bomb if it is a bomb. *)

mark[board_, x_, y_] :=
  If[board[[x, y]] == -100,
    b = board;
    b[[x, y]] = -99;
    b
    ,
    board
  ]

(* Check that the game has finished. All safe squares found and all bombs labeled. *)

gameWon[board_] :=
  Count[board, -1, {2}] == 0 && Count[board, -100, {2}] == 0

(* Get the user board. *)

getUserBoard[board_] :=
  board /. -100 -> -1

(* Confirmed safe squares and bombs. *)

confirmed[board_] :=
  Block[{l = Dimensions[board][[1]], w = Dimensions[board][[2]], safe
     = {}, unsafe = {}, selectedPositions = Position[Map[# > 0&, board, {
    2}], True]},
    helper[c_] :=
      (
        x = c[[1]];
        y = c[[2]];
        n = Count[neighbors[board, x, y], -1, {2}];
        b = board[[x, y]] - Count[neighbors[board, x, y], -99, {2}];
        If[b == n,
          unsafe = Union[unsafe, {{x - 1, y - 1}, {x - 1, y}, {x - 1,
             y + 1}, {x, y - 1}, {x, y + 1}, {x + 1, y - 1}, {x + 1, y}, {x + 1, 
            y + 1}}]
        ];
        If[b == 0,
          safe = Union[safe, {{x - 1, y - 1}, {x - 1, y}, {x - 1, y +
             1}, {x, y - 1}, {x, y + 1}, {x + 1, y - 1}, {x + 1, y}, {x + 1, y + 
            1}}]
        ];
      );
    Map[helper, selectedPositions];
    safe = DeleteDuplicates[Cases[safe, {x_, y_} /; 1 <= x <= l && 1 
      <= y <= w && board[[x, y]] == -1]];
    unsafe = DeleteDuplicates[Cases[unsafe, {x_, y_} /; 1 <= x <= l &&
       1 <= y <= w && board[[x, y]] == -1]];
    Return[{safe, unsafe}]
  ]

(* Selectable squares, AKA ones that have numbers greater than 0. *)

selectableSquares[board_] :=
  (
    toChoose = ConstantArray[0, Dimensions[board]];
    l = Dimensions[board][[1]];
    w = Dimensions[board][[2]];
    neighborIndex[idx_] := (ContainsAny[neighbors[board, idx[[1]], idx
      [[2]]], {-99, -1}]);
    nearest[idx_] :=
      (
        x = idx[[1]];
        y = idx[[2]];
        {{x - 1, y - 1}, {x - 1, y}, {x - 1, y + 1}, {x, y - 1}, {x, 
          y + 1}, {x + 1, y - 1}, {x + 1, y}, {x + 1, y + 1}}
      );
    selectedPositions = Position[Map[# > 0&, board, {2}], True];
    n = Map[nearest, selectedPositions];
    n = ArrayReshape[n, {Dimensions[n][[1]] * Dimensions[n][[2]], 2}]
      ;
    n = DeleteDuplicates[Cases[n, {x_, y_} /; (1 <= x <= l && 1 <= y 
      <= w && board[[x, y]] == -1)]];
    n
  )

(* Get squares for the very next layer that are possible. *)

validLocations[board_] :=
  Block[{},
    locations = selectableSquares[board];
    isValid[possibleLocation_] :=
      (
        b = ReplacePart[board, Thread[Rule[locations, possibleLocation
          ]]];
        isValidHelper[idx_] :=
          (
            x = idx[[1]];
            y = idx[[2]];
            Count[neighbors[b, x, y], -100, {2}] + Count[neighbors[b,
               x, y], -99, {2}] == b[[x, y]]
          );
        AllTrue[Position[Map[# > 0&, b, {2}], True], isValidHelper]
      );
    possibleLocations = Position[DynamicMap[isValid, Tuples[{-99, -1}, Length[
      locations]]], True];
    possibleLocations = ArrayReshape[possibleLocations, {Dimensions[possibleLocations
      ][[1]]}];
    Tuples[{-99, -1}, Length[locations]][[possibleLocations]]
  ]

(* Get the best choices of safe squares and bombs. *)

calculateBestChoice[board_] :=
  Block[{},
    selectable = selectableSquares[board];
    possibleLocations = validLocations[board];
    probabilities = Total[possibleLocations /. {-99 -> 0, -1 -> 1}, {1}
      ] / Length[possibleLocations];
    maxProb = Position[probabilities, Max[probabilities]];
    positions = Position[probabilities, Max[probabilities]];
    topRevealChoices = selectable[[ArrayReshape[positions, {Dimensions[
      positions][[1]]}]]];
    bombPositions = Position[probabilities, 0];
    bombs = selectable[[ArrayReshape[bombPositions, {Dimensions[bombPositions
      ][[1]]}]]];
    bombs = {};
    Return[{topRevealChoices, Max[probabilities], bombs}];
  ]

board = generate[20, 20, 80, 2, 2];

gameRunning = True;

history = {display[getUserBoard[board]]};

board = reveal[board, 2, 2];

display[board]

moves = 0;

While[gameRunning || !gameWon[board],
         (* Mark all the bombs and safe squares until there are only 
    
    guesses
     that can be made. *)
  moves += 1;
  Print[moves];
  output = confirmed[getUserBoard[board]];
  safe = output[[1]];
  unsafe = output[[2]];
  While[
    (Length[safe] != 0 || Length[unsafe] != 0) && !gameWon[board]
    ,
    For[i = 1, i <= Length[safe], i++,
      c = safe[[i]];
      x = c[[1]];
      y = c[[2]];
      board = reveal[board, x, y];
      history = Append[history, display[board]];
    ];
    For[i = 1, i <= Length[unsafe], i++,
      c = unsafe[[i]];
      x = c[[1]];
      y = c[[2]];
      board = mark[board, x, y];
      history = Append[history, display[board]];
    ];
    output = confirmed[getUserBoard[board]];
    safe = output[[1]];
    unsafe = output[[2]];
  ];
  output = calculateBestChoice[getUserBoard[board]];
  topGuesses = output[[1]];
  prob = output[[2]];
  bombs = output[[3]];
  For[i = 1, i <= Length[bombs], i++,
    topGuess = bombs[[i]];
    x = topGuess[[1]];
    y = topGuess[[2]];
    If[board[[x, y]] != -100,
      gameRunning = False
    ];
    board = mark[board, x, y];
    history = Append[history, display[board]];
  ];
  If[prob == 1,
    For[i = 1, i <= Length[topGuesses], i++,
      topGuess = topGuesses[[i]];
      x = topGuess[[1]];
      y = topGuess[[2]];
      board = reveal[board, x, y];
      history = Append[history, display[board]];
    ]
    ,
    topGuess = topGuesses[[1]];
    x = topGuess[[1]];
    y = topGuess[[2]];
    If[board[[x, y]] == -100,
      gameRunning = False
    ];
    board = reveal[board, x, y];
    history = Append[history, display[board]];
  ];
  Print[MatrixForm[board]];
  If[gameWon[board],gameRunning=False];
]

gameRunning
Export["game.gif",history]

