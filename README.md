# Word Jumble Solver

A Python program to automatically solve newspaper word jumble puzzles using data structures and algorithms.

## 📋 What is Word Jumble?

Word Jumble is a popular newspaper puzzle with:
1. **4 scrambled words** - Each is an anagram to unscramble
2. **Circled letters** - Certain positions in solved words are marked
3. **Final jumble** - A phrase made from all the circled letters (often a pun!)

## 🎯 Project Goals

Implement two main functions:

### 1. `solve_one_jumble(letters, words_dict)`
Unscramble a single word from scrambled letters.

**Example:**
```python
solve_one_jumble('ILST', words_dict)
# Returns: ['LIST', 'SILT', 'SLIT']
```

### 2. `solve_final_jumble(letters, final_circles, words_dict)`
Unscramble the final phrase (can be multiple words).

**Example:**
```python
solve_final_jumble('TUMUTHT', ['OOOO', 'OOO'], words_dict)
# Returns: [('MUTT', 'HUT'), ('TUTH', 'TUM')]
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Unix-based system (Mac/Linux) with `/usr/share/dict/words`

### Running the Program

```bash
python3 wordjumble.py
```

## 📊 Test Cases

### Test Case 1: Single Word Final
```
Jumble 1: ACOME => CAMEO
Jumble 2: FEROC => FORCE
Jumble 3: REDDEG => DREDGE
Jumble 4: YURFIP => PURIFY
Final: ERCDEPI => PIERCED
```

### Test Case 2: Two Word Final
```
Jumble 1: TARFD => DRAFT
Jumble 2: JOBUM => JUMBO
Jumble 3: TENJUK => JUNKET
Jumble 4: LETHEM => HELMET
Final: TUMUTHT => HUT MUTT (or MUTH TUT, TUM TUTH)
```

## 💡 Implementation Hints

### Data Structure Strategy
Create a hash table that maps sorted letters to words:
```python
words_dict = {
    'DGO': ['DOG', 'GOD'],
    'CDEO': ['CODE', 'COED'],
    'ILST': ['LIST', 'SILT', 'SLIT']
}
```

This enables **O(1) lookup** instead of O(n) linear search!

### Algorithm Approach

1. **For single words:**
   - Sort the scrambled letters
   - Look up in words_dict
   - Return all matches

2. **For multi-word phrases:**
   - Use `itertools.combinations` to partition letters
   - Filter by required word lengths
   - Validate each word exists in dictionary

## 🔧 TODO List

- [ ] Implement `create_words_dict()` function
- [ ] Implement `solve_one_jumble()` function
- [ ] Test with single word jumbles
- [ ] Implement `solve_final_jumble()` for multi-word phrases
- [ ] Handle edge cases (no solution, multiple solutions)

## 📝 Circle Notation

Circles are represented as strings:
- `O` (letter "oh") = letter IS in the final jumble
- `_` (underscore) = letter is NOT in the final jumble

**Example:**
```python
circles = ['___O_', '__OO_', 'O_O___', 'O__O__']
#          CAMEO    FORCE    DREDGE   PURIFY
#             ↓       ↓↓      ↓ ↓      ↓  ↓
# Circled:   E       RC      D E      P  I
# Final letters: ERCDEPI
```

## 🎨 Expected Output Format

```
==================== WORD JUMBLE TEST CASE 1 ====================
Jumble 1: ACOME => unscrambled into 1 words: CAMEO
Jumble 2: FEROC => unscrambled into 1 words: FORCE
Jumble 3: REDDEG => unscrambled into 2 words: DREDGE or GEDDER
Jumble 4: YURFIP => unscrambled into 1 words: PURIFY
Final Jumble: ERCDEPI => unscrambled into 1 possible phrases:
    Option 1: PIERCED
```

## 📚 Resources

- Dictionary file: `/usr/share/dict/words`
- Python `itertools.combinations` for multi-word solving
- Hash tables for efficient word lookup

## 🏆 Success Criteria

- ✅ Solve all 4 single word jumbles in each test case
- ✅ Solve final jumble for Test Case 1 (single word)
- ✅ Solve final jumble for Test Cases 2-3 (multi-word phrases)
- ✅ Handle Test Case 4 (no valid solution)

Good luck! 🎲

