
import argparse
from parser import parse_and_translate

def main():
    parser = argparse.ArgumentParser(description="Учебный конфигурационный язык -> TOML")
    parser.add_argument("--input", required=True, help="Путь к входному файлу")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    result = parse_and_translate(text)
    print(result)

if __name__ == "__main__":
    main()
