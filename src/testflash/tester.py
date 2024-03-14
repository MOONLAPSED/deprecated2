# FLASHES are tested like python modules are tested using pytest -s and function-based tests which can be run as modules or as functions at runtime.
import pytest
import sys
import types
from typing import Any, Callable, List, Tuple, Union

from main import main as ml

ml.logger.info('Testing flashes')


class FlashMethodFactory:
    """
    This is a factory class for pytest.mark.parametrize.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args: Tuple[Any, ...] = args
        self.kwargs: dict = kwargs

    def __call__(self, func: Union[Callable, str]) -> Any:
        """
        Decorate a function or a string with pytest.mark.parametrize.
        """
        if isinstance(func, str):
            return pytest.mark.parametrize(self.args, self.kwargs)(func)
        return pytest.mark.parametrize(*self.args, **self.kwargs)(func)


@pytest.mark.parametrize(
    'flash',
    [
        'cognos.flash.flash_0001',
        'cognos.flash.flash_0002',
        'cognos.flash.flash_0003',
    ],
    indirect=True
)
def test_flashes(flash: str) -> None:
    """
    Test flashes.
    """
    ml.logger.info(f'Testing flash: {flash}')


def test_rt_module() -> None:
    """
    Test the runtime module.
    """
    ml.logger.info('Testing runtime module')
    rt_module = types.ModuleType('cognos')
    rt_mod_name = 'cognos'
    rt_mod_path = sys.modules['__main__'].__file__
    rt_module.__name__ = rt_mod_name
    rt_module.__file__ = rt_mod_path
    rt_module.__package__ = 'cognos'
    rt_module.__path__ = None
    rt_module.__doc__ = None
    # advanced funcs tbd like __loaders__ (if needed)
    sys.modules['cognos'] = rt_module
    ml.logger.info(f'cognos module: {sys.modules["cognos"]}')
