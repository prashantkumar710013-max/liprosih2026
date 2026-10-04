from abc import ABC, abstractmethod
import pandas as pd
from typing import Any, Dict

class BaseModelInterface(ABC):
    
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Trains the model"""
        pass
        
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Generates predictions"""
        pass
        
    @abstractmethod
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Evaluates model performance"""
        pass
        
    @abstractmethod
    def save(self, path: str) -> None:
        """Saves the model to disk"""
        pass
        
    @abstractmethod
    def load(self, path: str) -> None:
        """Loads the model from disk"""
        pass
