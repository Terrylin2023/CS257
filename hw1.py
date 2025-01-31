import numpy as np
from collections import defaultdict

class HDStructure:
    def __init__(self, dimension, symbols):
        """
        Initialize dimension,codebook.
        """
        self.dimension = dimension
        self.symbols = symbols
        self.codebook = self.generate_hypervectors(dimension, symbols)
        self.data_structure = defaultdict(lambda: np.ones(dimension))  # Stores encoded structures
    
    def generate_hypervectors(self, dimension, symbols):
        """
        Generate n random bipolar hypervector of dimension D. (n is # of symbols)
        """
        return {symbol: np.random.choice([-1, 1], size=dimension) for symbol in symbols}
    
    def binding(self, hv1, hv2):
        """
        Perform elementwise multiplication for MAP-based HDC
        """
        return hv1 * hv2

    def bundling(self, *hv_list):
        """
        Perform elementwise addition 
        """
        bundled = np.sum(hv_list, axis=0)
        return np.sign(bundled)  # normalize hypervectors 

    def permute(self, hv):
        """
        Shifts all elements to the right by 1,
        """
        return np.roll(hv, shift=1)

    def encode(self, dictionary, label):
        encoded_hv = np.zeros(self.dimension)
        for key, value in dictionary.items():
            if key in self.codebook and value in self.codebook:
                pair_hv = self.binding(self.codebook[key], self.codebook[value])
                encoded_hv = self.bundling(encoded_hv, pair_hv)
        encoded_hv = np.sign(encoded_hv)
        self.data_structure[label] = encoded_hv  # Store encoded dictionary hypervector
        return encoded_hv

    def similarity(self, hv1, hv2):
        """ 
        compute cosine similarity.
        """
        return np.dot(hv1, hv2) / (np.linalg.norm(hv1) * np.linalg.norm(hv2))
    def add_data(self, symbol):
        """ 
        add new data (e.g. a key-value pair) to the structure.
        """
        if symbol not in self.symbols:
            self.symbols.append(symbol)
            self.codebook[symbol] = np.random.choice([-1, 1], size=self.dimension)
            
    def decode(self, hv_encoded):
        """ 
        optional: attempt to decode or interpret the HV
        """
        best_match = None
        best_similarity = -1
        for key, hv in self.data_structure.items():
            sim = self.similarity(hv_encoded, hv)
            if sim > best_similarity:
                best_similarity = sim
                best_match = key
        return best_match

if __name__ == "__main__":
    dimension = 1000
    symbols = ['A', 'B', 'C', 'X', 'Y', 'Z']

    hdc = HDStructure(dimension, symbols)
    
    # Encode dictionaries
    dict1 = {'A': 'X', 'C': 'Z'}
    dict2 = {'A': 'X', 'B': 'Z'}
    dict3 = {'B': 'X', 'C': 'Z'}  

    hv1 = hdc.encode(dict1, 'dict1')
    hv2 = hdc.encode(dict2, 'dict2')
    hv3 = hdc.encode(dict3, 'dict3')

    # Compute similarities
    print("Similarity between dict1 and dict2:", hdc.similarity(hv1, hv2))
    print("Similarity between dict1 and dict3:", hdc.similarity(hv1, hv3))
    print("Similarity between dict2 and dict3:", hdc.similarity(hv2, hv3))

    # Add new data
    hdc.add_data('D')
    dict4 = {'A': 'D', 'B': 'Z'}
    hv4 = hdc.encode(dict4, 'dict4')
    print("Similarity between dict1 and dict4:", hdc.similarity(hv1, hv4))
    print("Similarity between dict2 and dict4:", hdc.similarity(hv2, hv4))

    # Decode by finding the most similar stored vector
    print("Decoded closest match for dict1:", hdc.decode(hv1))
    print("Decoded closest match for dict2:", hdc.decode(hv2))
