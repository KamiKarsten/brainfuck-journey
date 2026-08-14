import sys

MEMORY_SIZE=30000
CELL_MAX_VALUE=255

def find_bracket_pairs(code):
    bracket_pairs = {}
    unmatched_opening_brackets = []

    for position, instruction in enumerate(code):
        if instruction == "[":
            # save position of opening bracket until we find its matching ']'.
            unmatched_opening_brackets.append(position)

        elif instruction == "]":
            # ']' without an opening bracket is invalid.
            if not unmatched_opening_brackets:
                raise SyntaxError(
                    f"Missing '[' for ']' at position {position}"
                )

            # save opening and closing postions for bracket pairs.
            # get opening bracket position from the most recent '['
            opening_position = unmatched_opening_brackets.pop()
            
            #save opening position to brackets pair
            bracket_pairs[position] = opening_position
            
            #save closing position to brackets pair
            bracket_pairs[opening_position] = position


    if unmatched_opening_brackets:
        # remaining '[' without a closing bracket is invalid.
        raise SyntaxError(
            f"Missing ']' for '[' at position {unmatched_opening_brackets[-1]}"
        )

    return bracket_pairs

def run(code):
    memory = [0] * MEMORY_SIZE
    data_pointer = 0
    instruction_pointer = 0
    
    bracket_pairs = find_bracket_pairs(code)
    
    while instruction_pointer < len(code):
        instruction = code[instruction_pointer]

        match instruction:
            case ">":
                data_pointer += 1
                
                if (data_pointer) >= len(memory):
                    raise RuntimeError("Data pointer moved outside the memory")
            case "<":
                data_pointer -= 1

                if data_pointer < 0:
                    raise RuntimeError("Data pointer moved outside the memory")
            case "+":
                memory[data_pointer] = (memory[data_pointer] +1) % (CELL_MAX_VALUE + 1)
            case "-":
                memory[data_pointer] = (memory[data_pointer] -1) % (CELL_MAX_VALUE + 1)
            case ".":
                output_character = chr(memory[data_pointer])
                print(output_character, end="")
            case ",":
                input_character = input()[0]
                memory[data_pointer] = ord(input_character)
            case "[":
                if memory[data_pointer] == 0:
                    instruction_pointer = bracket_pairs[instruction_pointer]
            case "]":
                if memory[data_pointer] != 0:
                    instruction_pointer = bracket_pairs[instruction_pointer]
            
        instruction_pointer +=1

def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <file.bf>")
        return

    filename = sys.argv[1]

    with open(filename, "r") as file:
        code = file.read()

    run(code)


if __name__ == "__main__":
    main()