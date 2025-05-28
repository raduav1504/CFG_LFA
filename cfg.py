import random
from typing import List, Dict, Set, Tuple, Optional

class CFG:
    """Context-Free Grammar implementation for S → aSb | ε"""
    
    def __init__(self):
        # Task 1: Define CFG components
        self.non_terminals: Set[str] = {'S'}
        self.terminals: Set[str] = {'a', 'b'}
        self.start_symbol: str = 'S'
        self.productions: Dict[str, List[str]] = {
            'S': ['aSb', 'ε']  # S → aSb | ε
        }
    
    def generate_strings(self, count: int = 10, max_length: int = 10) -> List[str]:
        """Task 2: Generate random strings from the CFG"""
        generated = []
        
        for _ in range(count):
            string = self._generate_single_string(max_length)
            if string is not None:
                generated.append(string)
        
        return generated
    
    def _generate_single_string(self, max_length: int) -> Optional[str]:
        """Generate a single string using random derivation"""
        current = self.start_symbol
        steps = 0
        max_steps = 20  # Prevent infinite loops
        
        while steps < max_steps:
            # Find leftmost non-terminal
            non_terminal_pos = -1
            for i, char in enumerate(current):
                if char in self.non_terminals:
                    non_terminal_pos = i
                    break
            
            # If no non-terminals, we're done
            if non_terminal_pos == -1:
                if current == 'ε':
                    return ''
                return current if len(current) <= max_length else None
            
            # Get the non-terminal to expand
            non_terminal = current[non_terminal_pos]
            
            # Choose random production
            production = random.choice(self.productions[non_terminal])
            
            # Apply production
            if production == 'ε':
                current = current[:non_terminal_pos] + current[non_terminal_pos + 1:]
            else:
                current = current[:non_terminal_pos] + production + current[non_terminal_pos + 1:]
            
            # Check length constraint
            if len(current.replace('ε', '')) > max_length:
                return None
            
            steps += 1
        
        return None
    
    def show_derivation(self, target: str) -> List[str]:
        """Task 3: Show derivation steps for a target string"""
        if not self.is_member(target):
            return [f"String '{target}' is not in the language"]
        
        # For this specific grammar S → aSb | ε, we can construct derivation directly
        # The language is {a^n b^n | n ≥ 0}
        if target == '':
            return ['S', 'ε']
        
        # Count the number of a's (which equals number of b's for valid strings)
        n = target.count('a')
        
        derivation = ['S']
        current = 'S'
        
        # Apply S → aSb production n times
        for i in range(n):
            current = current.replace('S', 'aSb', 1)
            derivation.append(current)
        
        # Apply S → ε production once
        if 'S' in current:
            current = current.replace('S', 'ε', 1)
            derivation.append(current)
        
        # Clean up ε if present
        if 'ε' in current and current != 'ε':
            final = current.replace('ε', '')
            if final != current:
                derivation.append(final)
        
        return derivation
    
    def is_member(self, string: str) -> bool:
        """Task 4: Check if string belongs to the language"""
        # For S → aSb | ε, the language is {a^n b^n | n ≥ 0}
        # Count a's and b's
        a_count = string.count('a')
        b_count = string.count('b')
        
        # Check if string contains only a's and b's
        if not all(c in 'ab' for c in string):
            return False
        
        # Check if equal number of a's and b's
        if a_count != b_count:
            return False
        
        # Check if all a's come before all b's
        if string != 'a' * a_count + 'b' * b_count:
            return False
        
        return True


class ExtendedCFG:
    """Task 5 Bonus: Extended CFG for L = {a^n b^n c^n | n ≥ 1}"""
    
    def __init__(self):
        # Note: This language is actually context-sensitive, not context-free
        # We simulate it with a context-free grammar that doesn't truly generate it
        self.non_terminals: Set[str] = {'S', 'A', 'B'}
        self.terminals: Set[str] = {'a', 'b', 'c'}
        self.start_symbol: str = 'S'
        
        # This is a simplified representation - the actual language requires
        # context-sensitive rules to ensure equal counts of a, b, and c
        self.productions: Dict[str, List[str]] = {
            'S': ['aSBC', 'aBC'],  # Generate at least one of each
            'A': ['a'],
            'B': ['b'], 
        }
    
    def is_member(self, string: str) -> bool:
        """Check if string is in L = {a^n b^n c^n | n ≥ 1}"""
        if not string:
            return False
        
        # Count each character
        a_count = string.count('a')
        b_count = string.count('b')
        c_count = string.count('c')
        
        # Check if string contains only a's, b's, and c's
        if not all(c in 'abc' for c in string):
            return False
        
        # Check if equal counts and at least 1 of each
        if not (a_count == b_count == c_count >= 1):
            return False
        
        # Check if pattern is a^n b^n c^n
        expected = 'a' * a_count + 'b' * b_count + 'c' * c_count
        return string == expected


def main():
    cfg = CFG()
    # Task 1: Display CFG definition
    print("\nTask 1: CFG Definition")
    print("-" * 30)
    print(f"Non-terminals: {cfg.non_terminals}")
    print(f"Terminals: {cfg.terminals}")
    print(f"Start symbol: {cfg.start_symbol}")
    print("Productions:")
    for nt, prods in cfg.productions.items():
        print(f"  {nt} → {' | '.join(prods)}")
    
    # Task 2: Generate strings
    print("\nTask 2: String Generation")
    print("-" * 30)
    generated = cfg.generate_strings(10, 10)
    print("Generated strings:")
    for i, s in enumerate(generated, 1):
        display_s = s if s else 'ε (empty string)'
        print(f"  {i}. '{display_s}'")
    
    # Task 3: Show derivation for a sample string
    print("\nTask 3: Derivation Example")
    print("-" * 30)
    sample_string = "aabb"
    derivation = cfg.show_derivation(sample_string)
    print(f"Derivation for '{sample_string}':")
    for i, step in enumerate(derivation):
        if i < len(derivation) - 1:
            print(f"  {step} →")
        else:
            print(f"  {step}")
    
    # Show another example with empty string
    print(f"\nDerivation for empty string:")
    empty_derivation = cfg.show_derivation("")
    for i, step in enumerate(empty_derivation):
        if i < len(empty_derivation) - 1:
            print(f"  {step} →")
        else:
            print(f"  {step}")
    
    # Task 4: Interactive membership testing
    print("\nTask 4: Membership Testing")
    print("-" * 30)
    print("Enter strings to test (press Enter with empty string to continue):")
    
    while True:
        test_string = input("Enter string to test: ").strip()
        if not test_string:
            break
        
        result = cfg.is_member(test_string)
        status = "ACCEPTED" if result else "REJECTED"
        print(f"String '{test_string}': {status}")
        
        if result:
            print("Derivation:")
            derivation = cfg.show_derivation(test_string)
            for i, step in enumerate(derivation):
                if i < len(derivation) - 1:
                    print(f"  {step} →")
                else:
                    print(f"  {step}")
        print()
    
    # Task 5: Bonus - Extended CFG
    print("\nTask 5 (Bonus): Extended CFG for L = {a^n b^n c^n | n ≥ 1}")
    print("-" * 60)
    extended_cfg = ExtendedCFG()
    
    print("Extended CFG Definition:")
    print(f"Non-terminals: {extended_cfg.non_terminals}")
    print(f"Terminals: {extended_cfg.terminals}")
    print(f"Start symbol: {extended_cfg.start_symbol}")
    print("Productions:")
    for nt, prods in extended_cfg.productions.items():
        print(f"  {nt} → {' | '.join(prods)}")
    
    print("\nTesting extended CFG:")
    test_cases = ["abc", "aabbcc", "aaabbbccc", "aabbbc", "abcc", ""]
    
    for test in test_cases:
        result = extended_cfg.is_member(test)
        status = "ACCEPTED" if result else "REJECTED"
        display_test = test if test else 'ε (empty)'
        print(f"String '{display_test}': {status}")
    
    print("\nInteractive testing for extended CFG:")
    print("Enter strings to test (press Enter with empty string to finish):")
    
    while True:
        test_string = input("Enter string for extended CFG: ").strip()
        if not test_string:
            break
        
        result = extended_cfg.is_member(test_string)
        status = "ACCEPTED" if result else "REJECTED"
        print(f"String '{test_string}': {status}")
    

The language L = {a^n b^n c^n | n ≥ 1} is NOT context-free!

This language is context-sensitive and cannot be generated by any 
context-free grammar. This is proven by the pumping lemma for 
context-free languages.

The CFG provided above is a simplified representation that doesn't 
actually generate the correct language. A true implementation would 
require context-sensitive grammar rules or additional constraints 
beyond what CFGs can express.

The recognizer function works by directly checking the pattern 
rather than using grammar derivation, which is why it appears 
to work correctly despite the theoretical limitation.


if __name__ == "__main__":
    main()
