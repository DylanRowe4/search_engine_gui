import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from haystack.document_stores import FAISSDocumentStore
from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor, EmbeddingRetriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader
import torch

gpu_use = torch.cuda.is_available()
print(f"GPU Available: {gpu_use}")

def query_index(index_location, user_query):
    ix = open_dir(index_location)
    
    with ix.searcher() as searcher:
        #load input query to parser
        query = QueryParser("content", ix.schema).parse(user_query)
        print(f"Query: {query}")
        #search index for query
        results = searcher.search(query, terms=True, limit=10)
        
        results_list = []
        #iterate through response
        for res in results:
            results_list.append((res['path'], res.score, res['content']))
    return query, results_list
    
def query_faiss_index(index_location, user_query):
    document_store = FAISSDocumentStore.load(index_path=index_location)
    
    #add reader using tinyroberta
    reader = FARMReader(model_name_or_path='../tinyroberta_local_farm',
                        use_gpu=gpu_use, context_window_size=300)
    
    #retriever using the same embedding model as when index is created
    retriever = EmbeddingRetriever(document_store=document_store,
                               embedding_model='../all-mpnet-base-v2',
                               model_format='sentence_transformers')
    
    #add reader and retriever to question-answer pipeline
    pipeline = ExtractiveQAPipeline(reader, retriever)
    
    prediction = pipeline.run(query=user_query,
                              params={
                                  "Retriever": {"top_k": 10},
                                  "Reader": {"top_k": 5}
                              })
    results = []
    for answer in prediction['answers']:
        results.append((answer.answer, answer.context, answer.score))
    return results