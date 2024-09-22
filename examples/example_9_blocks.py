from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating a simple block diagram """

SR = SeqRenderer()
SR.add_layer(layers.BlockLayer(10, 100, "Input"))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.BlockLayer(10, 100, "", (0, 0, 1)))
SR.add_operation(operations.LinearOp("Conv2D", loc="above"))
SR.add_layer(layers.BlockLayer(20, 50, "", (0, 0, 1)))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.BlockLayer(20, 50, "Activation\nFunction", (0, 1, 0)))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.BlockLayer(20, 50, "BatchNorm2d", (0, 1, 0)))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.BlockLayer(20, 50, "Dropout\n(Optional)", (0, 1, 0)))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.BlockLayer(20, 50, "Output", (0.2, 0.2, 0.2)))

SR.render(20, text_y_offset=5)
