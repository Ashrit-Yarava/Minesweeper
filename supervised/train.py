import torch
import torch.nn as nn
import numpy as np

from supervised.generate_batch import generate_batch
from supervised.model import Model


SHAPE = (20, 20)
LEARNING_RATE = 1e-4
EPOCHS = 100
BATCH_SIZE = 32


def one_hot(x, label_count):
    batch_size = x.shape[0]
    x_hat = torch.zeros((batch_size, label_count))
    x_hat[torch.arange(batch_size), x] = 1
    return x_hat


def training_step(batch_size, model, optimizer):
    batch, labels = generate_batch(batch_size, model)
    predictions = model(batch)
    # print(torch.argmax(predictions, dim=-1))
    # print(labels)
    loss = nn.CrossEntropyLoss(reduction="sum")(predictions, labels.squeeze(-1).long())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    accuracy = torch.mean((torch.argmax(predictions, dim=-1) == labels).float())
    return loss.item(), accuracy.item()


if __name__ == "__main__":
    model = Model()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    acc = []

    for epoch in range(EPOCHS):
        loss, accuracy = training_step(BATCH_SIZE, model, optimizer)
        acc.append(accuracy)

        print(f"Epoch {epoch}:\t {round(loss, 4)}, \t{accuracy * 100}%\t\t - \t\t{round(np.mean(np.array(acc)[-100:]) * 100, 2)}%")

    torch.save(model.state_dict(), "checkpoints/state_dict.pt")