from Domino import Domino
import argparse
import json
from typing import Tuple, List

def main():
    parser = argparse.ArgumentParser(description="Process a JSON file to calculate the best Mexican Train.")
    parser.add_argument('--source', type=str, help="Path to the JSON file containing domino values.")
    args = parser.parse_args()
    
    try:
      starting_value, dominoes = load_dominoes(args.source)
    except ValueError as e:
      print(e)
      
    best_mexican_train = find_best_mexican_train(starting_value, dominoes)
    
    print(f"Best Mexican Train starting with {starting_value}:")
    print_train(best_mexican_train)
  
def load_dominoes(file_path: str) -> Tuple[str, List[Domino]]:
  try:
    with open(file_path, 'r') as file:
      data = json.load(file)
      starting_value = data['starting_value']
      dominoes = [Domino(d["left"], d["right"]) for d in data["dominoes"]]
      return starting_value, dominoes
  except (json.JSONDecodeError, KeyError) as e:
    raise ValueError(f"Invalid JSON format: {e}")
  except FileNotFoundError:
    raise ValueError(f"File not found: {file_path}")

def find_best_mexican_train(starting_value: int, dominoes: List[Domino]) -> List[Domino]:
  best_train, best_score = [], 0
  
  def backtrack(current_train, open_end, remaining_dominoes):
    nonlocal best_train, best_score
    current_score = sum(d.left + d.right for d in current_train)
    
    if current_score > best_score:
      best_train = current_train[:]
      best_score = current_score
    
    for i, domino in enumerate(remaining_dominoes):
      if open_end in (domino.left, domino.right):
        next_open_end = domino.right if domino.left == open_end else domino.left
        backtrack(
            current_train + [domino], 
            next_open_end,
            remaining_dominoes[:i] + remaining_dominoes[i + 1:]
        )
  
  backtrack([], starting_value, dominoes)
  return best_train

def print_train(train):
    if not train:
        print("The train is empty.")
        return
    
    train_str = " -> ".join(str(domino) for domino in train)
    print(f"{train_str}")

if __name__ == '__main__':
  main()