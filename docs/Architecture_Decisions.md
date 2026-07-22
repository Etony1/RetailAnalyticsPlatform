# Architecture Decisions

## AD-001

Decision:
Separate Orders and Order Items.

Reason:
One order can contain many products.

Benefits:
- Database normalization
- Easier reporting
- Reduced data duplication

---

## AD-002

Decision:
Inventory Transactions are append-only.

Reason:
Maintain a complete audit trail.

Benefits:
- History is preserved
- Inventory can be reconstructed
- Easier reconciliation

---

## AD-003

Decision:
Separate business calculations from data generation.

Reason:
Follow the Single Responsibility Principle.

Benefits:
- Easier maintenance
- Easier testing
- More reusable code