#!/usr/bin/env python3
"""
Word Jumble Solver
==================
A program to solve newspaper word jumble puzzles automatically.

How it works:
1. Solve 4 scrambled words (anagrams)
2. Extract circled letters from solved words
3. Unscramble the final phrase from circled letters
"""


def get_file_lines(filename='/usr/share/dict/words'):
    """
    Return a list of strings from the dictionary file.
    Each line is stripped of whitespace and converted to uppercase.
    
    Args:
        filename: Path to dictionary file
        
    Returns:
        List of uppercase words
    """
    with open(filename) as file:
        lines = [line.strip().upper() for line in file]
    return lines


def sorted_letters(scrambled_letters):
    """
    Return a string with letters sorted in alphabetical order.
    
    Args:
        scrambled_letters: String of scrambled letters
        
    Returns:
        String with same letters in sorted order
        
    Example:
        >>> sorted_letters('DOG')
        'DGO'
    """
    return ''.join(sorted(scrambled_letters))


def create_words_dict(words_list):
    """
    Create a dictionary mapping sorted letters to list of valid words.
    This enables O(1) lookup instead of O(n) linear search.
    
    Args:
        words_list: List of dictionary words
        
    Returns:
        Dictionary where keys are sorted letters, values are lists of words
        
    Example:
        >>> words_dict = create_words_dict(['DOG', 'GOD', 'CAT'])
        >>> words_dict['DGO']
        ['DOG', 'GOD']
    """
    words_dict = {}
    
    # Loop through each word in the dictionary
    for word in words_list:
        # Get the sorted version of the word's letters
        key = sorted_letters(word)
        
        # If this key doesn't exist yet, create an empty list
        if key not in words_dict:
            words_dict[key] = []
        
        # Add this word to the list for this key
        words_dict[key].append(word)
    
    return words_dict


def solve_one_jumble(letters, words_dict):
    """
    Solve a single jumbled word by unscrambling the given letters.
    
    Args:
        letters: String of scrambled letters
        words_dict: Dictionary mapping sorted letters to valid words
        
    Returns:
        List of valid words that match the scrambled letters
        
    Example:
        >>> solve_one_jumble('ILST', words_dict)
        ['LIST', 'SILT', 'SLIT']
    """
    # Sort the scrambled letters to create a lookup key
    key = sorted_letters(letters)
    
    # Look up this key in our dictionary
    # Use .get() with empty list as default in case key doesn't exist
    valid_words = words_dict.get(key, [])
    
    return valid_words


def get_combinations(items, k):
    """
    Generate combinations using nested loops with indices.
    """
    n = len(items)
    result = []
    
    # Add this validation
    if k > n or k < 0:
        return []
    if k == 0:
        return [()]
    
    # We'll use indices to track which items to pick
    indices = list(range(k))  # Start with [0, 1, 2, ..., k-1]
    
    while True:
        # Add current combination
        combo = tuple(items[i] for i in indices)
        result.append(combo)
        
        # Find the rightmost index that can be incremented
        i = k - 1
        while i >= 0 and indices[i] == n - k + i:
            i -= 1
        
        # If no index can be incremented, we're done
        if i < 0:
            break
        
        # Increment this index and reset all indices to its right
        indices[i] += 1
        for j in range(i + 1, k):
            indices[j] = indices[j - 1] + 1
    
    return result


def solve_final_jumble(letters, final_circles, words_dict):
    """
    Solve the final jumbled phrase by unscrambling the given letters.
    
    Args:
        letters: String of scrambled letters from circled positions
        final_circles: List of strings showing word lengths (e.g., ['OOOO', 'OOO'])
        words_dict: Dictionary mapping sorted letters to valid words
        
    Returns:
        List of tuples, each tuple contains words forming a valid phrase
        
    Example:
        >>> solve_final_jumble('TUMUTHT', ['OOOO', 'OOO'], words_dict)
        [('MUTT', 'HUT'), ('TUTH', 'TUM')]
    """
    # Validate that number of circles matches number of letters
    num_circles = sum(len(circles) for circles in final_circles)
    if num_circles != len(letters):
        print('Number of circles does not match number of letters.')
        return []
    
    # If final jumble is just one word, solve it as a single jumble
    num_groups = len(final_circles)
    if num_groups == 1:
        words = solve_one_jumble(letters, words_dict)
        return [(word,) for word in words]
    
    # Multi-word case
    group_sizes = [len(circles) for circles in final_circles]
    valid_phrases = []
    seen = set()
    
    # For 2-word case
    if len(group_sizes) == 2:
        first_word_length = group_sizes[0]
        
        # Use our custom combinations function
        for combo in get_combinations(letters, first_word_length):
            # combo is a tuple like ('M', 'U', 'T', 'T')
            first_word_letters = ''.join(combo)
            
            # Get remaining letters for second word
            remaining = list(letters)
            for letter in combo:
                remaining.remove(letter)
            second_word_letters = ''.join(remaining)
            
            # Check if both form valid words
            first_words = solve_one_jumble(first_word_letters, words_dict)
            second_words = solve_one_jumble(second_word_letters, words_dict)
            
            # If both are valid, add all combinations
            for word1 in first_words:
                for word2 in second_words:
                    phrase = (word1, word2)
                    if phrase not in seen:
                        seen.add(phrase)
                        valid_phrases.append(phrase)
    
    return valid_phrases


def solve_word_jumble(letters, circles, final, words_dict):
    """
    Solve a complete word jumble puzzle.
    
    Args:
        letters: List of scrambled words (e.g., ['ACOME', 'FEROC', ...])
        circles: List of circle patterns (e.g., ['___O_', '__OO_', ...])
                 'O' = circled letter, '_' = not circled
        final: List showing final jumble pattern (e.g., ['OOOOOOO'])
        words_dict: Dictionary mapping sorted letters to valid words
    """
    final_letters = ''
    
    # Solve each of the 4 jumbled words
    for index in range(len(letters)):
        scrambled_letters = letters[index]
        circled_blanks = circles[index]
        
        # Unscramble the letters
        words = solve_one_jumble(scrambled_letters, words_dict)
        
        # Display results
        print(f'Jumble {index+1}: {scrambled_letters} => ', end='')
        if len(words) == 0:
            print('(no solution)')
            continue
        print(f'unscrambled into {len(words)} words: {" or ".join(words)}')
        
        # Extract circled letters from the first valid solution
        for letter, blank in zip(words[0], circled_blanks):
            if blank == 'O':
                final_letters += letter
    
    # Check if we solved any jumbles
    if len(final_letters) == 0:
        print('Did not solve any jumbles, so could not solve final jumble.')
        return
    
    # Solve the final jumble
    final_results = solve_final_jumble(final_letters, final, words_dict)
    
    # Display final results
    print(f'Final Jumble: {final_letters} => ', end='')
    if len(final_results) == 0:
        print('(no solution)')
        return
    print(f'unscrambled into {len(final_results)} possible phrases:')
    for num, result in enumerate(final_results):
        print(f'    Option {num+1}: {" ".join(result)}')


def test_solve_word_jumble_1(words_dict):
    """Test Case 1: Single word final jumble"""
    print('='*20 + ' WORD JUMBLE TEST CASE 1 ' + '='*20)
    # Cartoon prompt: "What her ears felt like at the rock concert: _______."
    letters = ['ACOME', 'FEROC', 'REDDEG', 'YURFIP']
    circles = ['___O_', '__OO_', 'O_O___', 'O__O__']
    final = ['OOOOOOO']  # Final jumble is 1 word with 7 letters
    solve_word_jumble(letters, circles, final, words_dict)


def test_solve_word_jumble_2(words_dict):
    """Test Case 2: Two word final jumble"""
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 2 ' + '='*20)
    # Cartoon prompt: "What a dog house is: ____ ___."
    letters = ['TARFD', 'JOBUM', 'TENJUK', 'LETHEM']
    circles = ['____O', '_OO__', '_O___O', 'O____O']
    final = ['OOOO', 'OOO']  # Final jumble is 2 words with 4 and 3 letters
    solve_word_jumble(letters, circles, final, words_dict)


def test_solve_word_jumble_3(words_dict):
    """Test Case 3: Two word final jumble with multiple solutions"""
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 3 ' + '='*20)
    # Cartoon prompt: "A bad way for a lawyer to learn: _____ and _____."
    letters = ['LAISA', 'LAURR', 'BUREEK', 'PROUOT']
    circles = ['_OOO_', 'O_O__', 'OO____', '__O_OO']
    final = ['OOOOO', 'OOOOO']  # Final jumble is 2 words with 5 and 5 letters
    solve_word_jumble(letters, circles, final, words_dict)


def test_solve_word_jumble_4(words_dict):
    """Test Case 4: No solution for final jumble"""
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 4 ' + '='*20)
    # Cartoon prompt: "Farley rolled on the barn floor: __-______."
    letters = ['TEFON', 'SOKIK', 'NIUMEM', 'SICONU']
    circles = ['__O_O', 'OO_O_', '____O_', '___OO_']
    final = ['OO', 'OOOOOO']  # Final jumble is 2 words with 2 and 6 letters
    solve_word_jumble(letters, circles, final, words_dict)


def main():
    """Main entry point for the program"""
    print("Loading dictionary...")
    words_list = get_file_lines('/usr/share/dict/words')
    print(f"Loaded {len(words_list)} words")
    
    print("\nCreating words dictionary...")
    words_dict = create_words_dict(words_list)
    print(f"Created dictionary with {len(words_dict)} unique letter combinations")
    
    # Test the words_dict with examples
    print("\n" + "="*60)
    print("Testing words_dict lookups:")
    print(f"words_dict['DGO'] = {words_dict.get('DGO', [])}")
    print(f"words_dict['CDEO'] = {words_dict.get('CDEO', [])}")
    print(f"words_dict['ILST'] = {words_dict.get('ILST', [])}")
    print(f"words_dict['EILNST'] = {words_dict.get('EILNST', [])}")
    print("="*60 + "\n")
    
    # Run all test cases
    test_solve_word_jumble_1(words_dict)
    test_solve_word_jumble_2(words_dict)
    test_solve_word_jumble_3(words_dict)
    test_solve_word_jumble_4(words_dict)


if __name__ == '__main__':
    main()

