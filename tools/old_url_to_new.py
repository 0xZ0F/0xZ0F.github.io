import argparse

TO_FIND = "]("
REPLACE_WITH = "{% post_url /RECourse/ %}"

# Currently, by design, single chars are assumed to be at the start
# and as such only the first char will be compared.
# Strings, however, will be searched for in the entire line.
EXCLUDE = [
    "{",
    "https"
]

def is_excluded(input: str) -> bool:
    for exclusion in EXCLUDE:
        if 1 == len(exclusion):
            if input[0] == exclusion:
                return True
        else:
            if exclusion in input:
                return True
            
    return False
            

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
                
                if(is_excluded(line[start:end])):
                    continue
                
                lines[index] = line[:start] + REPLACE_WITH + line[end:]
        
        for line in lines:
            print(line, end='')
        
def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', type=str)
    args = parser.parse_args()
    main(args.file_in)

if __name__ == "__main__":
    handle_args()