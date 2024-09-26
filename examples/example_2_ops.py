from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

""" Demonstrating examples of each type of operation """

SR = SeqRenderer()

SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.ArrowOp())
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.BlankOp())
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.Conv2dOp())
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.DenseOp(3, 8))
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.LinearOp())
SR.add_layer(layers.BlockLayer(10, 75))
SR.add_operation(
    operations.CircleOp(diameter=10, symbol="Σ", symbol_kwargs={"weight": "bold"})
)
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(
    operations.DiamondOp(
        width=10, height=10, symbol="Σ", symbol_kwargs={"weight": "bold"}
    )
)
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.ResidualOp(show_hori_segments=True))
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.EllipsisOp(diameter=2, fill_color=(0, 0, 0)))
SR.add_layer(layers.BlockLayer(10, 50))

SR.render(20)
