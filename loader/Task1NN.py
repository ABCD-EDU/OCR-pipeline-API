import torch.nn as nn
import torch.nn.functional as F
import torch
import pytorch_lightning as pl
import json

device = torch.device("cuda")

# with open('./loader/config/config.json', 'r') as f:
#     config = json.load(f)



class LangModelWithDense(pl.LightningModule):
    def __init__(self, lang_model, ):

        super(LangModelWithDense, self).__init__()
       
        self.lang_model = lang_model
  

        self.hidden = nn.Linear(self.lang_model.config.hidden_size,
                                self.lang_model.config.hidden_size)

        self.classifier = nn.Linear(
            self.lang_model.config.hidden_size, 1)

        torch.nn.init.xavier_uniform_(self.hidden.weight)
        torch.nn.init.xavier_uniform_(self.classifier.weight)


        self.dropout = nn.Dropout(0.2)
        
    def forward(self, input_ids, attention_mask):
        output = self.lang_model(input_ids, attention_mask=attention_mask)
        pooled_output = torch.mean(output.last_hidden_state, 1)

        pooled_output = self.hidden(pooled_output)
        # pooled_output = self.dropout(pooled_output)
        pooled_output = F.relu(pooled_output)

        output = self.classifier(pooled_output) 
        output = torch.sigmoid(output)
      
        return output