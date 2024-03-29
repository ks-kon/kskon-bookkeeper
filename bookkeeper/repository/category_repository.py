from repository.abstract_repository import AbstractRepository
from models.category import Category


# class CatRepo(AbstractRepository):
#     def __init__(self, list_cat: list[Category]):
#         self.list = list_cat
#
#     def add(self, new_cat: Category):
#         self.list.append(new_cat)
#
#     def get(self, pk:int) -> Category:
#         for cat in self.list:
#             if cat.pk == pk:
#                 return cat
#
#     def get_all(self):
#         return self.list
#
#     def update(self):
#         pass
#
#     def delete(self, pk):
#         for cat in self.list:
#             if cat.pk == pk:
#                 value = cat
#                 self.list.remove(value)
#
#     def get_list_cat(self):
#         return [cat.name for cat in self.list]