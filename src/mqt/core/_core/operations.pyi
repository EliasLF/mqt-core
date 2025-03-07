from abc import ABCMeta, abstractmethod
from collections.abc import Mapping, Sequence
from typing import ClassVar, overload

from .._compat.typing import Self
from ..symbolic import Expression, Variable

class Control:
    class Type:
        __members__: ClassVar[dict[Control.Type, str]]
        Neg: ClassVar[Control.Type]
        Pos: ClassVar[Control.Type]

        def __eq__(self: Self, other: object) -> bool: ...
        def __getstate__(self: Self) -> int: ...
        def __hash__(self: Self) -> int: ...
        def __index__(self: Self) -> int: ...
        def __init__(self: Self, value: int) -> None: ...
        def __int__(self: Self) -> int: ...
        def __ne__(self: Self, other: object) -> bool: ...
        def __setstate__(self: Self, state: int) -> None: ...
        @property
        def name(self: Self) -> str: ...
        @property
        def value(self: Self) -> int: ...

    qubit: int
    type_: Type

    @overload
    def __init__(self: Self, qubit: int) -> None: ...
    @overload
    def __init__(self: Self, qubit: int, type_: Type) -> None: ...

class OpType:
    __members__: ClassVar[dict[OpType, str]]  # readonly
    barrier: ClassVar[OpType]  # value = <OpType.barrier: 3>
    classic_controlled: ClassVar[OpType]  # value = <OpType.classic_controlled: 38>
    compound: ClassVar[OpType]  # value = <OpType.compound: 34>
    dcx: ClassVar[OpType]  # value = <OpType.dcx: 26>
    ecr: ClassVar[OpType]  # value = <OpType.ecr: 27>
    gphase: ClassVar[OpType]  # value = <OpType.gphase: 1>
    h: ClassVar[OpType]  # value = <OpType.h: 4>
    i: ClassVar[OpType]  # value = <OpType.i: 2>
    iswap: ClassVar[OpType]  # value = <OpType.iswap: 23>
    measure: ClassVar[OpType]  # value = <OpType.measure: 35>
    none: ClassVar[OpType]  # value = <OpType.none: 0>
    peres: ClassVar[OpType]  # value = <OpType.peres: 24>
    peresdg: ClassVar[OpType]  # value = <OpType.peresdg: 25>
    p: ClassVar[OpType]  # value = <OpType.p: 16>
    reset: ClassVar[OpType]  # value = <OpType.reset: 36>
    rx: ClassVar[OpType]  # value = <OpType.rx: 19>
    rxx: ClassVar[OpType]  # value = <OpType.rxx: 28>
    ry: ClassVar[OpType]  # value = <OpType.ry: 20>
    ryy: ClassVar[OpType]  # value = <OpType.ryy: 29>
    rz: ClassVar[OpType]  # value = <OpType.rz: 21>
    rzx: ClassVar[OpType]  # value = <OpType.rzx: 31>
    rzz: ClassVar[OpType]  # value = <OpType.rzz: 30>
    s: ClassVar[OpType]  # value = <OpType.s: 8>
    sdg: ClassVar[OpType]  # value = <OpType.sdg: 9>
    swap: ClassVar[OpType]  # value = <OpType.swap: 22>
    sx: ClassVar[OpType]  # value = <OpType.sx: 17>
    sxdg: ClassVar[OpType]  # value = <OpType.sxdg: 18>
    t: ClassVar[OpType]  # value = <OpType.t: 10>
    tdg: ClassVar[OpType]  # value = <OpType.tdg: 11>
    teleportation: ClassVar[OpType]  # value = <OpType.teleportation: 37>
    u2: ClassVar[OpType]  # value = <OpType.u2: 15>
    u: ClassVar[OpType]  # value = <OpType.u: 14>
    v: ClassVar[OpType]  # value = <OpType.v: 12>
    vdg: ClassVar[OpType]  # value = <OpType.vdg: 13>
    x: ClassVar[OpType]  # value = <OpType.x: 5>
    xx_minus_yy: ClassVar[OpType]  # value = <OpType.xx_minus_yy: 32>
    xx_plus_yy: ClassVar[OpType]  # value = <OpType.xx_plus_yy: 33>
    y: ClassVar[OpType]  # value = <OpType.y: 6>
    z: ClassVar[OpType]  # value = <OpType.z: 7>
    @property
    def name(self: Self) -> str: ...
    @property
    def value(self: Self) -> int: ...
    def __eq__(self: Self, other: object) -> bool: ...
    def __getstate__(self: Self) -> int: ...
    def __hash__(self: Self) -> int: ...
    def __index__(self: Self) -> int: ...
    @overload
    def __init__(self: Self, value: int) -> None: ...
    @overload
    def __init__(self: Self, arg0: str) -> None: ...
    def __int__(self: Self) -> int: ...
    def __ne__(self: Self, other: object) -> bool: ...
    def __setstate__(self: Self, state: int) -> None: ...

class Operation(metaclass=ABCMeta):
    type_: OpType
    controls: set[Control]
    num_qubits: int
    targets: list[int]
    parameter: list[float]
    @property
    def name(self: Self) -> str: ...
    @property
    def num_targets(self: Self) -> int: ...
    @property
    def num_controls(self: Self) -> int: ...
    @abstractmethod
    def add_control(self: Self, control: Control) -> None: ...
    def add_controls(self: Self, controls: set[Control]) -> None: ...
    @abstractmethod
    def clear_controls(self: Self) -> None: ...
    @abstractmethod
    def remove_control(self: Self, control: Control) -> None: ...
    def remove_controls(self: Self, controls: set[Control]) -> None: ...
    def acts_on(self: Self, qubit: int) -> bool: ...
    def get_used_qubits(self: Self) -> set[int]: ...
    def is_classic_controlled_operation(self: Self) -> bool: ...
    def is_compound_operation(self: Self) -> bool: ...
    def is_controlled(self: Self) -> bool: ...
    def is_non_unitary_operation(self: Self) -> bool: ...
    def is_standard_operation(self: Self) -> bool: ...
    def is_symbolic_operation(self: Self) -> bool: ...
    def is_unitary(self: Self) -> bool: ...
    def get_inverted(self: Self) -> Operation: ...
    @abstractmethod
    def invert(self: Self) -> None: ...
    @abstractmethod
    def qasm_str(self: Self, qreg: Sequence[tuple[str, str]], creg: Sequence[tuple[str, str]]) -> str: ...
    def __eq__(self: Self, other: object) -> bool: ...

class StandardOperation(Operation):
    @overload
    def __init__(self: Self) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        target: int,
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        control: Control,
        target: int,
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        control: Control,
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        target: int,
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(self: Self, nq: int, controls: set[Control], target: int, starting_qubit: int = 0) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        target0: int,
        target1: int,
        op_type: OpType,
        params: Sequence[float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    def add_control(self: Self, control: Control) -> None: ...
    def clear_controls(self: Self) -> None: ...
    def remove_control(self: Self, control: Control) -> None: ...
    def invert(self: Self) -> None: ...
    def qasm_str(self: Self, qreg: Sequence[tuple[str, str]], creg: Sequence[tuple[str, str]]) -> str: ...

class NonUnitaryOperation(Operation):
    @property
    def classics(self: Self) -> list[int]: ...
    @overload
    def __init__(self: Self, nq: int, targets: Sequence[int], classics: Sequence[int]) -> None: ...
    @overload
    def __init__(self: Self, nq: int, target: int, classic: int) -> None: ...
    @overload
    def __init__(self: Self, nq: int, targets: Sequence[int], op_type: OpType = ...) -> None: ...
    def add_control(self: Self, control: Control) -> None: ...
    def clear_controls(self: Self) -> None: ...
    def remove_control(self: Self, control: Control) -> None: ...
    def invert(self: Self) -> None: ...
    def qasm_str(self: Self, qreg: Sequence[tuple[str, str]], creg: Sequence[tuple[str, str]]) -> str: ...

class CompoundOperation(Operation):
    @overload
    def __init__(self: Self, nq: int) -> None: ...
    @overload
    def __init__(self: Self, nq: int, ops: Sequence[Operation]) -> None: ...
    def __len__(self: Self) -> int: ...
    @overload
    def __getitem__(self: Self, idx: int) -> Operation: ...
    @overload
    def __getitem__(self: Self, idx: slice) -> list[Operation]: ...
    def append(self: Self, op: Operation) -> None: ...
    def empty(self: Self) -> bool: ...
    def add_control(self: Self, control: Control) -> None: ...
    def clear_controls(self: Self) -> None: ...
    def remove_control(self: Self, control: Control) -> None: ...
    def invert(self: Self) -> None: ...
    def qasm_str(self: Self, qreg: Sequence[tuple[str, str]], creg: Sequence[tuple[str, str]]) -> str: ...

class SymbolicOperation(StandardOperation):
    @overload
    def __init__(self: Self) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        target: int,
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        control: Control,
        target: int,
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        control: Control,
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        target: int,
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        targets: Sequence[int],
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    @overload
    def __init__(
        self: Self,
        nq: int,
        controls: set[Control],
        target0: int,
        target1: int,
        op_type: OpType,
        params: Sequence[Expression | float] | None = None,
        starting_qubit: int = 0,
    ) -> None: ...
    def get_parameter(self: Self, idx: int) -> Expression | float: ...
    def get_parameters(self: Self) -> list[Expression | float]: ...
    def get_instantiated_operation(self: Self, assignment: Mapping[Variable, float]) -> StandardOperation: ...
    def instantiate(self: Self, assignment: Mapping[Variable, float]) -> None: ...

class ClassicControlledOperation(Operation):
    def __init__(
        self: Self, operation: Operation, control_register: tuple[int, int], expected_value: int = 1
    ) -> None: ...
    @property
    def operation(self: Self) -> Operation: ...
    @property
    def control_register(self: Self) -> tuple[int, int]: ...
    @property
    def expected_value(self: Self) -> int: ...
    def add_control(self: Self, control: Control) -> None: ...
    def clear_controls(self: Self) -> None: ...
    def remove_control(self: Self, control: Control) -> None: ...
    def invert(self: Self) -> None: ...
    def qasm_str(self: Self, qreg: Sequence[tuple[str, str]], creg: Sequence[tuple[str, str]]) -> str: ...
