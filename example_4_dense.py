from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating a generic Dense/Linear network with some of the available parameter variations """

SR = SeqRenderer()
SR.add_layer(
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
SR.add_operation(operations.DenseOp(10, 5, "Dense", limited_ends=3))
SR.add_layer(
    layers.Layer1D(5, 2, "Features", shape_spacing=0.5, fill_color=(0.5, 0.9, 0))
)
SR.add_operation(operations.DenseOp(5, 8, "Dense"))
SR.add_layer(layers.Layer1D(8, 1, "Features", shape_spacing=3, fill_color=(1, 0, 0)))
SR.add_operation(operations.DenseOp(8, 20, "Dense"))
SR.add_layer(layers.Layer1D(20, 1, "Features", shape_spacing=0.5))

SR.render(10, text_y_offset=1)
