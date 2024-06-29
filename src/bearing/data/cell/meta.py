# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Metadata Class
=======================


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any, Dict, Callable
import copy
import json

# Import | Libraries

# Import | Local Modules
from .data import Data


# =============================================================================
# Classes
# =============================================================================

class Metadata(Data):
    """
    Metadata Class
    ==============

    Manages metadata, leveraging the Data class for storage, retrieval, and
    manipulation of metadata key-value pairs.

    The Metadata class extends the Data class to specifically handle metadata,
    which is typically represented as a dictionary of key-value pairs.

    Inherits from:
    Data: The base class providing mechanisms for managing encapsulated
        content.

   Attributes:
    _value (Dict[str, Any]): A dictionary to store metadata key-value pairs.

    """

    # Constructor
    # =========================================================================

    def __init__(self, data: Dict[str, Any] = None, immutable: bool = False):
        """
        Initializes the Metadata instance with an optional dictionary of
        metadata.

        Parameters
        ----------
        data: A dictionary containing initial metadata key-value pairs.

        """
        super().__init__(data if data is not None else {})
        self.immutable = immutable

    # Magic Methods
    # =========================================================================

    def __str__(self) -> str:
        """
        Returns a string representation of the metadata.

        """
        return super().__str__()  # Utilizes __str__ from Data class

    def __repr__(self) -> str:
        """
        Generates a detailed string representation of the Metadata instance.

        """
        return f"Metadata(data={super().__repr__()})"

    def __getitem__(self, key) -> Any:
        """
        Retrieves an item from the encapsulated collection using the given
        key or index.

        Parameters
        ----------
        key: The key or index of the item to retrieve.

        Returns
        -------
        The item corresponding to the specified key or index in the collection.

        """
        return self._value[key]

    def __setitem__(self, key, item):
        """
        Updates the encapsulated collection with a new item at the specified
        key or index. Sets an item in metadata, with type checking and
        immutability considerations.

        Parameters
        ----------
        key: The key or index where the item should be updated or inserted.
        item: The new item to insert into the collection.

        """
        if self.immutable:
            raise ValueError("Cannot modify immutable Metadata instance.")
        # Perform type checking or validation for key and item here
        # if necessary
        super().__setitem__(key, item)

    def __delitem__(self, key):
        """
        Removes an item from the encapsulated collection at the specified key
        or index, considering immutability.

        Parameters
        ----------
        key: The key or index of the item to remove from the collection.

        """
        if self.immutable:
            raise ValueError("Cannot modify immutable Metadata instance.")
        super().__delitem__(key)

    # Public Methods
    # =========================================================================

    def update(self, updates: Dict[str, Any]):
        """
        Updates metadata with provided key-value pairs, adding new keys or
        overwriting existing ones.

        Parameters
        ----------
        updates: A dictionary containing metadata updates.

        """
        if self.immutable:
            raise ValueError("Cannot modify immutable Metadata instance.")
        else:
            for key, value in updates.items():
                self[key] = value  # Utilizes __setitem__

    def validate(self, schema: Dict[str, Any]) -> bool:
        """
        Validates metadata against a specified schema. This method serves as a
        placeholder for actual validation logic.

        Parameters
        ----------
        schema: A dictionary defining the validation schema.

        Returns
        -------
        Always returns True as this is a placeholder method. Implement
        validation as needed.

        """
        # Placeholder for validation logic; should be implemented as required.
        return True
        # if not validation_rule(self._value):
        #     raise ValueError("Metadata validation failed.")
        # return True

    def merge(self, other: 'Metadata', overwrite: bool = True) -> None:
        """
        Merges metadata from another Metadata instance into this one, utilizing
        the __setitem__ method for item assignment.

        Parameters
        ----------
        other (Metadata): The other Metadata instance from which to merge
            metadata.
        overwrite (bool): Determines whether existing metadata keys should
            be overwritten.

        """
        for key, value in other.items():
            if overwrite or key not in self:
                self[key] = value

    def clone(self, deep: bool = False) -> 'Metadata':
        """
        Clones the Metadata instance, optionally as a deep copy.

        """
        return Metadata(
            copy.deepcopy(self._value) if deep else copy.copy(self._value),
            self.immutable
        )

    def has_key(self, key: str) -> bool:
        """
        Checks for the existence of a specific metadata key, utilizing the
        __getitem__ method for item retrieval.

        Parameters
        ----------
        key (str): The metadata key to check for existence.

        Returns
        -------
        True if the key exists, False otherwise.

        """
        return key in self

    def remove_key(self, key: str) -> None:
        """
        Removes a specific key from the metadata, utilizing the  __delitem__
        method for item removal.

        Parameters
        ----------
        key (str): The metadata key to be removed.

        """
        del self[key]

    def to_json(self) -> str:
        """
        Serializes metadata to a JSON string.

        """
        return json.dumps(self._value)

    @classmethod
    def from_json(cls, json_str: str, immutable: bool = False) -> 'Metadata':
        """
        Deserializes metadata from a JSON string.

        """
        data = json.loads(json_str)
        return cls(data, immutable=immutable)
