class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        digits = [[] for _ in range(10)]
        digits[2] = ["a", "b", "c"]
        digits[3] = ["d", "e", "f"]
        digits[4] = ["g", "h", "i"]
        digits[5] = ["j", "k", "l"]
        digits[6] = ["m", "n", "o"]
        digits[7] = ["p", "q", "r", "s"]
        digits[8] = ["t", "u", "v"]
        digits[9] = ["w", "x", "y", "z"]