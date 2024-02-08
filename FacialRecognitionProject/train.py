# train.py
from torch.optim.lr_scheduler import StepLR
from data_preprocessing import prepare_data, get_data_loaders
from model import SimpleCNN
import torch
import torch.optim as optim
import torch.nn as nn
import os

def train_model(dataset_path, batch_size=32, epochs=10000, checkpoint_interval=100):
    # Prepare data and get data loaders
    X_train, X_test, Y_train, Y_test = prepare_data(dataset_path)
    train_loader, test_loader = get_data_loaders(X_train, X_test, Y_train, Y_test, batch_size=batch_size)
    
    # Check labels and calculate num_classes
    num_classes = max(Y_train) + 1  # Correctly calculating num_classes based on Y_train
    print(f"Unique labels in training data: {len(set(Y_train))}")
    print(f"Label range in training data: {min(Y_train)} - {max(Y_train)}")
    print(f"Min label: {min(Y_train)}, Max label: {max(Y_train)}, Num classes: {num_classes}")

    # Initialize model, criterion, and optimizer
    model = SimpleCNN(num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # Initial learning rate

    # Initialize the learning rate scheduler
    scheduler = StepLR(optimizer, step_size=30, gamma=0.1)  # Adjust the learning rate

    # Load checkpoint if exists
    checkpoint_path = 'model_checkpoint.pth'
    if os.path.isfile(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state'])
        optimizer.load_state_dict(checkpoint['optimizer_state'])
        scheduler.load_state_dict(checkpoint['scheduler_state'])  # Load scheduler state
        start_epoch = checkpoint['epoch']
        print(f"Resuming training from epoch {start_epoch + 1}")
    else:
        start_epoch = 0

    # Training loop
    for epoch in range(start_epoch, epochs):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        # After optimizer.step(), update the learning rate
        scheduler.step()
        
        # Evaluation on the test set
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        accuracy = correct / total
        print(f"Epoch {epoch+1}, Loss: {loss.item()}, Accuracy on test set: {accuracy:.2f}")
        
        # Save checkpoint at the end of each epoch or checkpoint interval
        if (epoch + 1) % checkpoint_interval == 0 or (epoch + 1) == epochs:
            torch.save({
                'epoch': epoch + 1,  # Save next epoch index to continue correctly
                'model_state': model.state_dict(),
                'optimizer_state': optimizer.state_dict(),
                'scheduler_state': scheduler.state_dict(),  # Save scheduler state
            }, checkpoint_path)
            print(f"Checkpoint saved at epoch {epoch + 1}")

    # Optionally, save the final model state separately
    torch.save(model.state_dict(), 'final_model_weights.pth')
    print("Training completed and final model saved.")

if __name__ == "__main__":
    dataset_path = 'C:\\Users\\OooO\\Documents\\Python ML AI\\lfwa\\lfw2\\lfw2'
    train_model(dataset_path)  # Use default batch_size and epochs unless you intend otherwise
