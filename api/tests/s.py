from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def set_default_value(
    data: dict[K, V],
    key: K,
    new_value: V,
) -> tuple[K, V]:
    value = data.get(key)
    if not value:
        data[key] = new_value
    return key, data[key]


def get_default_value(
    data: dict[K, V],
    key: K,
    default_value: V,
) -> V:
    if val := data.get(key):
        return val
    return default_value


def main() -> None:
    ages = {
        "John": 30,
        "Kate": 33,
    }
    name, age = set_default_value(ages, "Kate", 30)
    print("res:", name, age)
    print(ages)
    res = set_default_value(ages, "Bob", 22)
    print("res:", res)
    print(ages)

    kyle_res = get_default_value(ages, "Kyle", 16)
    print("kyle res:", kyle_res)
    print(ages)
    bob_res = get_default_value(ages, "Bob", 7)
    print("bob res:", bob_res)
    print(ages)


if __name__ == "__main__":
    main()