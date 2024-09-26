from pydrawnet.renderers import FreeformRenderer
from pydrawnet import layers, operations

""" Demonstrating residual operations using the Freeform Renderer """

FR = FreeformRenderer()

arrow_size = 5
hival = 120

X = 0
FR.add_layer(layers.Layer2D(4), "A")
X += hival + 40
FR.add_layer(layers.BlockLayer(X=X), "B")
X += hival
FR.add_layer(layers.BlockLayer(X=X), "C")
X += hival
FR.add_layer(layers.BlockLayer(X=X), "D")
X += hival
FR.add_layer(layers.BlockLayer(X=X), "E")

FR.add_operation(
    operations.ArrowOp("", arrow_size=arrow_size, arrow_offset=8), "A", "B"
)
FR.add_operation(
    operations.ArrowOp("", arrow_size=arrow_size, arrow_offset=3), "B", "C"
)
FR.add_operation(
    operations.ArrowOp("", arrow_size=arrow_size, arrow_offset=3), "C", "D"
)
FR.add_operation(
    operations.ArrowOp("", arrow_size=arrow_size, arrow_offset=3), "D", "E"
)

FR.add_operation(
    operations.ResidualOp(
        "", yoffset=-60, xoffset=15, arrow_size=arrow_size, connection_radius=2
    ),
    "A",
    "C",
)
FR.add_operation(
    operations.ResidualOp(
        "", yoffset=-70, xoffset=15, arrow_size=arrow_size, connection_radius=2
    ),
    "A",
    "D",
)
FR.add_operation(
    operations.ResidualOp(
        "", yoffset=-80, xoffset=15, arrow_size=arrow_size, connection_radius=2
    ),
    "A",
    "E",
)

FR.render()
