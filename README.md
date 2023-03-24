In this repository there are two NLP components, a search engine similar to how google operates and a question/answer pipeline that allows the user to ask a question and retrieve an answer based on the database of text used for the index. The indexes are created using a pdf of J.R.R Tolkien's The Lord of The Rings. The search engine was created using Whoosh and the question/answer pipeline was created using Haystack and two models from Huggingface for sentence transformation and question/answer retrieval.

The two components are the combined into a GUI created with tkinter in order to allow quick usage of the two functions. An example of the GUI can be seen below here:

<u>Question/Answer Pipeline:</u>
<img width="880" alt="image" src="https://user-images.githubusercontent.com/43864012/227404504-a9f26a8f-46e4-4845-a9d3-86fdb4f24292.png">


<u>Search and Retrieve Pipeline</u>
<img width="880" alt="image" src="https://user-images.githubusercontent.com/43864012/227404613-f987cb6e-4099-41ad-a327-afae6da3be03.png">
