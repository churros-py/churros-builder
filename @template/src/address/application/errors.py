# -*- coding: utf-8 -*-
from fastapi import status, HTTPException


class AddressNotFound:
    def __init__(self) -> None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            [
                {
                    "loc": ["param", "address_id"],
                    "msg": "Address not found",
                    "type": "not_found_error",
                }
            ],
        )
