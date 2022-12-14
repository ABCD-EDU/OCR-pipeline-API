import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, DistilBertModel, AutoModelForSequenceClassification
import gdown
from pathlib import Path
from loader.Task1NN import LangModelWithDense

# from loader.config


def download_model():
    # script_dir = os.path.dirname(__file__)
    path = "./bin/bert_models/model.pt"
    # abs_file_path = os.path.join(script_dir, rel_path)
    path = Path(path)

    url = "https://drive.google.com/uc?id=1ExkkBYxpuWHb_ffUzGbArgLCbay77_Ip"
    if path.is_file() == False:
        gdown.download(
            url=url, output="./bin/bert_models/model.pt", quiet=False)
    else:
        print('Model file already downloaded')


# download_model()
bert_model_name = 'distilbert-base-uncased'
task1_2_tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
task1_lang_model = DistilBertModel.from_pretrained(bert_model_name)
task1_model = LangModelWithDense(task1_lang_model)
task1_model.load_state_dict(torch.load('./bin/model1.pt'))
task1_model.eval()

task2_model = AutoModelForTokenClassification.from_pretrained(bert_model_name, num_labels=13)
task2_model.load_state_dict(torch.load('./bin/model2.pt'))
task2_model.eval()

task3_tokenizer = AutoTokenizer.from_pretrained("tobiaslee/roberta-large-defteval-t6-st3")

task3_model = AutoModelForSequenceClassification.from_pretrained("tobiaslee/roberta-large-defteval-t6-st3")
task3_model.eval()


def get_encoded(text)->dict:
   task1_2_encoding = task1_2_tokenizer.encode_plus(
      text.lower(),
      return_attention_mask=True,
      return_tensors='pt'
   )
   
   task3_encoding = task3_tokenizer.encode_plus(
      text.lower(),
      return_attention_mask=True,
      return_tensors='pt'
   )
   task1_2_encoded = dict(
     input_ids=task1_2_encoding['input_ids'].flatten(),
     attention_mask=encoding['attention_mask'].flatten()
   )
   
   return {"task1_2_encoded"}


