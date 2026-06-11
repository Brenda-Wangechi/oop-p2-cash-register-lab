#!/usr/bin/env python3

class CashRegister:
  """A simple cash register that can add items, apply a percentage
  discount to the total, and void the last transaction.

  Attributes
  - discount: integer percentage (0-100 inclusive).
  - total: numeric running total of the register.
  - items: list of item names added (repeats allowed for quantity).
  - previous_transactions: list of dicts with keys `item`, `price`, `quantity`.
  """

  def __init__(self, discount=0):
    # Ensure discount is an integer between 0 and 100. If invalid,
    # print a warning and set discount to 0.
    try:
      discount_int = int(discount)
    except Exception:
      print("Not valid discount")
      discount_int = 0

    if discount_int < 0 or discount_int > 100:
      print("Not valid discount")
      discount_int = 0

    self.discount = discount_int
    # running total (float to allow cents)
    self.total = 0
    # list of item names (repeated according to quantity)
    self.items = []
    # store each transaction as dicts: {item, price, quantity}
    self.previous_transactions = []

  def add_item(self, item, price, quantity=1):
    """Add an item to the register.

    - Increase `total` by `price * quantity`.
    - Append the `item` `quantity` times to `items` list.
    - Record the transaction in `previous_transactions`.
    """
    # Update total
    line_total = price * quantity
    self.total += line_total

    # Update items list with repeated entries for quantity
    for _ in range(quantity):
      self.items.append(item)

    # Record the transaction so it can be voided later
    self.previous_transactions.append({
      'item': item,
      'price': price,
      'quantity': quantity
    })

  def apply_discount(self):
    """Apply the registered percentage discount to the total.

    - If `discount` is 0, prints a message indicating no discount.
    - Otherwise, reduces `total` by the discount percent and prints
      the updated total in dollars.
    """
    if self.discount <= 0:
      print("There is no discount to apply.")
      return

    discount_amount = (self.discount / 100.0) * self.total
    self.total = self.total - discount_amount

    # Format output: if total is a whole number, print without decimals
    if float(self.total).is_integer():
      print(f"After the discount, the total comes to ${int(self.total)}.")
    else:
      # Show two decimal places for cents
      print(f"After the discount, the total comes to ${self.total:.2f}.")

  def void_last_transaction(self):
    """Remove the most recent transaction from the register.

    - Pops the last transaction from `previous_transactions`.
    - Subtracts its total (price * quantity) from `total`.
    - Removes the corresponding number of item entries from `items`.
    """
    if not self.previous_transactions:
      # Nothing to void.
      return

    last = self.previous_transactions.pop()
    deduction = last['price'] * last['quantity']
    self.total -= deduction

    # Remove the item occurrences from the items list (from the end).
    item_name = last['item']
    qty = last['quantity']
    # Remove `qty` occurrences of item_name starting from the right
    removed = 0
    new_items = []
    # Iterate items in reverse and skip the first `qty` matches
    for name in reversed(self.items):
      if name == item_name and removed < qty:
        removed += 1
        continue
      new_items.append(name)

    # Re-reverse to original order
    self.items = list(reversed(new_items))

    # Guard against negative zero-like totals: set to 0 if very small negative
    if abs(self.total) < 1e-9:
      self.total = 0.0
