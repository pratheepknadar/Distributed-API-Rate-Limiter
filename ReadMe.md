## Project: Distributed Rate Limiter Service
#### Problem: 
Modern APIs face the constant challenge of resource exhaustion, whether from malicious DDoS attacks, scraping bots, or simply buggy client implementations. Without a mechanism to control traffic volume, backend services can easily become overwhelmed, leading to high latency or complete downtime.
#### Solution: 
I established a robust, distributed Rate Limiting middleware designed to sit in front of protected API routes. Unlike simple in-memory counters which cannot scale across multiple worker processes or servers, this solution utilizes Redis as a centralized, high-performance ephemeral store.
## Key Features:
    • Distributed Architecture: Works seamlessly across multiple API instances (Gunicorn/uWSGI workers) by sharing state in Redis.
    • Atomic Operations: Utilizes Redis Pipelines to execute INCR and TTL checks atomically, preventing race conditions under high concurrency.
    • Fixed Window Algorithm: Implements a time-bucket approach (e.g., X requests per Y seconds) that efficiently manages quotas.
    • Developer Friendly: Exposed as a clean @rate_limit decorator, making it trivial to protect specific endpoints with just one line of code.
    • Informative Responses: Returns detailed 429 Error responses including the current usage, limit cap, and time remaining until reset, allowing well-behaved clients to back off gracefully.
## Technical Highlights:
    • Language: Python
    • Framework: Flask
    • Database: Redis (In-memory key-value store)
    • Concepts: Concurrency Control, Atomic Transactions, Decorator Pattern, REST Standards.
