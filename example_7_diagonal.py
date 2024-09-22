from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating a generic Dense/Linear network as diagonal blocks """

SR = SeqRenderer()
SR.add_layer(layers.Layer1DDiagonal(2, 10, "Input\n10"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DDiagonal(2, 30, "Features\n30"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DDiagonal(2, 60, "Features\n60"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DDiagonal(2, 60, "Features\n60"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DDiagonal(2, 30, "Features\n30"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DDiagonal(2, 10, "Features\n10"))

SR.render(5, 5, text_y_offset=1, offset_from_limits=True)
