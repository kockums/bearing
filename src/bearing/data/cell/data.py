# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Data Class
===================


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any, Callable, TypeVar, Generic
import copy
import json
import logging

# Import | Libraries

# Import | Local Modules


# =============================================================================
# Variables
# =============================================================================

# Define a type variable for type annotations
T = TypeVar('T')


# =============================================================================
# Classes
# =============================================================================

class DataValidationError(Exception):
    """
    Custom exception for data validation errors.
    """
    pass


class Data:
    """
    Data Class
    ==========

    Represents an encapsulated data unit, designed for versatile content
    management within data structures, with added robustness, logging, and
    type annotations.

    This class provides mechanisms to store, validate, and manipulate data,
    offering a generic approach to handle various data types and operations.
    It's suitable for applications requiring structured data management, such
    as in cells of a grid, elements of a collection, or standalone
    data holders.

    Attributes
    ----------
    _value (T): The encapsulated content or value, supporting diverse 
        data types.
    _immutable (bool): Flag indicating whether the Data instance is immutable.
    _logger (logging.Logger): Logger instance for logging data operations
        and changes.

    Methods
    -------
    value: Property to access or update the data value.
    immutable: Property to check or set the immutable state of the
        Data instance.
    validate: Validates the data against custom criteria or rules.
    transform: Applies a transformation function to the data.
    clone: Creates a deep or shallow copy of the Data instance.
    to_json: Serializes the data to a JSON string.
    from_json: Deserializes data from a JSON string.

    """

    # Constructor
    # =========================================================================

    def __init__(self, value: T = None, immutable: bool = False):
        """
        Initializes a new Data instance with the specified value and
        immutability flag.

        Parameters
        ----------
        value (T, optional): The initial data value. Defaults to None.
        immutable (bool, optional): Flag indicating whether the data should be
            immutable. Defaults to False.

        """
        self._value = value
        self._immutable = immutable
        self._logger = logging.getLogger(__name__)

    # Properties
    # =========================================================================

    # Property | Value
    # -------------------------------------------------------------------------

    @property
    def value(self) -> T:
        """
        Retrieves the encapsulated data value.

        """
        return self._value

    @value.setter
    def value(self, new_value: T):
        """
        Updates the encapsulated data value, with an option for custom
        validation.

        Parameters
        ----------
        new_value: New content for the data object. Custom validation can be
            integrated here.

        """
        if self.immutable:
            raise DataValidationError(
                "Cannot modify immutable Data instance."
            )
        self._value = new_value
        self._logger.info("Data value updated.")

    @value.deleter
    def value(self) -> None:
        """
        Resets the data value to its default state (None), if not immutable.
        """
        if self.immutable:
            raise DataValidationError(
                "Cannot delete value of immutable Data instance."
            )
        self._value = None

    # Property | Immutable
    # -------------------------------------------------------------------------

    @property
    def immutable(self) -> bool:
        """
        Checks if the Data instance is immutable.

        """
        return self._immutable

    @immutable.setter
    def immutable(self, new_state: bool):
        """
        Sets the immutable state of the Data instance. Once set to True, it
        cannot be reverted to False.

        Parameters
        ----------
        new_state (bool): The new immutable state. True makes the instance
        immutable, False has no effect if already immutable.

        """
        if self._immutable:
            return  # Once immutable, the state cannot be changed
        self._immutable = new_state
        self._logger.info(f"Data instance immutability set to {new_state}.")

    # Magic Methods
    # =========================================================================

    def __str__(self) -> str:
        """
        Provides a string representation of the encapsulated data for
        display purposes.

        """
        return str(self._value)

    def __repr__(self) -> str:
        """
        Generates a detailed string representation of the Data instance
        for debugging.

        """
        return f"Data(value={repr(self._value)}, immutable={self.immutable})"

    # Magic Methods | Rich Comparison Methods
    # -------------------------------------------------------------------------

    def __eq__(self, other: Any) -> bool:
        """
        Checks if the encapsulated data value is equal to the value in
        another Data instance or any other comparable value.

        Parameters
        ----------
        other: Another Data instance or a value to compare with.

        Returns
        -------
        bool: True if the values are equal, False otherwise.

        """
        if isinstance(other, Data):
            return self._value == other._value
        return self._value == other

    def __lt__(self, other: Any) -> bool:
        """
        Checks if the encapsulated data value is less than the value in
        another Data instance or any other comparable value.

        Parameters
        ----------
            other: Another Data instance or a value to compare with.

        Returns
        -------
        bool: True if the encapsulated value is less than the `other` value,
            False otherwise.

        """
        if isinstance(other, Data):
            return self._value < other._value
        return self._value < other

    def __le__(self, other: Any) -> bool:
        """
        Checks if the encapsulated data value is less than or equal to the
        value in another Data instance or any other comparable value.

        Parameters
        ----------
        other: Another Data instance or a value to compare with.

        Returns
        -------
        bool: True if the encapsulated value is less than or equal to the
            `other` value, False otherwise.

        """
        if isinstance(other, Data):
            return self._value <= other._value
        return self._value <= other

    def __gt__(self, other: Any) -> bool:
        """
        Checks if the encapsulated data value is greater than the value in
        another Data instance or any other comparable value.

        Parameters
        ----------
        other: Another Data instance or a value to compare with.

        Returns
        -------
        bool: True if the encapsulated value is greater than the `other`
            value, False otherwise.

        """
        if isinstance(other, Data):
            return self._value > other._value
        return self._value > other

    def __ge__(self, other: Any) -> bool:
        """
        Checks if the encapsulated data value is greater than or equal to
        the value in another Data instance or any other comparable value.

        Parameters
        ----------
        other: Another Data instance or a value to compare with.

        Returns
        -------
        bool: True if the encapsulated value is greater than or equal to
            the `other` value, False otherwise.

        """
        if isinstance(other, Data):
            return self._value >= other._value
        return self._value >= other

    # Public Methods
    # =========================================================================

    def validate(self, validation_function: Callable[[T], bool]):
        """
        Validates the data using a custom validation function.

        Parameters
        ----------
        validation_function: A function that takes the data value as
            input and returns a boolean indicating validity.

        Returns
        -------
        A boolean value indicating whether the data is valid according
            to the validation function.

        """
        if not validation_function(self._value):
            raise DataValidationError("Data validation failed.")
        # return validation_function(self._value)

    def transform(self, transformation_function: Callable[[T], T]):
        """
        Applies a transformation to the data using a custom function.

        Parameters
        ----------
        transformation_function: A function that takes the current data
            value as input and returns a transformed value.

        """
        if self.immutable:
            raise DataValidationError(
                "Cannot transform immutable Data instance."
            )
        self._value = transformation_function(self._value)

    def clone(self, deep: bool = False) -> 'Data':
        """
        Creates a copy of this Data instance, preserving the 'immutable' flag.

        Parameters
        ----------
        deep (bool): If True, performs a deep copy of the data; otherwise,
            a shallow copy is made.

        Returns
        -------
        A new Data instance with the same value.

        """
        if deep:
            new_value = copy.deepcopy(self._value, self.immutable)
        else:
            new_value = copy.copy(self._value, self.immutable)
        return Data(new_value)

    def to_json(self) -> str:
        """
        Serializes the data to a JSON string.

        """
        try:
            return json.dumps(self._value)
        except TypeError as e:
            self._logger.error("Error serializing Data to JSON: %s", e)
            return None

    @classmethod
    def from_json(cls, json_str: str) -> 'Data':
        """
        Deserializes data from a JSON string.

        """
        try:
            value = json.loads(json_str)
            return cls(value)
        except json.JSONDecodeError as e:
            logging.error("Error deserializing JSON to Data: %s", e)
            return cls()
