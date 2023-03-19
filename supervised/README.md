# Supervised Learning

Minesweeper can be seen as a supervised learning game with the inputs of the board with the task of predicitng whether
a given square is a mine or not.

This approach allows for the function approximation of probability of an index being a mine given a square.
To make this algorithm more efficient, obvious mines are precalculated and revealed, and only when a guess has to be
made is the Deep Learning model used.

Revealed bomb indicies are also used.

### Model Analysis and Results

```
Model(
  (layers): Sequential(
    (0): Flatten(start_dim=1, end_dim=-1)
    (1): Linear(in_features=1100, out_features=1024, bias=True)
    (2): LeakyReLU(negative_slope=0.01)
    (3): Linear(in_features=1024, out_features=1024, bias=True)
    (4): LeakyReLU(negative_slope=0.01)
    (5): Linear(in_features=1024, out_features=1024, bias=True)
    (6): LeakyReLU(negative_slope=0.01)
    (7): Linear(in_features=1024, out_features=128, bias=True)
    (8): LeakyReLU(negative_slope=0.01)
    (9): Linear(in_features=128, out_features=2, bias=True)
    (10): LogSoftmax(dim=-1)
  )
)
```

The above configuration of the model is purely a stack of linear layers. 
It seems to converge on an accuracy of 28% during the training phase and achieves a 30% winrate
on a `10x10` board with `20` mines.