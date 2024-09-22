from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating the option to arbitrarily combine operations between layers """

SR = SeqRenderer()

kernel = (16, 16)
SR.add_layer(layers.Layer2D(3, 60, 60, "Input"))
SR.add_operation(
    [
        operations.LinearOp("Transform"),
        operations.ArrowOp(""),
    ]
)
SR.add_layer(
    layers.Layer2D(16, 30, 30, "", limited=8, end_channels=2, skip_ival=1, cspace=5)
)
SR.add_operation(
    [
        operations.LinearOp(""),
        operations.Conv2dOp(),
        operations.ArrowOp(""),
    ]
)
SR.add_layer(
    layers.Layer2D(
        32,
        15,
        15,
        "",
        limited=16,
        end_channels=3,
        skip_ival=3,
        cspace=5,
        limited_radius=3,
    )
)
SR.render(50, ymargin=0.25)
