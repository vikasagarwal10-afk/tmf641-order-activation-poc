# TMF641 Order Management POC — Working Demo

## Test Results

### Idempotency Test ✅
Same request twice → Same orderId (no duplicate orders)

### SLA Prediction ✅
- 5G Gaming Slice: 10 seconds predicted
- Home Broadband: 30 seconds predicted

### Order Tracking ✅
GET /orders returns all created orders

## Live Demo Commands
```bash
# Create order
curl -X POST http://localhost:8000/order -H "Content-Type: application/json" -H "x-request-id: test-001" -H "x-subscriber-id: sub-123" -d '{"orderItem": [{"productId": "5g_slicing_gaming", "action": "add"}]}'

# Get order
curl http://localhost:8000/order/b287004a-598c-4d48-bc64-12cbd57bed0b
Architecture Decision Record (ADR)
Why Idempotency?
Without it, network retries or agent double-clicks create duplicate orders → double billing → customer churn.

Why SLA Prediction?
Customers abandon orders if activation takes too long. Predicting SLA before order sets correct expectations.


# TMF641 Order Management POC

**Built for e& (Etisalat) Enterprise Architect Interview**

## Why I Built This

e& is transforming from Telco to Techco. Two problems I see in order-to-activation:
1. **Duplicate orders** → double billing → customer churn
2. **No SLA visibility** → customers don't know when service will activate

This POC solves both using TM Forum principles.

## How It Works

| Feature | Implementation | Why It Matters |
|---------|---------------|----------------|
| Idempotency | SHA256(x-request-id + x-subscriber-id) | Prevents duplicate charges |
| SLA Prediction | Product-based mapping with logarithmic scaling | Sets customer expectations |
| Order Tracking | In-memory storage with GET /order/{id} | Audit & debugging |

## Live Demo

```bash
# Create order (5G gaming)
curl -X POST http://localhost:8000/order \
  -H "x-request-id: demo-001" -H "x-subscriber-id: gamer-123" \
  -d '{"orderItem": [{"productId": "5g_slicing_gaming", "action": "add"}]}'

# Same request again → SAME orderId (idempotency!)

# List all orders
curl http://localhost:8000/orders
