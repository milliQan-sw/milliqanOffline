import numpy as np
import matplotlib.pyplot as plt


def plot_loss(discriminator_loss:np.ndarray, generator_loss:np.ndarray,
              save_location="loss.png", show_figure=False,
              save_figure=True)->None:
    plt.plot(discriminator_loss, label="Discriminator")
    plt.plot(generator_loss, label="Generator")
    plt.ylabel("Loss")
    plt.xlabel("Epochs")
    plt.title("Loss vs Epochs")
    plt.legend()

    if save_figure:
        plt.savefig(save_location)
    if show_figure:
        plt.show() 
    

    
    
