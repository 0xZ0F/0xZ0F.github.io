import argparse

TO_FIND = "]("

MATCH_REPLACE = {
    "$LINGO$": "LINGO_MD_HERE.md"
    "$BEFOREYOUBEGIN$": "LINGO_MD_HERE.md"
    "$CREDIT$": "LINGO_MD_HERE.md"
    "LINGO": "LINGO_MD_HERE.md"
    "LINGO": "LINGO_MD_HERE.md"
    "LINGO": "LINGO_MD_HERE.md"
    "LINGO": "LINGO_MD_HERE.md"
}

def do_replace(input: str):
    print(f"Input: {input}")
    for match in MATCH_REPLACE:
        start = input.find(match)
        if start != -1:
            return input[:start] + MATCH_REPLACE[match] + input[start + len(match):]
    
    return ""
            

def main(file_in: str) -> None:
    with open(file_in, "r") as fin:
        lines = fin.readlines()
        for index, line in enumerate(lines):
            start = line.find(TO_FIND)
            if start != -1:
                start += 2
                
                end = line[start:].find(")")
                if end == -1:
                    continue
                end += start
                
                lines[index] = line[:start] + do_replace(line[start:end]) + line[end:]
        
        for line in lines:
            print(line, end='')
        
def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str)
    args = parser.parse_args()
    main(args.file_in)

if __name__ == "__main__":
    handle_args()