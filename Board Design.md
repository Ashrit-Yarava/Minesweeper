# Board Design

* Generate board with randomly placed bombs.

```mathematica
generateBoard[l_, w_, b_] :=
 Return[ArrayReshape[
   ReplacePart[ConstantArray[-1, {l*w}],
   	ArrayReshape[RandomSample[Range[l*w], b], {b, 1}] -> -100], 
   {l, w}]]
```

* Neighbors of a given square.

```mathematica
neighbors[board_, x_, y_] := (
  l = Dimensions[board][[1]];
  w = Dimensions[board][[2]];
  Return[
   board[[Max[1, x - 1] ;; Min[l, x + 1], 
     Max[1, y - 1] ;; Min[w, y + 1]]]]
	)
```

* Display a board using colors

```mathematica
display[board_] := 
 Block[{color = Gray}, 
  ArrayPlot[board, 
   ColorRules -> {-100 -> Black, -1 -> White, 0 -> color, 
     1 -> Darker[color, 0.1],
     2 -> Darker[color, 0.2], 3 -> Darker[color, 0.3], 
     4 -> Darker[color, 0.4], 5 -> Darker[color, 0.5],
     6 -> Darker[color, 0.6], 7 -> Darker[color, 0.7], 
     8 -> Darker[color, 0.8]},]]
```

* Reveal the current square and adjacent squares if the number is zero.
* 