from data_repository import DataRepository
from fp_context import FPContext
from pooling_synchronizer import PoolingSynchronizer
from synchronizer import Synchronizer
from synchronizer_factory import SynchronizerFactory


class PoolingSynchronizerFactory(SynchronizerFactory):
    def create(self, context: FPContext, data_repo: DataRepository) -> Synchronizer:
        return PoolingSynchronizer(context, data_repo)
