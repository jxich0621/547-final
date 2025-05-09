#! /usr/bin/env python3

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Type, Union


@dataclass
class CBILogEntry:
    """
    Data class for a single entry in a CBI log.

    :param kind: The kind of entry [branch/return].
    :param line: The line number specified in the log.
    :param column: The column number specified in the log.
    :param value: The value specified in the log.
    """

    kind: str
    line: int
    column: int
    value: Union[bool, int]

    @property
    def is_return(self) -> bool:
        """
        :return: True if the entry is a return.
        """
        return self.kind == "return"

    @property
    def is_branch(self) -> bool:
        """
        :return: True if the entry is a branch.
        """
        return self.kind == "branch"


"""Type Alias for a list of CBILogEntry"""
CBILog: Type[List[CBILogEntry]] = List[CBILogEntry]


class ObservationStatus(Enum):
    """
    Enum for the Observation Status of a predicate.

    :param NEVER: The predicate was never observed.
    :param ONLY_TRUE: The predicate was observed and was always true.
    :param ONLY_FALSE: The predicate was observed and was always false.
    :param BOTH: The predicate was observed at least once as true and false.
    """

    NEVER = "never"
    ONLY_TRUE = "true"
    ONLY_FALSE = "false"
    BOTH = "both"

    @classmethod
    def from_bool(cls, observed_as: bool) -> "ObservationStatus":
        """
        Convinence method to create an Observation status enum from a boolean.
        """
        return cls.ONLY_TRUE if observed_as else cls.ONLY_FALSE

    @staticmethod
    def merge(observation1, observation2) -> "ObservationStatus":
        """
        Merge two observations statuses.

        :param observation1: The first observation.
        :param observation2: The second observation.
        :return: The merged observation.
            If one of the observations is None, the other is returned.
            If one of the observations is BOTH, BOTH is returned.
            If the two observations are the same, the same observation is returned.
            If the two observations are different, BOTH is returned.
        """
        if observation1 == ObservationStatus.NEVER:
            return observation2
        elif observation1 == ObservationStatus.BOTH:
            return observation1
        elif observation1 != observation2:
            return ObservationStatus.BOTH
        else:
            return observation1


class PredicateType:
    """
    Enum for the type of a predicate.

    :param branch_true: Predicate that the branch was taken.
    :param branch_false: Predicate that the branch was not taken.
    :param return_positive: Predicate that the return value was positive.
    :param return_zero: Predicate that the return value was zero.
    :param return_negative: Predicate that the return value was negative.
    """

    BRANCH_TRUE = "BranchTrue"
    BRANCH_FALSE = "BranchFalse"
    RETURN_POSITIVE = "ReturnPositive"
    RETURN_ZERO = "ReturnZero"
    RETURN_NEGATIVE = "ReturnNegative"
    BRANCH_TYPES = [BRANCH_TRUE, BRANCH_FALSE]
    RETURN_TYPES = [RETURN_POSITIVE, RETURN_ZERO, RETURN_NEGATIVE]
    ALL_TYPES = BRANCH_TYPES + RETURN_TYPES

    @classmethod
    def alternatives(cls, value: Union[bool, int]) -> List[Tuple[str, bool]]:
        """
        Gel all possible Branch/Return types for a given value
        and whether value indicates a true or false observation for that type.

        ex. if value = True, means that the predicate was about a branch
        condition that was evaluated as True, then the alternatives are:
            (BranchTrue, True), and (BranchFalse, False)
        Similarly, if value = False, means that the predicate was about a branch
        condition that was evaluated as False, then the alternatives are:
            (BranchTrue, False), and (BranchFalse, True)

        :param value: The value corresponding to the predicate.
        :return: A list of tuples of (predicate_type, observation status).
        """
        pred_type = cls.from_value(value=value)
        if pred_type in cls.BRANCH_TYPES:
            return [
                (cls.BRANCH_TRUE, ObservationStatus.from_bool(value)),
                (cls.BRANCH_FALSE, ObservationStatus.from_bool(not value)),
            ]
        elif pred_type in cls.RETURN_TYPES:
            return [
                (cls.RETURN_POSITIVE, ObservationStatus.from_bool(value > 0)),
                (cls.RETURN_ZERO, ObservationStatus.from_bool(value == 0)),
                (cls.RETURN_NEGATIVE, ObservationStatus.from_bool(value < 0)),
            ]

    @staticmethod
    def from_value(value: Union[bool, int]) -> str:
        """
        Get the predicate type for a given value found in CBILogEntry.
        """
        if type(value) == int:
            if value > 0:
                return PredicateType.RETURN_POSITIVE
            elif value == 0:
                return PredicateType.RETURN_ZERO
            else:
                return PredicateType.RETURN_NEGATIVE
        elif type(value) == bool:
            return PredicateType.BRANCH_TRUE if value else PredicateType.BRANCH_FALSE
        raise ValueError(f"Unknown value encountered: {value}")


@dataclass(init=False, order=True, unsafe_hash=True)
class Predicate:
    """
    Data class for a predicate.

    :param line: The line number of the predicate in the program.
    :param column: The column number of the predicate in the program.
    :param pred_type: The type of the predicate.
        One of the predicate types from PredicateType.
    """

    line: int
    column: int
    pred_type: str

    def __init__(
        self,
        line: int,
        column: int,
        value: Union[bool, int, str],
    ):
        """
        Initialize a predicate.

        :param line: The line number of the predicate in the program.
        :param column: The column number of the predicate in the program.
        :param value: The value of the predicate (boolean or integer or PredicateType).
        """
        self.line = line
        self.column = column
        if value in PredicateType.ALL_TYPES:
            self.pred_type = value
        else:
            self.pred_type = PredicateType.from_value(value)

    def __str__(self) -> str:
        return f"Line {self.line:03}, Col {self.column:03}, {self.pred_type:>14}"

    def __repr__(self) -> str:
        return str(self)


@dataclass
class PredicateInfo:
    """
    Data class for a holding information about a predicate.
    """

    predicate: Predicate
    num_true_in_success: int = field(default=0, init=False)
    num_true_in_failure: int = field(default=0, init=False)

    num_true_in_failure_div_zero: int = field(default=0, init=False)
    num_true_in_failure_null_ptr: int = field(default=0, init=False)
    num_true_in_failure_assertion: int = field(default=0, init=False)

    num_observed_in_success: int = field(default=0, init=False)
    num_observed_in_failure: int = field(default=0, init=False)

    num_observed_in_failure_div_zero: int = field(default=0, init=False)
    num_observed_in_failure_null_ptr: int = field(default=0, init=False)
    num_observed_in_failure_assertion: int = field(default=0, init=False)

    # Computed properties
    # These properties are computed based on the values of the other fields.
    failure: float = field(default=0.0, init=False)
    context: float = field(default=0.0, init=False)
    increase: float = field(default=0.0, init=False)

    failure_div_zero: float = field(default=0.0, init=False)
    context_div_zero: float = field(default=0.0, init=False)
    increase_div_zero: float = field(default=0.0, init=False)

    failure_null_ptr: float = field(default=0.0, init=False)
    context_null_ptr: float = field(default=0.0, init=False)
    increase_null_ptr: float = field(default=0.0, init=False)

    failure_assertion: float = field(default=0.0, init=False)
    context_assertion: float = field(default=0.0, init=False)
    increase_assertion: float = field(default=0.0, init=False)

    @property
    def failure(self) -> float:
        """
        The Failure value of the predicate.

        :return: The failure value.
        """
        # TODO: Implement the calculation of the failure value.

        if (self.num_true_in_failure + self.num_true_in_success) == 0:
            return 0
        else:
            return self.num_true_in_failure / (self.num_true_in_failure + self.num_true_in_success)

    @property
    def context(self) -> float:
        """
        The Context value of the predicate.

        :return: The context value.
        """
        # TODO: Implement the calculation of the context value.

        if (self.num_observed_in_failure + self.num_observed_in_success) == 0:
            return 0
        else:
            return self.num_observed_in_failure / (self.num_observed_in_failure + self.num_observed_in_success)

    @property
    def increase(self):
        """
        The Increase value of the predicate.

        :return: The increase value.
        """
        # TODO: Implement the calculation of the increase value.

        return self.failure - self.context
    
    @property
    def failure_div_zero(self) -> float:
        """
        The Failure value of the predicate when the failure is due to a division by zero.

        :return: The failure value.
        """
        if (self.num_true_in_failure_div_zero + self.num_true_in_success) == 0:
            return 0
        else:
            return self.num_true_in_failure_div_zero / (self.num_true_in_failure_div_zero + self.num_true_in_success)

    @property
    def context_div_zero(self) -> float:
        """
        The Context value of the predicate when the failure is due to a division by zero.

        :return: The context value.
        """
        if (self.num_observed_in_failure_div_zero + self.num_observed_in_success) == 0:
            return 0
        else:
            return self.num_observed_in_failure_div_zero / (self.num_observed_in_failure_div_zero + self.num_observed_in_success)

    @property
    def increase_div_zero(self):
        """
        The Increase value of the predicate when the failure is due to a division by zero.

        :return: The increase value.
        """
        return self.failure_div_zero - self.context_div_zero
    
    @property
    def failure_null_ptr(self) -> float:
        """
        The Failure value of the predicate when the failure is due to a null pointer dereference.

        :return: The failure value.
        """
        if (self.num_true_in_failure_null_ptr + self.num_true_in_success) == 0:
            return 0
        else:
            return self.num_true_in_failure_null_ptr / (self.num_true_in_failure_null_ptr + self.num_true_in_success)
        
    @property
    def context_null_ptr(self) -> float:
        """
        The Context value of the predicate when the failure is due to a null pointer dereference.

        :return: The context value.
        """
        if (self.num_observed_in_failure_null_ptr + self.num_observed_in_success) == 0:
            return 0
        else:
            return self.num_observed_in_failure_null_ptr / (self.num_observed_in_failure_null_ptr + self.num_observed_in_success)
        
    @property
    def increase_null_ptr(self):
        """
        The Increase value of the predicate when the failure is due to a null pointer dereference.

        :return: The increase value.
        """
        return self.failure_null_ptr - self.context_null_ptr
    
    @property
    def failure_assertion(self) -> float:
        """
        The Failure value of the predicate when the failure is due to an assertion failure.

        :return: The failure value.
        """
        if (self.num_true_in_failure_assertion + self.num_true_in_success) == 0:
            return 0
        else:
            return self.num_true_in_failure_assertion / (self.num_true_in_failure_assertion + self.num_true_in_success)
        
    @property
    def context_assertion(self) -> float:
        """
        The Context value of the predicate when the failure is due to an assertion failure.

        :return: The context value.
        """
        if (self.num_observed_in_failure_assertion + self.num_observed_in_success) == 0:
            return 0
        else:
            return self.num_observed_in_failure_assertion / (self.num_observed_in_failure_assertion + self.num_observed_in_success)
        
    @property
    def increase_assertion(self):
        """
        The Increase value of the predicate when the failure is due to an assertion failure.

        :return: The increase value.
        """
        return self.failure_assertion - self.context_assertion

    


    """
    Helper methods that map variable names to names in lecture slides.

    they let you use the variable names as used in the lecture slides
    instead of the variable names used in the code.

    s     -> num_true_in_success
    f     -> num_true_in_failure
    s_obs -> num_observed_in_success
    f_obs -> num_observed_in_failure
    """

    @property
    def s(self):
        return self.num_true_in_success

    @s.setter
    def s(self, value: int):
        self.num_true_in_success = value

    @property
    def s_obs(self):
        return self.num_observed_in_success

    @s_obs.setter
    def s_obs(self, value: int):
        self.num_observed_in_success = value

    @property
    def f(self):
        return self.num_true_in_failure

    @f.setter
    def f(self, value: int):
        self.num_true_in_failure = value

    @property
    def f_obs(self):
        return self.num_observed_in_failure

    @f_obs.setter
    def f_obs(self, value: int):
        self.num_observed_in_failure = value

    @property
    def f_div_zero(self):
        return self.num_true_in_failure_div_zero
    
    @f_div_zero.setter
    def f_div_zero(self, value: int):
        self.num_true_in_failure_div_zero = value

    @property
    def f_obs_div_zero(self):
        return self.num_observed_in_failure_div_zero

    @f_obs_div_zero.setter
    def f_obs_div_zero(self, value: int):
        self.num_observed_in_failure_div_zero = value

    @property
    def f_null_ptr(self):
        return self.num_true_in_failure_null_ptr
    
    @f_null_ptr.setter
    def f_null_ptr(self, value: int):
        self.num_true_in_failure_null_ptr = value

    @property
    def f_obs_null_ptr(self):
        return self.num_observed_in_failure_null_ptr
    
    @f_obs_null_ptr.setter
    def f_obs_null_ptr(self, value: int):
        self.num_observed_in_failure_null_ptr = value

    @property
    def f_assertion(self):
        return self.num_true_in_failure_assertion
    
    @f_assertion.setter
    def f_assertion(self, value: int):
        self.num_true_in_failure_assertion = value

    # Disallow directly setting computed properties

    @failure.setter
    def failure(self, value):
        pass

    @context.setter
    def context(self, value):
        pass

    @increase.setter
    def increase(self, value):
        pass

    @failure_div_zero.setter
    def failure_div_zero(self, value):
        pass

    @context_div_zero.setter
    def context_div_zero(self, value):
        pass

    @increase_div_zero.setter
    def increase_div_zero(self, value):
        pass

    @failure_null_ptr.setter
    def failure_null_ptr(self, value):
        pass

    @context_null_ptr.setter
    def context_null_ptr(self, value):
        pass

    @increase_null_ptr.setter
    def increase_null_ptr(self, value):
        pass

    @failure_assertion.setter
    def failure_assertion(self, value):
        pass

    @context_assertion.setter
    def context_assertion(self, value):
        pass

    @increase_assertion.setter
    def increase_assertion(self, value):
        pass

    def __str__(self) -> str:
        """
        String representation of the predicate info.
        """
        return (
            "== S(P) ==\n"
            f"{self.predicate}: {self.s}\n"
            "== F(P) ==\n"
            f"{self.predicate}: {self.f}\n"
            "== Failure(P) ==\n"
            f"{self.predicate}: {self.failure}\n"
            "== Context(P) ==\n"
            f"{self.predicate}: {self.context}\n"
            "== Increase(P) ==\n"
            f"{self.predicate}: {self.increase}\n"
        )


@dataclass
class Report:
    """
    Data class for the CBI Report.

    :param predicates_info_list: A list of PredicateInfo objects of all predicates in the program.
    """

    predicate_info_list: List[PredicateInfo]

    def __str__(self):
        """
        A fancy string representation of the report.
        """
        sorted_predicate_info = sorted(
            self.predicate_info_list, key=lambda pred_info: pred_info.predicate
        )
        s_p = "\n".join(f"{info.predicate}: {info.s}" for info in sorted_predicate_info)
        f_p = "\n".join(f"{info.predicate}: {info.f}" for info in sorted_predicate_info)
        # Add the failure, context and increase values for each predicate
        f_p_div_zero = "\n".join(
            f"{info.predicate}: {info.f_div_zero}" for info in sorted_predicate_info
        )
        f_p_null_ptr = "\n".join(
            f"{info.predicate}: {info.f_null_ptr}" for info in sorted_predicate_info
        )
        f_p_assertion = "\n".join(
            f"{info.predicate}: {info.f_assertion}" for info in sorted_predicate_info
        )

        failure = "\n".join(
            f"{info.predicate}: {info.failure}" for info in sorted_predicate_info
        )
        context = "\n".join(
            f"{info.predicate}: {info.context}" for info in sorted_predicate_info
        )
        increase = "\n".join(
            f"{info.predicate}: {info.increase}" for info in sorted_predicate_info
        )

        # Add the failure, context and increase values for each predicate
        failure_div_zero = "\n".join(
            f"{info.predicate}: {info.failure_div_zero}" for info in sorted_predicate_info
        )
        context_div_zero = "\n".join(
            f"{info.predicate}: {info.context_div_zero}" for info in sorted_predicate_info
        )
        increase_div_zero = "\n".join(
            f"{info.predicate}: {info.increase_div_zero}" for info in sorted_predicate_info
        )
        failure_null_ptr = "\n".join(
            f"{info.predicate}: {info.failure_null_ptr}" for info in sorted_predicate_info
        )
        context_null_ptr = "\n".join(
            f"{info.predicate}: {info.context_null_ptr}" for info in sorted_predicate_info
        )
        increase_null_ptr = "\n".join(
            f"{info.predicate}: {info.increase_null_ptr}" for info in sorted_predicate_info
        )
        failure_assertion = "\n".join(
            f"{info.predicate}: {info.failure_assertion}" for info in sorted_predicate_info
        )
        context_assertion = "\n".join(
            f"{info.predicate}: {info.context_assertion}" for info in sorted_predicate_info
        )
        increase_assertion = "\n".join(
            f"{info.predicate}: {info.increase_assertion}" for info in sorted_predicate_info
        )


        return (
            "== S(P) ==\n"
            f"{s_p}\n"
            "== F(P) ==\n"
            f"{f_p}\n"
            "== F(P) Div Zero ==\n"
            f"{f_p_div_zero}\n"
            "== F(P) Null Ptr ==\n"
            f"{f_p_null_ptr}\n"
            "== F(P) Assertion ==\n"
            f"{f_p_assertion}\n"

            "================================\n"
            "== Failure(P) ==\n"
            f"{failure}\n"
            "== Context(P) ==\n"
            f"{context}\n"
            "== Increase(P) ==\n"
            f"{increase}\n"

            "================================\n"

            "== Failure(P) Div Zero ==\n"
            f"{failure_div_zero}\n"
            "== Context(P) Div Zero ==\n"
            f"{context_div_zero}\n"
            "== Increase(P) Div Zero ==\n"
            f"{increase_div_zero}\n"

            "================================\n"
            "== Failure(P) Null Ptr ==\n"
            f"{failure_null_ptr}\n"
            "== Context(P) Null Ptr ==\n"
            f"{context_null_ptr}\n"
            "== Increase(P) Null Ptr ==\n"
            f"{increase_null_ptr}\n"

            "================================\n"

            "== Failure(P) Assertion ==\n"
            f"{failure_assertion}\n"
            "== Context(P) Assertion ==\n"
            f"{context_assertion}\n"
            "== Increase(P) Assertion ==\n"
            f"{increase_assertion}\n"

        )
