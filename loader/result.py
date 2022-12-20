import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, DistilBertModel, AutoModelForSequenceClassification
import gdown
from pathlib import Path
from loader.Task1NN import LangModelWithDense

# from loader.config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# def download_model():
#     # script_dir = os.path.dirname(__file__)
#     path = "./bin/bert_models/model.pt"
#     # abs_file_path = os.path.join(script_dir, rel_path)
#     path = Path(path)

#     url = "https://drive.google.com/uc?id=1ExkkBYxpuWHb_ffUzGbArgLCbay77_Ip"
#     if path.is_file() == False:
#         gdown.download(
#             url=url, output="./bin/bert_models/model.pt", quiet=False)
#     else:
#         print('Model file already downloaded')


# download_model()
bert_model_name = 'distilbert-base-uncased'
task1_2_tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
task1_lang_model = DistilBertModel.from_pretrained(bert_model_name)
task1_model = LangModelWithDense(task1_lang_model)
task1_model.load_state_dict(torch.load('./loader/bin/model1.pt'))
task1_model.to(device)
task1_model.eval()

task2_model = AutoModelForTokenClassification.from_pretrained(bert_model_name, num_labels=13)
task2_model.load_state_dict(torch.load('./loader/bin/model2.pt'))
task2_model.to(device)
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
   # print(pred)
   for p in pred: 
      if p[0]-9<torch.max(p[1:]).item():
         p=p[1:]
         out = inv_eval_ent_dict[torch.argmax(p).item()+1]
      else:
         out = inv_eval_ent_dict[torch.argmax(p).item()]
      # print(p)
      output.append(out)
   return output


def get_encoded(text)->dict:
   task1_2_encoding = task1_2_tokenizer.encode_plus(
      text.lower(),
      return_attention_mask=True,
      return_tensors='pt'
   )
   
   task1_2_encoded = dict(
     input_ids=task1_2_encoding['input_ids'],
     attention_mask=task1_2_encoding['attention_mask']
   )
      
   return task1_2_encoded 

# def remove_padding(x, mask):

#   non_token_idx = x.nonzero()
#   non_token_idx = non_token_idx.reshape(1, len(non_token_idx))
#   # print(non_token_idx)
#   end_ = max(non_token_idx[0])
#   return x[:end_], mask[:end_]


         
def get_word_label_mapping(words, labels):
   words_output = []
   labels_output = []
   
   for word, label  in zip(words, labels):
      if word.startswith('##'):
         words_output.append(words_output.pop()+word[2:])
      else:
         words_output.append(word)
         labels_output.append(label)
   
   return words_output, labels_output

def generate_span(words, labels):
   span = []
   for idx in range(len(words)):
      span.append({'type': labels[idx][2:], 'index':idx}) 
   return span

def get_term_definition(words, labels):
   term =''
   definition = ''
   for i in range(len(words)):
      # if 'definition' in labels[i].lower():
      #    definition +=' '+words[i]
      if 'term' in labels[i].lower():
         term += ' '+words[i]
      elif 'O' != labels[i].lower() and 'term' not in labels[i].lower():
         definition+=' '+words[i]
         
   return term.strip(), definition.strip()

def get_result(texts):
   output = []
   for text in texts:
      
      task1_2_encoded = get_encoded(text)
      input_ids =  task1_2_encoded['input_ids'].flatten()
      attention_mask = task1_2_encoded['attention_mask'].flatten()
      # print(type(input_ids))
      # input_ids, attention_mask = remove_padding(input_ids, attention_mask)
      toks = task1_2_tokenizer.convert_ids_to_tokens(input_ids) 
      print(toks)
      with torch.no_grad():
         
         task1_prediction = task1_model(
            input_ids.unsqueeze(dim=0).to(device),
         attention_mask.unsqueeze(dim=0).to(device)
            )
         
         if task1_prediction >=0.4:
            task2_prediction = task2_model(
             input_ids.unsqueeze(dim=0).to(device),
         attention_mask.unsqueeze(dim=0).to(device)  
            )
             
           

            toks = task1_2_tokenizer.convert_ids_to_tokens(input_ids)
            labels = pred_to_label(task2_prediction.logits[0])
            words, labels = get_word_label_mapping(toks[1:-1], labels)
            span = generate_span(words,labels)
            term, definition = get_term_definition(words, labels)
            
            output.append({'sentence': words, 'span': span,'term':term,'definition': definition})
   print(output)
   return output

      
     


