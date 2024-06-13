## Context
This code is based on the AlphaGeometry Project :
https://github.com/google-deepmind/alphageometry
Its goal is to transform the alpha geometry model from a LLM to a VLM. 
For this purpose, I created multiple scripts which purpose was to generate random geometric figures.
To use the files present here, please clone the project and put them here.
## Files Description

Here is each custom script added to the base AlphaGeometry repo and their description.
Please see the original project's README.md to check the other files' description.

| File name              | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| `text_to_graph.py`     | The main script used to generate the dataset with randomly generated figures             |
| `random_data.py`       | Generate a random string following the alphageometry structure. Used in the above script.|
| `proof_step_to_txt.py` | Transforms the results of the solver into a string containing all the needed infos.      |

