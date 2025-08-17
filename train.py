import torch
from torch import nn, optim


# Creating the PyTorch neural network
class ChatModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChatModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, hidden_size)
        self.output = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output(x)
        return self.softmax(x)


def train(model, training, output):
    # Convert numpy arrays to PyTorch tensors
    X_train = torch.FloatTensor(training)
    y_train = torch.FloatTensor(output)
    
    # Convert one-hot to class indices
    y_train_indices = torch.argmax(y_train, dim=1)  # This converts [1,0,0] → 0, [0,1,0] → 1, etc.
    
    # Define loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    
    # Training loop
    for epoch in range(500):
        # Forward pass
        optimizer.zero_grad()
        outputs = model(X_train)
        
        # Calculate loss and backward pass
        loss = criterion(outputs, y_train_indices)
        loss.backward()
        
        # Update weights
        optimizer.step()
        
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
    
    # Save the trained model
    torch.save(model.state_dict(), 'model.pth')
