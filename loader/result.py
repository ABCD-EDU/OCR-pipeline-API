import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, DistilBertModel, AutoModelForSequenceClassification
import gdown
from pathlib import Path
from loader.Task1NN import LangModelWithDense

# from loader.config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

inv_eval_ent_dict= {
   1:'B-Term', 
   2:'I-Term', 
   3:'B-Definition', 
   4:'I-Definition', 
   5:'B-Alias-Term', 
   6:'I-Alias-Term',            
   7:'B-Referential-Definition', 
   8:'I-Referential-Definition', 
   9:'B-Referential-Term', 
   10:'I-Referential-Term',   
   11:'B-Qualifier', 
   12:'I-Qualifier', 
   0:'O'}         


eval_ent_dict = {value:key for key, value in inv_eval_ent_dict.items()}


def pred_to_label(pred):
   output = []
   for p in pred[0]: 
      out = inv_eval_ent_dict[torch.argmax(p).item()]
      output.append(out)
   return output


def get_encoded(text)->dict:
   task1_2_encoding = task1_2_tokenizer.encode_plus(
      text.lower(),
      return_attention_mask=True,
      return_tensors='pt'
   )
   
   task1_2_encoded = dict(
     input_ids=task1_2_encoding['input_ids'].flatten(),
     attention_mask=task1_2_encoding['attention_mask'].flatten()
   )
   
 
   
   return {"task1_2_encoded":task1_2_encoded}

def get_result(texts):
   output = []
   for text in texts:
      task1_2_encoded = get_encoded(text)
      with torch.no_grad():
         task1_prediction = task1_model(
            task1_2_encoded['input_ids'].unsqueeze(dim=0).to(device),
            task1_2_encoded['attention_mask'].unsqueeze(dim=0).to(device))

         if task1_prediction >=0.5:
            task2_prediction = task2_model(
            task1_2_encoded['input_ids'].unsqueeze(dim=0).to(device),
            task1_2_encoded['attention_mask'].unsqueeze(dim=0).to(device))
            
            output.append({"text": text, "labels":pred_to_label(task2_prediction)})
   
   return output

      
     


