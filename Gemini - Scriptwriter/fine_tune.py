import google.generativeai as genai

from train import training_data
from load_creds import load_creds

creds = load_creds()
genai.configure(credentials=creds)

base_model = [
    m for m in genai.list_models()
    if "createTunedModel" in m.supported_generation_methods][0]
print(base_model)

name = 'plot-writer'
operation = genai.create_tuned_model(
    source_model=base_model.name,
    training_data=training_data,
    id=name,
    epoch_count=100,
    batch_size=2,
    learning_rate=0.001,
)

model = genai.get_tuned_model(f'tunedModels/{name}')
print(model.state)
import time

for status in operation.wait_bar():
  time.sleep(30)

model = genai.GenerativeModel('gemini-pro')