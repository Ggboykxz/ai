
# --- NEXUS_AI_SYSTEM/05_TRAINING/__init__.py ---

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import os

class NexusTrainer:
    """
    Orchestre la boucle d'entraînement pour un modèle Nexus.
    """
    def __init__(self, model, train_dataset, learning_rate, batch_size, epochs, device):
        self.model = model.to(device)
        self.train_dataset = train_dataset
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.device = device
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate)
        self.save_path = os.path.join("checkpoints", "nexus_model_final.pth")

    def train(self):
        """
        Exécute la boucle d'entraînement complète.
        Retourne la perte moyenne de la dernière époque et le chemin de sauvegarde.
        """
        print(f"--- Début de l'entraînement sur {self.device} ---")
        print(f"Époques: {self.epochs}, Taille de batch: {self.batch_size}, Taux d'apprentissage: {self.learning_rate}")

        dataloader = DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

        self.model.train() # Mettre le modèle en mode entraînement
        final_avg_loss = 0

        for epoch in range(self.epochs):
            print(f"\n--- Époque {epoch + 1}/{self.epochs} ---")
            total_loss = 0
            progress_bar = tqdm(dataloader, desc=f"Époque {epoch + 1}")

            for batch in progress_bar:
                input_ids = batch['input_ids'].to(self.device)
                labels = batch['labels'].to(self.device)

                self.optimizer.zero_grad()

                loss, _ = self.model(input_ids=input_ids, labels=labels)
                
                if loss is None:
                    continue

                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                progress_bar.set_postfix({"Perte": f"{loss.item():.4f}"})

            avg_loss = total_loss / len(dataloader)
            print(f"Perte moyenne pour l'époque {epoch + 1}: {avg_loss:.4f}")
            if epoch == self.epochs - 1:
                final_avg_loss = avg_loss
        
        self.save_model()
        return final_avg_loss, self.save_path

    def save_model(self):
        """
        Sauvegarde les poids du modèle entraîné.
        """
        save_dir = os.path.dirname(self.save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"\nSauvegarde du modèle entraîné à l'emplacement : {self.save_path}")
        torch.save(self.model.state_dict(), self.save_path)
        print("Modèle sauvegardé avec succès.")

