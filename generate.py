"""
This script is used to generate answers for a set of instructions using OpenAI's GPT-4 model.
It extracts questions_to_generate_answers from a file, generates answers for each question, and stores the question-answer pairs in a JSON file.
The script iterates over 26 principle files, generating 10 answers for each question in each file.
The generated JSON files are stored in the 'gpt4' directory.
"""
import os
from openai import OpenAI
import json

API_KEY = 'OPENAI_KEY'
DEFAULT_GPT_MODEL = "gpt-4-1106-preview"
PRINCIPLES_DIR = "principles"
RESULTS_DIR = "gpt4"

client = OpenAI(api_key=os.environ[API_KEY])


def generate_answers(questions_to_generate_answers, gpt_model=DEFAULT_GPT_MODEL):
    """
    Generate answers for a given set of questions_to_generate_answers
    """
    return [
        client.chat.completions.create(
            messages=[{"role": "user", "content": question}], model=gpt_model
        )
        .choices[0]
        .message.content
        for question in questions_to_generate_answers
    ]


def extract_questions_from_file(file_path):
    """
    Extract questions_to_generate_answers from a given file
    """
    with open(file_path) as file:
        lines = file.readlines()
    return [line for line in lines if line.strip().lower().startswith("question")]


def save_results_to_file(principle_id, question_answer_save_result):
    """
    Save the generated questions_to_generate_answers and answers into a JSON file
    """
    json_data = json.dumps(question_answer_save_result, indent=4)
    folder_path = RESULTS_DIR
    filename = f'principle_{principle_id}.json'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as file:
        file.write(json_data)


if __name__ == "__main__":
    for i in range(1, 27):
        principle_file_path = os.path.join(PRINCIPLES_DIR, f"principle_{i}.txt")
        questions = extract_questions_from_file(principle_file_path)
        question_answer_pairs = [{"instruction": question, "output": answer} for question, answer in zip(questions, generate_answers(questions))]
        save_results_to_file(i, question_answer_pairs)
