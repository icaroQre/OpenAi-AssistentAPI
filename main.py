import openai
from dotenv import find_dotenv, load_dotenv
import time 
import logging
from datetime import datetime

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

# # ==== Criando a assistente (personal trainer) ====
# personal_trainer_assistant = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions ="You are the best personal trainer and nutritionist.",
#     model=model
# )
# assistant_id = personal_trainer_assistant.id
# print("Assistent ID: " + assistant_id)

# # ==== Criando uma thread com uma menssagem ====
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "How do I get started working out to build muscles?",
#         }
#     ]
# )
# thread_id = thread.id
# print("Thread ID: " + thread_id)

# Salvando os ID's manualmente depois de criados
assistent_id = "asst_y39ZJf8O1cfTcivfimDDH0YW"
thread_id = "thread_JT2WB2N6M7jFrrBkiba9C3NF"

# ==== Criar uma menssagem ====
message = "how much water I need to drink?"
messagem = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message,
)

# ==== Run assistente ====
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistent_id,
    instructions="Please address the user as Jamas Bond"
)

# Função para tratar intervalo de tempo durante o processamento da pergunta e responsta
def wait_for_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Recebe as mensagens quando Run estiver completa
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistent Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info(f"Waiting for Run to complete...")
        time.sleep(sleep_interval)

# ==== Executando ====   
wait_for_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Logs da execução ==== 
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data}")