from uuid import UUID
from typing import List, Union


class Charge:
    id: UUID
    items: List[List[Union[int, str]]]
    date: int
    product_group: int

    def __init__(self, id: UUID, items: List[List[Union[int, str]]], date: int, product_group: int) -> None:
        self.id = id
        self.items = items
        self.date = date
        self.product_group = product_group


class ValueCharge:
    charge: Charge
    type: str

    def __init__(self, charge: Charge, type: str) -> None:
        self.charge, self.type = charge, type


class ValueReserveId:
    reserve_id: UUID
    date: int
    product_group: int
    type: str

    def __init__(self, reserve_id: UUID, date: int, product_group: int, type: str) -> None:
        self.reserve_id = reserve_id
        self.date = date
        self.product_group = product_group
        self.type = type


class ValueProductGroup:
    product_group: int
    reserve_id: UUID
    order_id: UUID
    date: int
    quantity: int
    gtin: str
    payment_type: int
    type: str
    pext_id: None

    def __init__(self, product_group: int, reserve_id: UUID, order_id: UUID, date: int, quantity: int, gtin: str,
                 payment_type: int, type: str, pext_id: None) -> None:
        self.product_group = product_group
        self.reserve_id = reserve_id
        self.order_id = order_id
        self.date = date
        self.quantity = quantity
        self.gtin = gtin
        self.payment_type = payment_type
        self.type = type
        self.pext_id = pext_id


class ValuePayment:
    charge: Charge
    account: str
    balance_before: int
    amount_charged: int
    balance_after: int
    reserve_before: int
    reserve_after: int
    type: str

    def __init__(self, charge: Charge, account: str, balance_before: int, amount_charged: int, balance_after: int,
                 reserve_before: int, reserve_after: int, type: str) -> None:
        self.charge = charge
        self.account = account
        self.balance_before = balance_before
        self.amount_charged = amount_charged
        self.balance_after = balance_after
        self.reserve_before = reserve_before
        self.reserve_after = reserve_after
        self.type = type
