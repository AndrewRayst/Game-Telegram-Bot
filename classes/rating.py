from typing import List


class Rating:
    def __init__(self, arr: List):
        self.__arr: List = arr
        self.length: int = len(arr)
        self.__cur_index: int = 0

        self.cur_page = 1
        self.total_pages = self.length // 5

    def __str__(self) -> str:
        rating_text = '\n'.join(
            [
                f"{i_index + 1}) {i_item['name']}: {i_item['topCriticScore']}⭐"
                for i_index, i_item in enumerate(self.get())
            ]
        )

        return f'Рейтинг игр. Страница {self.cur_page} из {self.total_pages}\n' + rating_text

    def get(self) -> List:
        return self.__arr[self.__cur_index:self.__cur_index + 5]

    def prev_part(self) -> None:
        if self.__cur_index - 5 >= 0:
            self.__cur_index -= 5
            self.cur_page -= 1

    def next_part(self) -> None:
        if self.__cur_index + 5 * 2 < self.length:
            self.__cur_index += 5
            self.cur_page += 1
