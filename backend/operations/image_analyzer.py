import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

from utils.file_constants import get_platform


class ImageAnalyzer:
    """Analyse images and find similar groups"""

    def __init__(self, similarity_threshold: float = 0.85):
        """
        Args:
            similarity_threshold: (0-1) for duplicates definition
        """
        self.similarity_threshold = similarity_threshold
        self.device = self._define_device()
        self.model = self._load_model()
        self.transform = self._get_transforms()
        self.image_embeddings = {}                  # Cache для embeddings


    @staticmethod
    def _define_device():
        platform = get_platform()
        if  platform == "macos":
            return torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        elif platform == "windows":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            return torch.device("cpu")


    def _load_model(self):
        """Load ResNet18 model and transforms for preprocessing"""
        weights = models.ResNet18_Weights.DEFAULT
        model = models.resnet18(weights=weights)
        model = torch.nn.Sequential(*list(model.children())[:-1])           # Видаляємо classification layer
        model = model.to(self.device)
        model.eval()

        return model

    @staticmethod
    def _get_transforms():
        """Get ResNet transformations for image"""
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    @staticmethod
    def _is_valid_image(file_path: str) -> bool:
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def _get_embedding(self, file_path: str):
        """Receive embedding vector for image"""
        try:
            if file_path in self.image_embeddings:
                return self.image_embeddings[file_path]

            image = Image.open(file_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                embedding = self.model(image_tensor)

            embedding = embedding.cpu().numpy().flatten()
            embedding = embedding / np.linalg.norm(embedding)

            self.image_embeddings[file_path] = embedding
            return embedding

        except Exception as e:
            print(f"Error getting embedding for {file_path}: {e}")
            return None


    def find_duplicates(self, files: list[dict]) -> dict[str, list[dict]]:
        """Finds similar images or duplicates

        Args:
            files: list of files

        Returns:
            Dict with groups of similar images
            {
                "image1.jpg": [
                    {"path": "image2.jpg", "similarity": 0.95},
                    {"path": "image3.jpg", "similarity": 0.92}
                ]
            }
        """
        image_files = [
            f for f in files
            if f["category"] == "Images" and self._is_valid_image(f["path"])
        ]

        if len(image_files) < 2:
            return {}

        print(f"Analyzing {len(image_files)} images for duplicates...")

        # Отримуємо embeddings для всіх зображень
        embeddings_dict = {}
        for file_info in image_files:
            embedding = self._get_embedding(file_info["path"])
            if embedding is not None:
                embeddings_dict[file_info["path"]] = embedding

        if len(embeddings_dict) < 2:
            print("Not enough valid images to compare")
            return {}

        paths = list(embeddings_dict.keys())
        embeddings = np.array(list(embeddings_dict.values()))

        similarity_matrix = cosine_similarity(embeddings)

        # Знаходимо дублікати
        duplicates = {}
        for i, path1 in enumerate(paths):
            similar_images = []

            for j, path2 in enumerate(paths):
                if i == j:
                    continue

                similarity = float(similarity_matrix[i][j])

                if similarity >= self.similarity_threshold:
                    similar_images.append({
                        "path": path2,
                        "similarity": round(similarity, 3),
                        "similarity_percent": round(similarity * 100, 1)
                    })

            # Зберігаємо тільки якщо знайшли дублікати
            if similar_images:
                similar_images.sort(key=lambda x: x["similarity"], reverse=True)
                duplicates[path1] = similar_images

        return duplicates

    def clear_cache(self):
        """Clear embeddings cache"""
        self.image_embeddings = {}