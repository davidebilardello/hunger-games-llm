import os

from Game import Game

def main():
    os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"

    if not os.getenv("HF_TOKEN") and not os.path.exists(os.path.expanduser("~/.cache/huggingface/token")):
        print("Warning: HF_TOKEN not found. Ensure you have logged in via 'huggingface-cli login'.")

    g = Game()
    g.loop_game()


if __name__ == '__main__':
    main()
