In this repository I create two search engine components one using the native to Python Whoosh package for strict keyword searching and retrieving documnents using metadata and another using Haystack to make a semantic question answering pipeline for document retrieval. The indexes are created using a pdf version of J.R.R Tolkien's The Lord of The Rings. There are two models from Huggingface used for sentence embedding and question-answer retrieval.

The two components are the combined into a GUI created with tkinter to allow quick no code usage of the two functions for end users with no Python experience. The app can be hosted via an API or bundled into an executable for use if needed. An example of the GUI can be seen below.

<u>Question/Answer Pipeline:</u>
<img width="880" alt="image" src="https://user-images.githubusercontent.com/43864012/227404504-a9f26a8f-46e4-4845-a9d3-86fdb4f24292.png">


<u>Search and Retrieve Pipeline</u>
<img width="880" alt="image" src="https://user-images.githubusercontent.com/43864012/227404613-f987cb6e-4099-41ad-a327-afae6da3be03.png">
