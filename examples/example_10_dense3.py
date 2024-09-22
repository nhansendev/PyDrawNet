from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating a generic Dense/Linear network without limiting shown nodes, which is a bit ugly """

SR = SeqRenderer()
SR.add_layer(layers.Layer1DRect(10, 1, 1, "Input", shape_spacing=0))
SR.add_operation(operations.DenseOp(10, 30, "Dense"))
SR.add_layer(layers.Layer1D(30, 1, "Features", shape_spacing=0.5))
SR.add_operation(operations.DenseOp(30, 30, "Dense"))
SR.add_layer(layers.Layer1D(30, 1, "Features", shape_spacing=0.5))
SR.add_operation(operations.DenseOp(30, 5, "Dense"))
SR.add_layer(layers.Layer1D(5, 1, "Features", shape_spacing=0.5))

SR.render(30, text_y_offset=1)
