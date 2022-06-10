import sys
import typer
import random
import hashlib
import json

import numpy as np
from PIL import Image


def hash_sequences(sequence_noise: list):

  values = []
    
  for value in sequence_noise:

    h = hashlib.new('sha256')
    h.update(str(value).encode())
      
    values.append(h.hexdigest())
      
  return values
    
def mod256(hashed_list: list):     

  values = []
    
  for value in hashed_list:

    values.append(int(value,16) % 255)
       
  return values    
 
def noise_addition(sequence, noise):

  random.seed(noise)
  noise = random.randint(1,5)
    
  noise_sequence = [i + noise for i in sequence]
       
  return noise_sequence
  

def main(sequence: str, noise: int):

  typer.echo(sequence)
  
  sequence = json.loads(sequence)
  
  sequence_noise = noise_addition(sequence, noise)
    
  hashed_list = hash_sequences(sequence_noise)

  typer.echo(f"Hash list: \n {hashed_list}")
  
  mod_hashes = mod256(hashed_list)
  
  typer.echo(mod_hashes)
  
  return mod_hashes
  
  


if __name__ == "__main__":
  # Example call:
  # python verification_hash.py '[6, 7, 9, 10, 12]' 1

  typer.run(main)
