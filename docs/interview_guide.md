# Orders

Question:
Why separate Orders and Order Items?

Answer:
Orders represent the header of a purchase. Order Items represent the individual products purchased. Separating them avoids data duplication, supports one-to-many relationships, and makes reporting easier.

-------------------------------------

# Inventory

Question:
Why create Inventory Transactions?

Answer:
Inventory Transactions provide a complete audit trail of inventory movements. Current inventory can be calculated from the transaction history, while Inventory Snapshot provides the current state for reporting.

Question

Why separate Inventory Snapshot and Inventory Transactions?

Answer

Inventory Snapshot represents the current state.

Inventory Transactions represent the history of inventory movements.

Keeping them separate preserves history while allowing efficient reporting.

-------------------------------------

# Returns

Question:
Why append returns instead of updating sales?

Answer:
Returns are independent business events. Recording them separately preserves history and provides a complete audit trail.