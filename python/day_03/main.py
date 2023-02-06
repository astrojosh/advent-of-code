def main(input_data: str) -> tuple[int, int]:

    data = input_data.splitlines()

    return tuple(
        map(
            lambda e: sum(
                ord(x) - 38 - 58 * (ord(x) > 90)
                for a, b, c in e
                for x in set(a)
                if x in b and x in c
            ),
            [
                map(
                    lambda y: [t := y[: (s := len(y) // 2)], y[s:], t],
                    data,
                ),
                zip(data[::3], data[1::3], data[2::3]),
            ],
        )
    )
