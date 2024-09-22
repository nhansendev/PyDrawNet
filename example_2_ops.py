from pydrawnet import NetGraph, layers, operations

""" Demonstrating examples of each type of operation """

NG = NetGraph()

NG.add_layer(layers.BlockLayer(50, 50))
NG.add_operation(operations.ArrowOp())
NG.add_layer(layers.BlockLayer(50, 50))
NG.add_operation(operations.BlankOp())
NG.add_layer(layers.BlockLayer(50, 50))
NG.add_operation(operations.Conv2dOp())
NG.add_layer(layers.BlockLayer(50, 50))
NG.add_operation(operations.DenseOp(3, 8))
NG.add_layer(layers.BlockLayer(50, 50))
NG.add_operation(operations.LinearOp())
NG.add_layer(layers.BlockLayer(50, 75))

NG.render(50)
