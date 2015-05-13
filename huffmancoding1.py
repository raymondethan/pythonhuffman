import queue
import timeit

class Node:

    def __init__ (self, left, right, freq, value = None):
        self.freq = freq
        self.value = value
        if left and left.freq and right and right.freq:
            self.freq = left.freq + right.freq
        self.left = left
        self.right = right

    def __gt__(self, node):
        return self.freq > node.freq

    def __eq__(self, node):
        return self.value == node.value and self.freq == node.freq


def read_file(f):
    with open(f, "r") as input_file:
        return input_file.read()

#Divides the code into segments of the specified length
#Used for inputs with varying frequencies
def create_segments(input, n):
    return [input[i:i+n] for i in range(0, len(input), n)]

#Calculates the frequencies of each symbol for each segment
def create_freq(input, n):
    freq = {}
    i = 0
    for segment in input:
        for j in range(0, len(segment), n):
            if not i in freq:
                freq[i] = {}
            if segment[j:j+n] in freq[i]:
                freq[i][segment[j:j+n]] += 1
            else:
                freq[i][segment[j:j+n]] = 1
        i += 1
    return freq

#Creates a list of trees for each segment
def create_tree(freq):
    result = []
    for segment in freq:
        priority_queue = queue.PriorityQueue()
        #Creates a node for each symbol
        for character in freq[segment]:
            new_node = Node(None, None, freq[segment][character], character)
            priority_queue.put((new_node.freq, new_node))
        #combines the smallest nodes until the tree includes all nodes
        while priority_queue.qsize() > 1:
            min1 = priority_queue.get()
            min2 = priority_queue.get()
            new_node = Node(min1[1], min2[1], min1[1].freq + min2[1].freq, None)
            priority_queue.put((new_node.freq, new_node))
        result.insert(len(result), priority_queue)
    return result


def create_code(node, code_dict, code):
    if node.left is None and node.right is None:
        code_dict[node.value] = str(code)
    else:
        if node.left:
            create_code(node.left, code_dict, code[:]+'0')
        if node.right:
            create_code(node.right, code_dict, code[:]+'1')

#Creates a huffman code for each segment of the input
def huffcode(input, segment_length, character_length):
    segment = create_segments(input, segment_length)
    segment = create_freq(segment, character_length)
    segment = create_tree(segment)
    result = []
    for q in segment:
        result.insert(len(result), callHuffcode(q))
    return result

def callHuffcode(q):
    root = q.get()[1]
    code_dict = {}
    create_code(root, code_dict, '')
    return code_dict

#Creates the encoded message using the created huffman code
def encode_message(input, segment_length, character_length, encoding):
    output = ""
    seg_number = 0
    for i in range(0, len(input), segment_length):
        for j in range(0, min(segment_length, len(input) - i), character_length):
            if segment_length - j < character_length:
                output += encoding[seg_number][input[j+i:i+segment_length]]
            else:
                output += encoding[seg_number][input[j+i:j+i+character_length]]
        seg_number += 1
    return output

def getCodeLength(encoding):
    length = 0
    for segment in encoding:
        length += len(segment)
    return length

def getAverageCodeLength(encoding):
    length = 0
    num = 0
    for segment in encoding:
        for key in segment:
            num += 1
            length += len(segment[key])
    return float(length)/num

def test(file, segment_size, char_size, printCode = False):
    input = read_file(file)
    huff_code_time = timeit.timeit(lambda: huffcode(input, segment_size, char_size), number = 1)
    code = huffcode(input, segment_size, char_size)
    encode_time = timeit.timeit(lambda: encode_message(input, segment_size, char_size, code), number = 1)
    output = encode_message(input, segment_size, char_size, code)
    if printCode:
        print(code)
    print("Test for file " + file + " of symbol size " + str(char_size) + " and segment size " + str(segment_size))
    print("Size of input: " + str(len(input)) + " characters")
    print("Number of differently encoded symbols: " + str(getCodeLength(code)))
    print("Average symbol code length: " + str(getAverageCodeLength(code)) + " bits")
    print("Size of encoded message: " + str(len(output)) + " bits")
    print("Time to create Huffman Code: " + str(huff_code_time) + " seconds")
    print("Time to encode message: " + str(encode_time) + " seconds")
    print("Total time: " + str(huff_code_time+encode_time) + " seconds")

def main():
    test("test.txt", 100, 1, True)
    print()
    test("englishpaper.txt", 1000000, 1)
    print()
    test("englishpaper.txt", 1000000, 2)
    print()
    test("englishpaper.txt", 1000000, 3)
    print()
    test("englishpaper.txt", 1000000, 4)
    print()
    test("englishpaper.txt", 10, 1)
    print()
    test("englishpaper.txt", 100, 1)
    print()
    test("englishpaper.txt", 1000, 1)
    print()
    test("englishpaper.txt", 10000, 1)
    print()
    test("englishpaper.txt", 100, 3)
    print()
    test("englishpaper.txt", 1000, 3)
    print()
    test("englishpaper.txt", 10000, 3)
    print()
    test("thunderroad.txt", 100, 1)
    print()
    test("thunderroad.txt", 500, 1)
    print()
    test("thunderroad.txt", 1000000, 1)
    print()
    test("limitedchars.txt", 10000, 1)
    print()
    test("limitedchars.txt", 10000, 2)
    print()
    test("limitedchars.txt", 10000, 4)
    print()

main()

