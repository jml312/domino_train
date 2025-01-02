from Domino import Domino
import argparse
import json
from typing import Tuple, List

def main():
  parser = argparse.ArgumentParser(description="Process a JSON file to calculate the best Mexican Train.")
  parser.add_argument('--source', type=str, help="Path to the JSON file containing domino values.")
  parser.add_argument('--start_value', type=int, help="Start value for the Mexican Train.")
  args = parser.parse_args()
  
  try:
    start_value = args.start_value
    dominoes = load_dominoes(args.source)
  except ValueError as e:
    print(e)
    return
    
  best_train = find_best_train(start_value, dominoes)
  
  print(f"Best Mexican Train for start value {start_value} ({len(best_train)}/16 dominoes):")
  print_train(best_train)
  
def load_dominoes(file_path: str) -> List[Domino]:
  try:
    with open(file_path, 'r') as file:
      data = json.load(file)
      dominoes = [Domino(d["left"], d["right"]) for d in data["dominoes"]]
      
      if len(dominoes) != 16:
        raise ValueError("There should be 16 dominoes")
      
      return dominoes
  except (json.JSONDecodeError, KeyError) as e:
    raise ValueError(f"Invalid JSON format: {e}")
  except FileNotFoundError:
    raise ValueError(f"File not found: {file_path}")

def find_best_train(start_value: int, dominoes: List[Domino]) -> List[Domino]:
  best_train, best_score = [], 0
  
  def backtrack(current_train, open_end, remaining_dominoes):
    nonlocal best_train, best_score
    current_score = len(current_train)
    
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
  
  backtrack([], start_value, dominoes)
  return flip_dominoes_in_train(start_value, best_train)

def flip_dominoes_in_train(start_value: int, train: List[Domino]) -> List[Domino]:
  if not train: 
    return train

  flipped_train = []
  prev = start_value

  for domino in train:
    if domino.left != prev:
      domino = domino.flip()
    flipped_train.append(domino)
    prev = domino.right

  return flipped_train 

def print_train(train):
    if not train:
        print("The train is empty.")
        return
    
    train_str = " -> ".join(str(domino) for domino in train)
    print(f"{train_str}")

if __name__ == '__main__':
  main()