from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating examples of each type of operation """

SR = SeqRenderer()

SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.ArrowOp())
SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.BlankOp())
SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.Conv2dOp())
SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.DenseOp(3, 8))
SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.LinearOp())
SR.add_layer(layers.BlockLayer(50, 75))

SR.render(50)
