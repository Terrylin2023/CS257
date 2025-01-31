# CS257

This implementation encodes structured data (dictionaries of key-value pairs) into high-dimensional hypervectors.
### Encoding Mechanism
Step 1: Codebook Initialization
Each symbol (e.g., 'A', 'B', 'X', 'Y') is assigned a random bipolar hypervector (-1 or +1 values).  
Step 2: Encoding Key-Value Pairs
1.	Retrieve each corresponding hypervectors from the codebook.
2.	Bind (⊙) them using element-wise multiplication
3.	Bundle (⊕) the bound hypervectors using element-wise addition
4.	Normalize (sign()) to ensure the result remains bipolar (-1, +1)  

Step 3: Storing the Encoded Hypervector
The final bundled hypervector represents the entire dictionary and is stored in self.data_structure[label]

### Summary
|     Comparison           |     Similarity   Score    |     Interpretation           |
|--------------------------|---------------------------|------------------------------|
|     dict1 vs.   dict2    |     0.5066                |     Moderately similar       |
|     dict1 vs.   dict3    |     0.5513                |     Moderately similar       |
|     dict2 vs.   dict3    |     0.0449                |     Weak similarity          |
|     dict1 vs.   dict4    |     -0.0334               |     Almost no similarity     |
|     dict2 vs.   dict4    |     0.4689                |     Some similarity          |

* Dicts with more shared key-value pairs have higher similarity scores.
* Dissimilar dictionaries show near-zero or negative similarity.
