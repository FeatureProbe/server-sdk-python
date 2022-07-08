from data_repository import DataRepository
from fp_context import FPContext
from synchronizer import Synchronizer
from synchronizer_factory import SynchronizerFactory

class FileSynchronizerFactory(SynchronizerFactory):
    def create(self, context: FPContext, data_repo: DataRepository) -> Synchronizer:
        return FileSynchronizer(data_repo, context.location)
