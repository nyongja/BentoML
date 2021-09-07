import os
import typing as t

import bentoml._internal.constants as const

from ._internal.models.base import MODEL_NAMESPACE, PICKLE_EXTENSION, Model
from ._internal.types import MetadataType, PathType
from ._internal.utils import LazyLoader, catch_exceptions
from .exceptions import BentoMLException, MissingDependencyException

_exc = const.IMPORT_ERROR_MSG.format(
    fwr="fastai",
    module=__name__,
    inst="Make sure to install PyTorch first,"
    " then `pip install fastai`. Refers to"
    " https://github.com/fastai/fastai#installing",
)
if t.TYPE_CHECKING:  # pragma: no cover
    # pylint: disable=unused-import
    import fastai
    import fastai.basics as basics
    import fastai.learner as learner
else:
    fastai = LazyLoader("fastai", globals(), "fastai")
    basics = LazyLoader("basics", globals(), "fastai.basics")
    learner = LazyLoader("learner", globals(), "fastai.learner")


class FastAIModel(Model):
    """
    Model class for saving/loading :obj:`fastai` model

    Args:
        model (`fastai.learner.Learner`):
            Learner model from fastai
        metadata (`Dict[str, Any]`,  `optional`, default to `None`):
            Class metadata

    Raises:
        MissingDependencyException:
            :obj:`fastai` is required by FastAIModel

    Example usage under :code:`train.py`::

        TODO:

    One then can define :code:`bento.py`::

        TODO:
    """

    _model: "learner.Learner"

    @catch_exceptions(
        catch_exc=ModuleNotFoundError, throw_exc=MissingDependencyException, msg=_exc
    )
    def __init__(
        self,
        model: "learner.Learner",
        metadata: t.Optional[MetadataType] = None,
    ):
        assert learner, BentoMLException("Only fastai2 is supported by BentoML")
        super(FastAIModel, self).__init__(model, metadata=metadata)

    @classmethod
    @catch_exceptions(
        catch_exc=ModuleNotFoundError, throw_exc=MissingDependencyException, msg=_exc
    )
    def load(cls, path: PathType) -> "learner.Learner":
        return basics.load_learner(
            os.path.join(path, f"{MODEL_NAMESPACE}{PICKLE_EXTENSION}")
        )

    @catch_exceptions(
        catch_exc=ModuleNotFoundError, throw_exc=MissingDependencyException, msg=_exc
    )
    def save(self, path: PathType) -> None:
        self._model.export(
            fname=os.path.join(path, f"{MODEL_NAMESPACE}{PICKLE_EXTENSION}")
        )