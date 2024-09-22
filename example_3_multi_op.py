from pydrawnet import NetGraph, layers, operations

""" Demonstrating the option to arbitrarily combine operations between layers """

NG = NetGraph()

kernel = (16, 16)
NG.add_layer(layers.Layer2D(3, 60, 60, "Input"))
NG.add_operation(
    [
        operations.LinearOp("Transform"),
        operations.ArrowOp(""),
    ]
)
NG.add_layer(
    layers.Layer2D(16, 30, 30, "", limited=8, end_channels=2, skip_ival=1, cspace=5)
)
NG.add_operation(
    [
        operations.LinearOp(""),
        operations.Conv2dOp(),
        operations.ArrowOp(""),
    ]
)
NG.add_layer(
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
NG.render(50, ymargin=0.25)
