from pydrawnet import NetGraph, layers, operations

""" Demonstrating a generic Dense/Linear network with some of the available parameter variations """

NG = NetGraph()
NG.add_layer(
    layers.Layer1D(
        30,
        1,
        "Input with\nlimited features",
        shape_spacing=0.5,
        limited=10,
        limited_radius=0.25,
        end_features=3,
    )
)
NG.add_operation(operations.DenseOp(10, 5, "Dense", limited_ends=3))
NG.add_layer(
    layers.Layer1D(5, 2, "Features", shape_spacing=0.5, fill_color=(0.5, 0.9, 0))
)
NG.add_operation(operations.DenseOp(5, 8, "Dense"))
NG.add_layer(layers.Layer1D(8, 1, "Features", shape_spacing=3, fill_color=(1, 0, 0)))
NG.add_operation(operations.DenseOp(8, 20, "Dense"))
NG.add_layer(layers.Layer1D(20, 1, "Features", shape_spacing=0.5))

NG.render(10, text_y_offset=1)
