import numpy
import torch
import random
import json
import nltk
from vacation_functions import find_vacation_by_weather, find_vacation_by_activity
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

def execute_function(function_name, args=None, session_state=None, vacation_spots=None):
    """Execute the specified function with arguments and return its result"""
    if args is None:
        args = {}
    
    if function_name == "find_vacation_by_weather":
        return find_vacation_by_weather(**args, session_state=session_state, vacation_spots=vacation_spots)
    elif function_name == "find_vacation_by_activity":
        return find_vacation_by_activity(**args, session_state=session_state, vacation_spots=vacation_spots)
    elif function_name == "end_conversation":
        end_conversation()
    else:
        return None

def end_conversation():
    print("Thank you for using the vacation chatbot. Have a great day!")
    exit()

def write_exception(input, tag, exception_filename):
    with open(exception_filename) as exception_file:
        if input not in exception_file.read():
            with open(exception_filename, 'a') as exception_file:
                exception_file.write(f'{input}  (Predicted category: {tag})\n')

def chat():
    with open("vacation_spots.json") as file:    
        vacation_spots: list[dict[str,str]] = json.load(file)

    session_state: dict[str, str] = {
        "weather_preference": "",
        "activity_preference": ""
    }

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
                results = outputs.numpy()[0]

            results_index = numpy.argmax(results)
            tag = labels[results_index]
            if results[results_index] > 0.9:
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg["responses"]
                        
                        # Check if this intent has a function to execute
                        if "function" in tg and tg["function"]:
                            function_args = tg.get("function_args", {})
                            function_result = execute_function(tg["function"], function_args, session_state, vacation_spots)
                            print(f"{random.choice(responses)}")
                            print(f"{function_result}")
                        else:
                            print(f"{random.choice(responses)}")
            else:
                print("Please rephrase it!")
                exception_filename = 'exceptions.txt'
                try:
                    write_exception(inp, tag, exception_filename)
                except:
                    file = open(exception_filename, 'x').close()
                    write_exception(inp, tag, exception_filename)

chat()
