from pydrawnet.renderers import FreeformRenderer, SeqRenderer
from pydrawnet import layers, operations

import matplotlib.pyplot as plt

""" Demonstrating multiple networks using a pre-defined plot """

fig, ax = plt.subplots(2, 1)
axs = fig.axes

### PART 1

FR = FreeformRenderer(axs[0])
arrow_size = 3
hival = 25

labels = [
    "Input",
    "Reflection\nPad2d",
    "Conv2d",
    "Instance\nNorm2d",
    "RelU",
    "Reflection\nPad2d",
    "Conv2d",
    "Instance\nNorm2d",
    "Output",
]

colors = [
    (0, 0.5, 0.5),
    (0, 0.7, 0),
    (0.7, 0, 0.7),
    (0, 0.7, 0),
    (0.8, 0.8, 0.8),
    (0, 0.7, 0),
    (0.7, 0, 0.7),
    (0, 0.7, 0),
    (0, 0.5, 0.5),
]

abet = "ABCDEFGHIJKLMNOPQRSTUVQXYZ"

X = 0
for i, L in enumerate(labels):
    FR.add_layer(layers.BlockLayer(10, 50, X=X, label=L, fill_color=colors[i]), abet[i])
    X += hival
    if i > 0 and i < len(labels) - 2:
        FR.add_operation(
            operations.ArrowOp("", arrow_size=arrow_size), abet[i], abet[i + 1]
        )

FR.add_operation(operations.ArrowOp("", arrow_size=0), "A", "B")

FR.add_operation(
    operations.ResidualOp("", yoffset=-35, xoffset=7.5, arrow_size=arrow_size),
    "A",
    "I",
)

FR.add_operation(
    operations.CircleOp("", diameter=6, symbol_kwargs={"weight": "bold"}), "H", "I"
)

FR.render(text_y_offset=5, show=False)

### PART 2

SR = SeqRenderer(axs[1])

labels = [
    "Conv2d",
    "Instance\nNorm2d",
    "RelU",
]

colors = [
    (0.7, 0, 0.7),
    (0, 0.7, 0),
    (0.8, 0.8, 0.8),
]

for i, L in enumerate(labels):
    SR.add_layer(layers.BlockLayer(10, 50, label=L, fill_color=colors[i]))
    if i < len(labels) - 1:
        SR.add_operation(operations.ArrowOp("", 5))

SR.render(20)
