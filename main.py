import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, gaussian_filter
import matplotlib.animation as animation
from typing import Tuple, List

def update(soup: np.ndarray) -> np.ndarray:
    """
    Update the grid based on Conway's Game of Life rules.

    Parameters:
    - soup: np.ndarray, the current state of the grid.

    Returns:
    - np.ndarray: The updated state of the grid.
    """
    # Define the kernel for counting neighbors
    K = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])
    
    # Count neighbors for each cell
    N = convolve(soup, K, mode='constant', cval=0)

    # Apply rules of Conway's Game of Life
    return np.where((N == 3) | ((N == 2) & (soup == 1)), 1, 0)

def create_random_soup(size: Tuple[int, int], noise_type: str = 'uniform', 
                       p: float = 0.5, std: float = 1.0, 
                       salt_vs_pepper: float = 0.5) -> np.ndarray:
    """
    Create a random initial grid with the given size and noise type.

    Parameters:
    - size: tuple, the dimensions of the grid.
    - noise_type: str, the type of noise to generate ('uniform', 'gaussian', 'salt_and_pepper').
    - p: float, probability of a cell being alive for uniform and salt_and_pepper noise.
    - std: float, standard deviation for Gaussian noise.
    - salt_vs_pepper: float, ratio of salt vs. pepper noise (only for salt_and_pepper).

    Returns:
    - np.ndarray: The generated initial grid.
    """
    if noise_type == 'uniform':
        # Uniform random noise
        return np.random.choice([0, 1], size=size, p=[1-p, p])
    
    elif noise_type == 'gaussian':
        # Gaussian noise
        random_values = np.random.normal(loc=0.5, scale=std, size=size)
        return (random_values > 0.5).astype(int)
    
    elif noise_type == 'salt_and_pepper':
        # Salt and pepper noise
        soup = np.random.choice([0, 1, 2], size=size, p=[salt_vs_pepper*(1-p), (1-salt_vs_pepper)*(1-p), p])
        soup[soup == 2] = 1  # Convert salt values (2) to 1
        return soup

    else:
        raise ValueError(f"Unsupported noise type: {noise_type}")

def calculate_second_order_changes(soup: np.ndarray, updated_soup: np.ndarray) -> int:
    """
    Calculate the second-order changes matrix.

    Parameters:
    - soup: np.ndarray, the original grid.
    - updated_soup: np.ndarray, the updated grid.

    Returns:
    - int: The sum of second-order changes.
    """
    first_order_changes = np.abs(soup - updated_soup)
    updated_first_order = update(first_order_changes)
    second_order_changes = np.abs(first_order_changes - updated_first_order)
    return np.sum(second_order_changes)

def update_frame(frame_num: int, img: plt.Axes, soup: List[np.ndarray], 
                 line: plt.Line2D, second_order_changes: List[int]) -> Tuple[plt.Axes, plt.Line2D]:
    """
    Update the frame for the animation and plot.

    Parameters:
    - frame_num: int, the current frame number.
    - img: plt.Axes, the image axis to update.
    - soup: list of np.ndarray, the current grid state.
    - line: plt.Line2D, the line plot axis for second order changes.
    - second_order_changes: list of int, the list of second order change sums.

    Returns:
    - Tuple[plt.Axes, plt.Line2D]: Updated image and line plot.
    """
    new_soup = update(soup[0])
    
    # Calculate second order changes
    changes = calculate_second_order_changes(soup[0], new_soup)
    second_order_changes.append(max(changes, 1))  # Ensure no zero value by using 1

    # Update image
    img.set_data(new_soup)
    soup[0] = new_soup

    # Update line plot
    line.set_data(range(len(second_order_changes)), second_order_changes)
    line.axes.relim()
    line.axes.autoscale_view()

    return img, line

def simulate_conway(size: Tuple[int, int] = (500, 500), frames: int = 100, 
                    speed: float = 100.0) -> None:
    """
    Simulate Conway's Game of Life using the update function.

    Parameters:
    - size: tuple, the dimensions of the grid.
    - frames: int, number of frames to simulate.
    - speed: float, speed of the animation in frames per second.
    """
    soup = [create_random_soup(size, noise_type='uniform')]
    second_order_changes = []

    # Create a larger figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Display the Game of Life grid
    img = ax1.imshow(soup[0], cmap='binary')
    ax1.set_title("Conway's Game of Life")
    ax1.axis('off')  # Hide the axes

    # Initialize line plot for second order changes
    line, = ax2.plot([], [], lw=2)
    ax2.set_xlim(0, frames)
    ax2.set_yscale('log')  # Set y-axis to logarithmic scale
    ax2.set_ylim(1, np.prod(size))  # Start from 1 to avoid log(0) issues
    ax2.grid(True, which="both", linestyle='--', color='gray')  # Dotted gray grid
    ax2.set_title("Second Order Changes Over Time")
    ax2.set_xlabel("Frames")
    ax2.set_ylabel("Total 1s in Second Order Changes")

    # Calculate interval based on speed
    interval = max(1, int(1000 / speed))  # Minimum interval set to 1 ms

    ani = animation.FuncAnimation(
        fig, update_frame, fargs=(img, soup, line, second_order_changes),
        frames=frames, interval=interval, blit=True, repeat=False  # Ensure repeat=False
    )

    plt.tight_layout()
    plt.show()

# Run the simulation with very high speed and larger grid
simulate_conway(size=(100, 100), frames=2000, speed=1000.0)
