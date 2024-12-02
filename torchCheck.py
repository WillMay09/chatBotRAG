import torch

# Check if CUDA is available
print("CUDA available:", torch.cuda.is_available())

# Perform a simple tensor operation
a = torch.tensor([1, 2, 3], device="cuda" if torch.cuda.is_available() else "cpu")
print(a)



# Check if CUDA (GPU) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Print the device PyTorch is using
print(f"PyTorch is using the {device} device.")