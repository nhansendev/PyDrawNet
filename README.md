# PyDrawNet
A python utility for plotting neural network (and other) diagrams

![DenseEx1](examples/dense_example.png)
![ConvEx1](examples/conv_example.png)
![BlockEx1](examples/block_example.png)

Example files have been created to demonstrate the capabilities of the project.

### Requirements
- python 3+ (tested on 3.12 only)
- matplotlib (tested on 3.8.1 only)

### How It Works
##### Layers
Layers are classes that represent "objects", like nodes or images. They create one or more matplotlib collections for rendering, as well as holding useful graphic properties like corner coordinates and total height/width. See "example_1_layers.py" for the currently available layers.

##### Operations
Operations are classes that create connections between layers, such as convolutions, dense lines, or arrows. They create one or more matplotlib collections for rendering. See "example_2_ops.py" for the currently available operations.

##### Renderers
Currently only a sequential renderer class (SeqRenderer) is implemented, which works as follows: layers are rendered one after another from left to right, with operations connecting adjacent layers (no skip-connections). Normally, the renderer calls `plt.show`, but this can be disabled to allow further customization outside of its capabilites.

### Installation
From within pydrawnet folder:
```
pip install .
```

To uninstall:
```
pip uninstall pydrawnet
```

### Basic Usage

```
from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

# The renderer must first be created
SR = SeqRenderer()

# Layers and operations are then added to the renderer
# Note that the order matters for layers and operations, separately
SR.add_layer(layers.BlockLayer(50, 50))
SR.add_operation(operations.ArrowOp())
SR.add_layer(layers.BlockLayer(10, 50))
SR.add_operation(operations.ArrowOp())
SR.add_layer(layers.BlockLayer(50, 10))

# --- This is equivalent to: ---
# SR.add_layer(layers.BlockLayer(50, 50))
# SR.add_layer(layers.BlockLayer(10, 50))
# SR.add_layer(layers.BlockLayer(50, 10))
# SR.add_operation(operations.ArrowOp())
# SR.add_operation(operations.ArrowOp())

# Plot the resulting graphic
SR.render()
```