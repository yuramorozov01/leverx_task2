from functools import total_ordering
from itertools import zip_longest


@total_ordering
class Version:
    def __init__(self, version):
        self._weights = self._generate_weights()
        self.version = self._convert_operand(version)

    def __eq__(self, other):
        other = self._convert_operand(other)
        me, other = self._equalize_length_of_operands(self.version, other)
        return me == other

    def __lt__(self, other):
        other = self._convert_operand(other)
        me, other = self._equalize_length_of_operands(self.version, other)
        return me < other

    def _convert_operand(self, operand):
        '''Convert operand to the specified form.
        If operand is instance of Version class - it doesn't need conversion,
        because version had been converted in an initialize process.
        Conversion example (every digit, letter, word has its own weight):
            - source: "1.0.1b"
            - output: [1, 0, 1 + 2]
            "1 + 2" means that this weight consist of digit 1 and letter b (weight of b is 2)
        '''
        processed_operand = []
        if isinstance(operand, str):
            str_lower_operand = operand.lower().replace('-', '.')
            splitted_operand = str_lower_operand.split('.')
            for operand_part in splitted_operand:
                result_operand_part_weight = 0
                weight = self._weights.get(operand_part)
                if weight is None:
                    if operand_part.isdigit():
                        result_operand_part_weight += int(operand_part)
                    else:
                        result_operand_part_weight += self._weights[operand_part[-1]]
                        result_operand_part_weight += int(operand_part[:-1])
                else:
                    result_operand_part_weight += weight
                processed_operand.append(result_operand_part_weight)
        elif isinstance(operand, Version):
            return operand.version
        return processed_operand

    def _generate_weights(self):
        '''Generating weights for words and letters.
        Letters (in lower case) has weights from 1 to 26 (from letter "a" to letter "z")
        '''
        weights = {
            'alpha': -3,
            'beta': -2,
            'rc': -1,
        }
        for i, letter_ord in enumerate(range(ord('a'), ord('z') + 1)):
            weights[chr(letter_ord)] = i + 1

        for i in range(10):
            weights[str(i)] = i

        return weights

    def _equalize_length_of_operands(self, operand_1, operand_2):
        extended_operands = list(zip(*zip_longest(operand_1, operand_2, fillvalue=0)))
        new_operand_1 = extended_operands[0]
        new_operand_2 = extended_operands[1]

        return new_operand_1, new_operand_2


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0-rc.1', '1.0.0'),
    ]

    for version_1, version_2 in to_test:
        print(version_1, version_2)
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == '__main__':
    main()
