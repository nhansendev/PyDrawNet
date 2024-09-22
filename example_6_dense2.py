from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating a generic Dense/Linear network with some of the available parameter variations """

SR = SeqRenderer()
SR.add_layer(layers.Layer1DRect(10, 1, 1, "Input", shape_spacing=0))
SR.add_operation(operations.DenseOp(10, 15, "Dense", limited_ends=(None, 3)))
SR.add_layer(
    layers.Layer1D(30, 1, "Features", shape_spacing=0.5, limited=15, end_features=3)
)
SR.add_operation(operations.DenseOp(15, 15, "Dense", limited_ends=3))
SR.add_layer(
    layers.Layer1D(30, 1, "Features", shape_spacing=0.5, limited=15, end_features=3)
)
SR.add_operation(operations.DenseOp(15, 5, "Dense", limited_ends=(3, None)))
SR.add_layer(layers.Layer1D(5, 1, "Features", shape_spacing=0.5))

SR.render(10, text_y_offset=1)
