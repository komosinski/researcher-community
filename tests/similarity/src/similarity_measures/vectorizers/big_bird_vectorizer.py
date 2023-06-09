from tests.similarity.src.similarity_measures.vectorizers.vectorizer import Vectorizer
import numpy as np
from pathlib import Path
from transformers import AutoTokenizer, AutoModel, BertForSequenceClassification, BertModel, RobertaModel, BigBirdModel
import torch
import gc


class BigBirdVectorizer(Vectorizer):

    def __init__(self, context_len=512):
        self.tokenizer = AutoTokenizer.from_pretrained("google/bigbird-roberta-base")
        self.model = AutoModel.from_pretrained("google/bigbird-roberta-base").to("cuda")
        self.model.eval()
        self.context_len = context_len

        gc.collect()

        torch.cuda.empty_cache()

    def transform(self, corpus: list) -> list:
        results = []
        for doc in corpus:
            encoding = self.tokenizer(
                doc,
                add_special_tokens=True,
                max_length=self.context_len,
                return_token_type_ids=False,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt', )
            encoding = encoding.to("cuda")
            embeddings = self.model(encoding["input_ids"],
                                          encoding["attention_mask"])
        #print()
            results.append(embeddings['pooler_output'].squeeze().cpu().detach().tolist())
        return results

#if __name__ == "__main__":
#    b= BigBirdVectorizer()
#    b.transform(['''ome weights of the model checkpoint at prajjwal1/bert-tiny were not used when initializing BertModel: ['cls.predictions.bias', 'cls.seq_relationship.weight', 'cls.predictions.decoder.weight', 'cls.predictions.transform.LayerNorm.weight', 'cls.seq_relationship.bias', 'cls.predictions.decoder.bias', 'cls.predictions.transform.LayerNorm.bias', 'cls.predictions.transform.dense.bias', 'cls.predictions.transform.dense.weight']
#- This IS expected if you are initializing BertModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
#- This IS NOT expected if you are initializing BertModel from the checkpoint of a model that you expect to be exactly identical'''])