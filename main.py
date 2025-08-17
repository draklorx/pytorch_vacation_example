import numpy
import torch
import random
import json
import nltk
from train import train, ChatModel
from tools import get_pattern_words, get_labels, create_data, create_vector

# Check if punkt and punkt_tab are already downloaded before downloading
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading punkt_tab...")
    nltk.download('punkt_tab')

with open("intents.json") as file:
    data = json.load(file)

words = get_pattern_words(data["intents"])
labels = get_labels(data["intents"])
training, output = create_data(data["intents"], words, labels)

# Initialize model
input_size = len(training[0])
hidden_size = 8
output_size = len(output[0])
model = ChatModel(input_size, hidden_size, output_size)

try:
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
except FileNotFoundError:
    print("No trained model found, training new model...")
    train(model, training, output)
except Exception as e:
    print(f"Error loading model: {e}")
    print("Training new model...")
    train(model, training, output)

def execute_function(function_name, args=None):
    """Execute the specified function with arguments and return its result"""
    if args is None:
        args = {}
    
    if function_name == "end_conversation":
        end_conversation()
    else:
        return None

def end_conversation():
    exit()

def write_exception(input, tag, probability, exception_filename):
    with open(exception_filename) as exception_file:
        if input not in exception_file.read():
            with open(exception_filename, 'a') as exception_file:
                exception_file.write(f'{input}  (Predicted category: {tag} Confidence: {probability})\n')

def chat():
    print("Start talking with the bot (type /quit to stop and /retrain to train again)!")
    while True:
        inp = input("You: ")
        
        if inp.lower() == "/quit":
            end_conversation()
            break
            
        elif inp.lower() == "/retrain":
            # Recreate the model
            global model
            model = ChatModel(input_size, hidden_size, output_size)
            train(model, training, output)
            print("Model retrained successfully!")
            continue
        else:
            # Get prediction using PyTorch
            with torch.no_grad():
                inputs = torch.FloatTensor(create_vector(inp, words)).unsqueeze(0)
                outputs = model(inputs)
                probs = torch.softmax(outputs, dim=1).numpy()[0]  # <-- Add this line

            results_index = numpy.argmax(probs)
            tag = labels[results_index]

            if probs[results_index] > 0.9:
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg["responses"]
                        
                        # Check if this intent has a function to execute
                        if "function" in tg and tg["function"]:
                            print(f"{random.choice(responses)}    Predicted: {tag} Confidence: {probs[results_index]}")
                            function_args = tg.get("function_args", {})
                            function_result = execute_function(tg["function"], function_args)
                            print(f"{function_result}")
                        else:
                            print(f"{random.choice(responses)}    Predicted: {tag} Confidence: {probs[results_index]}")
            else:
                print("Please rephrase it!")
                exception_filename = 'exceptions.txt'
                try:
                    write_exception(inp, tag, probs[results_index], exception_filename)
                except:
                    file = open(exception_filename, 'x').close()
                    write_exception(inp, tag, probs[results_index], exception_filename)

chat()
