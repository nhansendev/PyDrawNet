from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating a generic 2D convolutional network with limited channel displays for compactness and linear layers on the end """

SR = SeqRenderer()

kernel = (16, 16)
SR.add_layer(layers.Layer2D(3, 600, 600, "Input"))
SR.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
SR.add_layer(layers.Layer2D(16, 299, 299, "", limited=8))
SR.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
SR.add_layer(layers.Layer2D(32, 148, 148, "", limited=16))
SR.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
SR.add_layer(layers.Layer2D(64, 73, 73, "", limited=32))
SR.add_operation(operations.Conv2dOp(kernel, 2, "ConvBlock"))
SR.add_layer(layers.Layer2D(128, 35, 35, "", limited=64))
SR.add_operation(operations.Conv2dOp(kernel, 1, "ConvBlock"))
SR.add_layer(layers.Layer2D(1, 32, 32, ""))
SR.add_operation(operations.LinearOp("Adaptive\nAvgPool2d"))
SR.add_layer(layers.Layer2D(1, 3, 3, ""))
SR.add_operation(operations.LinearOp("Flatten"))
SR.add_layer(layers.Layer1DDiagonal(10, 90, "Features\n9"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(2, 10, 10, "Output"))

SR.render(100, 200, ymargin=0.25)
