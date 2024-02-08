# data_preprocessing.py
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader

def load_images_from_folder(folder, image_size=(50, 50)):
    images = []
    labels = []
    label_map = {}  # A dictionary to map original labels to continuous ones
    current_label = 0
    
    for subdir in sorted(os.listdir(folder)):
        subdir_path = os.path.join(folder, subdir)
        if os.path.isdir(subdir_path):
            if subdir not in label_map:  # Assign a new label if subdir is not already in the map
                label_map[subdir] = current_label
                current_label += 1
            for filename in sorted(os.listdir(subdir_path)):
                img_path = os.path.join(subdir_path, filename)
                try:
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        raise ValueError("Image not loaded.")
                    img = cv2.resize(img, image_size)
                    images.append(img)
                    labels.append(label_map[subdir])  # Use mapped label
                except Exception as e:
                    print(f"Skipping file {img_path} due to error: {e}")
    
    return images, labels


def normalize_images(images):
    images_normalized = np.array(images).astype('float32') / 255.0
    return images_normalized

def prepare_data(dataset_path):
    images, labels = load_images_from_folder(dataset_path)
    unique_labels = sorted(set(labels))  # Get sorted list of unique labels
    label_mapping = {label: i for i, label in enumerate(unique_labels)}  # Map original labels to continuous

    # Apply the mapping to your labels
    labels = [label_mapping[label] for label in labels]

    images_normalized = normalize_images(images)
    X_train, X_test, Y_train, Y_test = train_test_split(np.array(images_normalized), np.array(labels), test_size=0.2, random_state=42)
    return X_train, X_test, Y_train, Y_test


class FacesDataset(Dataset):
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        return torch.tensor(image, dtype=torch.float).unsqueeze(0), torch.tensor(label, dtype=torch.long)

def get_data_loaders(X_train, X_test, Y_train, Y_test, batch_size=32):
    train_dataset = FacesDataset(X_train, Y_train)
    test_dataset = FacesDataset(X_test, Y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, test_loader
