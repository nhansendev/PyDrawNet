from pydrawnet import NetGraph, layers, operations

""" Demonstrating a generic 2D convolutional network with limited channel displays for compactness and linear layers on the end """

NG = NetGraph()

kernel = (16, 16)
NG.add_layer(layers.Layer2D(3, 600, 600, "Input"))
NG.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
NG.add_layer(layers.Layer2D(16, 299, 299, "", limited=8))
NG.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
NG.add_layer(layers.Layer2D(32, 148, 148, "", limited=16))
NG.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
NG.add_layer(layers.Layer2D(64, 73, 73, "", limited=32))
NG.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
NG.add_layer(layers.Layer2D(128, 35, 35, "", limited=64))
NG.add_operation(operations.Conv2dOp(kernel, 1, "ConvBlock"))
NG.add_layer(layers.Layer2D(1, 32, 32, ""))
NG.add_operation(operations.LinearOp("Adaptive\nAvgPool2d"))
NG.add_layer(layers.Layer2D(1, 3, 3, ""))
NG.add_operation(operations.LinearOp("Flatten"))
NG.add_layer(layers.Layer1DDiagonal(10, 90, "Features\n9"))
NG.add_operation(operations.LinearOp("Dense"))
NG.add_layer(layers.Layer1DRect(2, 10, 10, "Output"))

NG.render(100, 200, ymargin=0.25)
