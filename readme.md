# Full Signature Protocols

This Package offers the FullSignatureProtocol class, which serves as an alterative to Python's builtin Protocol class, offering type-checks over method signatures.

## Usage

You can use the `FullSignatureProtocol` class like you would use the [`Protocol` class](https://typing.python.org/en/latest/spec/protocol.html). In addition to the usual type checks, `FullSignatureProtocol` also checks the signatures of methods in the protocol, e.g.:

```python
@runtime_checkable
class Prot(Protocol):
    def meth(a : int) -> None:
        ...

@runtime_checkable
class FSProt(FullSignatureProtocol):
    def meth(a : int) -> None:
        ...

class Impl():
    def meth() -> None:
        ...

impl = Impl()

isinstance(impl, Prot)      # True
isinstance(impl, FSProt)    # False
```

`FullSignatureMeta` has the property `_exclude_prefix`, which defaults to `_`. That means, that any methods starting with `_` will not be signature-checked. Note that the method still needs to be present, because the `Protocol` base class requires so. You can change this prefix with `configure_exclude_prefix()`.

## Notes

I am not sure how much time I can spare to maintain this package, but please add bug-reports anyway. Hope this helps!

–J
