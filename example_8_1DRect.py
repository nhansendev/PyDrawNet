from pydrawnet import SeqRenderer, layers, operations

""" Demonstrating a generic Dense/Linear network as stacked rectangular blocks """

SR = SeqRenderer()
SR.add_layer(layers.Layer1DRect(10, 10, 10, "Input"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(30, 10, 10, "Features"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(60, 10, 10, "Features"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(60, 10, 10, "Features"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(30, 10, 10, "Features"))
SR.add_operation(operations.LinearOp("Dense"))
SR.add_layer(layers.Layer1DRect(10, 10, 10, "Features"))

SR.render(100, text_y_offset=1, offset_from_limits=True, ymargin=0.1)
