class CyclicRange:
    def __init__(self, start, stop, step=1, repeats=1):
        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
        self._current = start
        self._cycle = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cycle >= self._repeats:
            raise StopIteration

        result = self._current
        self._current += self._step

        if self._current >= self._stop:
            self._current = self._start
            self._cycle += 1

        return result


def main():
    print("CyclicRange(1, 4, repeats=3):")
    for num in CyclicRange(1, 4, repeats=3):
        print(num, end=" ")
    print()

    print("\nCyclicRange(0, 10, step=3, repeats=2):")
    for num in CyclicRange(0, 10, step=3, repeats=2):
        print(num, end=" ")
    print()

    result = list(CyclicRange(5, 8, repeats=2))
    print("\nСписок: " + str(result))

    total = sum(CyclicRange(1, 5, repeats=2))
    print("Сума: " + str(total))


if __name__ == "__main__":
    main()