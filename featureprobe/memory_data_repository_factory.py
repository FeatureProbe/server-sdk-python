from data_repository_factory import DataRepositoryFactory
from fp_context import FPContext
from memory_data_repository import MemoryDataRepository


class MemoryDataRepositoryFactory(DataRepositoryFactory):

    def create(self, context: FPContext):
        return MemoryDataRepository()
