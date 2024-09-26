from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating a ResNet style network using residual operations """

SR = SeqRenderer()

abet = "ABCDEFGHIJKLMNOP"

SR.add_layer(layers.Layer2D(3, 256, 256, "Input", color_light=(0.7, 0.7, 0.5)))
SR.add_layer(layers.Layer2D(64, 256, 256, "", limited=16, end_channels=5))
SR.add_layer(layers.Layer2D(128, 128, 128, "", limited=32, end_channels=10))
SR.add_layer(layers.Layer2D(256, 64, 64, "", limited=64, end_channels=20))
SR.add_layer(layers.Layer2D(256, 64, 64, "", limited=64, end_channels=20))
SR.add_layer(layers.Layer2D(256, 64, 64, "", limited=64, end_channels=20))
SR.add_layer(layers.Layer2D(256, 64, 64, "", limited=64, end_channels=20))
SR.add_layer(layers.Layer2D(256, 64, 64, "", limited=64, end_channels=20))
SR.add_layer(layers.Layer2D(128, 128, 128, "", limited=32, end_channels=10))
SR.add_layer(layers.Layer2D(64, 256, 256, "", limited=16, end_channels=5))
SR.add_layer(layers.Layer2D(3, 256, 256, "Output", color_light=(0.5, 0.7, 0.7)))

SR.add_operation(operations.Conv2dOp((16, 16), label="Downsample", label_only=True))
SR.add_operation(operations.Conv2dOp((16, 16), label="Downsample", label_only=True))
SR.add_operation(operations.Conv2dOp((16, 16), label="Downsample", label_only=True))
SR.add_operation(operations.LinearOp("Residual\nBlock"))
SR.add_operation(operations.LinearOp("Residual\nBlock"))
SR.add_operation(operations.LinearOp("Residual\nBlock"))
SR.add_operation(operations.LinearOp("Residual\nBlock"))
SR.add_operation(
    operations.Conv2dOp((16, 16), label="Upsample", label_only=True, reverse=True)
)
SR.add_operation(
    operations.Conv2dOp((16, 16), label="Upsample", label_only=True, reverse=True)
)
SR.add_operation(
    operations.Conv2dOp((16, 16), label="Upsample", label_only=True, reverse=True)
)

SR.render(75, 150, text_y_offset=20, offset_from_limits=False)
