import random
from typing import List, Dict, Set, Optional

class CFG:
    def __init__(self):
        # Task 1: Define CFG components
        self.non_terminals: Set[str] = {'S'}
        self.terminals: Set[str] = {'a', 'b'}
        self.start_symbol: str = 'S'
        self.productions: Dict[str, List[str]] = {'S': ['aSb', 'ε']}
    
    def generate_strings(self, count: int = 10, max_length: int = 10) -> List[str]:
        # Task 2: Generate random strings from the CFG
        generated = []
        for _ in range(count):
            string = self._generate_single_string(max_length)
            if string is not None:
                generated.append(string)
        return generated
    
    def _generate_single_string(self, max_length: int) -> Optional[str]:
        current = self.start_symbol
        steps = 0
        
        while steps < 20:
            non_terminal_pos = -1
            for i, char in enumerate(current):
                if char in self.non_terminals:
                    non_terminal_pos = i
                    break
            
            if non_terminal_pos == -1:
                return '' if current == 'ε' else current if len(current) <= max_length else None
            
            production = random.choice(self.productions[current[non_terminal_pos]])
            
            if production == 'ε':
                current = current[:non_terminal_pos] + current[non_terminal_pos + 1:]
            else:
                current = current[:non_terminal_pos] + production + current[non_terminal_pos + 1:]
            
            if len(current.replace('ε', '')) > max_length:
                return None
            steps += 1
        return None
    
    def show_derivation(self, target: str) -> List[str]:
        # Task 3: Show derivation steps for a target string
        if not self.is_member(target):
            return [f"String '{target}' is not in the language"]
        
        if target == '':
            return ['S', 'ε']
        
        n = target.count('a')
        derivation = ['S']
        current = 'S'
        
        for i in range(n):
            current = current.replace('S', 'aSb', 1)
            derivation.append(current)
        
        if 'S' in current:
            current = current.replace('S', 'ε', 1)
            derivation.append(current)
        
        if 'ε' in current and current != 'ε':
            final = current.replace('ε', '')
            if final != current:
                derivation.append(final)
        
        return derivation
    
    def is_member(self, string: str) -> bool:
        # Task 4: Check if string belongs to the language
        a_count = string.count('a')
        b_count = string.count('b')
        
        return (all(c in 'ab' for c in string) and 
                a_count == b_count and 
                string == 'a' * a_count + 'b' * b_count)


class ExtendedCFG:
    # Task 5 Bonus: Extended CFG for L = {a^n b^n c^n | n ≥ 1}
    def __init__(self):
        self.non_terminals: Set[str] = {'S', 'A', 'B'}
        self.terminals: Set[str] = {'a', 'b', 'c'}
        self.start_symbol: str = 'S'
        self.productions: Dict[str, List[str]] = {
            'S': ['aSBC', 'aBC'],
            'A': ['a'],
            'B': ['b']
        }
    
    def is_member(self, string: str) -> bool:
        if not string:
            return False
        
        a_count = string.count('a')
        b_count = string.count('b')
        c_count = string.count('c')
        
        return (all(c in 'abc' for c in string) and
                a_count == b_count == c_count >= 1 and
                string == 'a' * a_count + 'b' * b_count + 'c' * c_count)


def main():
    cfg = CFG()
    
    # Task 1: Display CFG definition
    print("Task 1: CFG Definition")
    print(f"Non-terminals: {cfg.non_terminals}")
    print(f"Terminals: {cfg.terminals}")
    print(f"Start symbol: {cfg.start_symbol}")
    print("Productions:")
    for nt, prods in cfg.productions.items():
        print(f"  {nt} → {' | '.join(prods)}")
    
    # Task 2: Generate strings
    print("\nTask 2: String Generation")
    generated = cfg.generate_strings(10, 10)
    for i, s in enumerate(generated, 1):
        display_s = s if s else 'ε'
        print(f"{i}. '{display_s}'")
    
    # Task 3: Show derivation for a sample string
    print("\nTask 3: Derivation Example")
    sample_string = "aabb"
    derivation = cfg.show_derivation(sample_string)
    print(f"Derivation for '{sample_string}':")
    for i, step in enumerate(derivation):
        print(f"  {step}" + (" →" if i < len(derivation) - 1 else ""))
    
    # Task 4: Interactive membership testing
    print("\nTask 4: Membership Testing")
    while True:
        test_string = input("Enter string to test (empty to continue): ").strip()
        if not test_string:
            break
        
        result = cfg.is_member(test_string)
        print(f"'{test_string}': {'ACCEPTED' if result else 'REJECTED'}")
        
        if result:
            derivation = cfg.show_derivation(test_string)
            for i, step in enumerate(derivation):
                print(f"  {step}" + (" →" if i < len(derivation) - 1 else ""))
    
    # Task 5: Bonus - Extended CFG
    print("\nTask 5 (Bonus): Extended CFG for L = {a^n b^n c^n | n ≥ 1}")
    extended_cfg = ExtendedCFG()
    
    test_cases = ["abc", "aabbcc", "aaabbbccc", "aabbbc", "abcc", ""]
    for test in test_cases:
        result = extended_cfg.is_member(test)
        display_test = test if test else 'ε'
        print(f"'{display_test}': {'ACCEPTED' if result else 'REJECTED'}")
    
    while True:
        test_string = input("Extended CFG test (empty to finish): ").strip()
        if not test_string:
            break
        result = extended_cfg.is_member(test_string)
        print(f"'{test_string}': {'ACCEPTED' if result else 'REJECTED'}")


if __name__ == "__main__":
    main()
