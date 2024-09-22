from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating image layers """

SR = SeqRenderer()
SR.add_layer(layers.ImageLayer("examples//dense_example.png", 100, 60))
SR.add_operation(operations.ArrowOp(""))
SR.add_layer(layers.ImageLayer("examples//dense_example.png", 60, 100))

SR.render(30, text_y_offset=1)
