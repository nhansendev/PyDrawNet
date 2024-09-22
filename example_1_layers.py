from pydrawnet import NetGraph, layers
import math

""" Demonstrating examples of each type of layer """

NG = NetGraph()

kernel = (8, 16)
NG.add_layer(layers.Layer2D(20, 16, 40, "Layer2D", cspace=5))
NG.add_layer(
    layers.Layer2D(
        32,
        12,
        12,
        "Layer2D",
        limited=16,
        end_channels=2,
        limited_radius=2,
        skip_ival=1,
        cspace=5,
        color_dark=(0, 0, 1),
        color_light=(0, 1, 0),
    )
)
NG.add_layer(layers.Layer1D(9, 10, "Layer1D", shape_spacing=3))
NG.add_layer(
    layers.Layer1D(
        50,
        10,
        "Layer1D",
        shape_spacing=-5,
        limited=16,
        limited_radius=2,
        fill_color=(0.5, 0.5, 0.5),
    )
)
NG.add_layer(
    layers.Layer1D(
        50,
        10,
        "Layer1D",
        shape_spacing=5,
        limited=16,
        limited_radius=2,
        fill_color=(0.5, 0.5, 0.5),
    )
)
NG.add_layer(layers.Layer1DRect(20, 10, 10, "Layer1DRect"))
NG.add_layer(
    layers.Layer1DRect(
        80,
        10,
        10,
        "Layer1DRect",
        limited=20,
        shape_spacing=5,
        fill_color=(0.9, 0.4, 0.3),
    )
)
NG.add_layer(layers.Layer1DDiagonal(10, 64, "Layer1DDiagonal"))
NG.add_layer(
    layers.Layer1DDiagonal(50, 12, "Layer1DDiagonal", fill_color=(0.1, 0.9, 0.5))
)
NG.add_layer(layers.BlockLayer(60, 20))
NG.add_layer(layers.BlockLayer(5, 90, fill_color=(0.9, 0.8, 0.7)))

X = [100 * math.cos(-0.5 + i / 10) ** 3 - 70 for i in range(11)]
Y = [50 * math.sin(-0.5 + i / 10) for i in range(11)]
NG.add_layer(layers.PolyLayer(list(zip(X, Y))))

NG.render(75, 150, ymargin=0.25)
