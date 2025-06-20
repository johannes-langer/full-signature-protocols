from __future__ import annotations
from typing import Any, Callable, Protocol, _ProtocolMeta, get_type_hints


class FullSignatureMeta(_ProtocolMeta):
    '''
    Overrides the default Protocol metaclass to include signature checking. Ignores methods that start with a specified prefix (default is ``_``).
    '''

    _exclude_prefix : str = '_'

    def __instancecheck__(cls: FullSignatureMeta, instance : Any) -> bool:
        '''
        Parameters
        ----------
        instance : Any
            The instance to check against the protocol.

        Returns
        -------
        bool
            True if the usual Protocol checks pass and the instance has all methods with the correct signatures.
        '''
        if not super().__instancecheck__(instance):
            return False
         
        if all(
            hasattr(instance, k) and
            all(
                _k in (sign := get_type_hints(getattr(instance, k))) and
                (issubclass(sign[_k], _v) or sign[_k] is Any)
                for _k, _v in get_type_hints(v).items()
            )
            for k, v in cls.__dict__.items() if not k.startswith(cls._exclude_prefix) and isinstance(v, Callable)
        ):
            return True
        
        return False
    

class FullSignatureProtocol(Protocol, metaclass = FullSignatureMeta):
    '''
    A Protocol that checks not only the presence of methods but also their signatures.
    '''
    def __init_subclass__(cls) -> None:
        '''
        Automatically adds the Protocol base class to the subclass, so that it is not necessary to explicitly inherit from Protocol for each subclass.
        '''
        cls.__bases__ += (Protocol,)
        return super().__init_subclass__()
    

def configure_exclude_prefix(prefix : str) -> None:
    '''
    Configures the prefix used to exclude methods from signature checking.

    Parameters
    ----------
    prefix : str
        The prefix to exclude from signature checking.
    '''
    FullSignatureMeta._exclude_prefix = prefix
