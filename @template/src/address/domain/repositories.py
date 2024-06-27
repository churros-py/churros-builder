
# -*- coding: utf-8 -*-
from typing import Tuple
from abc import ABCMeta, abstractmethod

from src.address.domain.entities import Address


class AddressRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> Tuple[Address]:
        """
        Method responsable for find all addresss considering pagination
        """
        pass

    @abstractmethod
    def find_by_id(self, address_id: int) -> Address | None:
        """
        Method responsable for find address by id
        """
        pass

    @abstractmethod
    def save(self, input_save_address) -> Address:
        """
        Method responsable for save address
        """
        pass

    @abstractmethod
    def update(self, input_update_address) -> Address:
        """
        Method responsable for update address
        """
        pass

    @abstractmethod
    def inactivate(self, address_id: int) -> None:
        """
        Method responsable for inactive address
        """
        pass

    @abstractmethod
    def delete(self, address_id: int) -> None:
        """
        Method responsable for delete address
        """
        pass
