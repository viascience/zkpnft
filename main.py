import hashlib
import json
import random

import numpy as np
import typer
from PIL import Image

prover = typer.Typer()


def random_sequence():
    randomlist = []

    for i in range(0, 5):
        n = random.randint(1, 30)
        randomlist.append(n)

    return randomlist


def hash_sequences(shuffled_list: list):
    # it is needed to return a seed value per user
    # repeated numbers of a sequence are exfiltrated therefore random noise is needed before hash
    hashed_list = []
    for sequence in shuffled_list:

        values = []

        for value in sequence:

            h = hashlib.new("sha256")
            h.update(str(value).encode())

            values.append(h.hexdigest())

        hashed_list.append(values)

    return hashed_list


def mod256(hashed_list: list):

    mod256_list = []
    for sequence in hashed_list:

        values = []

        for value in sequence:

            values.append(int(value, 16) % 255)

        mod256_list.append(values)

    return mod256_list


def sequence_scrambler(list_random_sequences: list, list_given_sequences: list):

    combined_list = list_random_sequences + list_given_sequences

    random.shuffle(combined_list)

    return combined_list


def noise_addition(list_given_sequences, noise):
    list_given_sequences_noise = []
    noise_seeds = {}
    for num, sequence in enumerate(list_given_sequences):
        if noise is not None:
            n = noise
        else:
            n = random.randint(1, 30)

        noise_seeds[f"user_{num}"] = n

        random.seed(n)
        noise = random.randint(1, 5)

        noise_sequence = [i + noise for i in sequence]

        list_given_sequences_noise.append(noise_sequence)

    return list_given_sequences_noise, noise_seeds


@prover.command()
def main(dict_of_sequences_str: str, noise=None):

    dict_of_sequences = json.loads(dict_of_sequences_str)

    typer.echo(dict_of_sequences)

    n_random_sequences = 3

    list_random_sequences = [random_sequence() for i in range(n_random_sequences)]

    list_given_sequences = [dict_of_sequences[user] for user in dict_of_sequences]

    list_given_sequences_noise, noise_seeds = noise_addition(
        list_given_sequences, noise
    )

    shuffled_list = sequence_scrambler(
        list_random_sequences, list_given_sequences_noise
    )

    typer.echo(f"Shuffled list: \n {shuffled_list}")

    hashed_list = hash_sequences(shuffled_list)

    typer.echo(hashed_list)

    mod_hashes = mod256(hashed_list)

    typer.echo(mod_hashes)

    mod_hashes_array = np.array([np.array(xi).astype(np.uint8) for xi in mod_hashes])

    typer.echo(mod_hashes_array)

    img = Image.fromarray(mod_hashes_array)

    # img.show()

    img.save("./image/proof.png")

    typer.echo(noise_seeds)

    return img

    # padded_lists = padding_image(mod_hashes)

    # image = create_image(padded_lists)

    # show(image)


if __name__ == "__main__":
    # Example call:
    # python main.py '{"user1": [6, 7, 9, 10, 12], "user2": [1, 2, 3, 8, 7]}'
    # Proof as image:
    # [[177,  34, 231,   2,  88], [169, 137, 213,  11, 215], [ 67, 169,  23, 165, 109], [143, 165, 165,   2,  11], [ 81, 143, 237, 137, 169]]
    # Noise to create verification sequence {'user_0': 1, 'user_1': 19}
    prover()
