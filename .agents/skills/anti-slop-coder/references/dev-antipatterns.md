# Developer Anti-Patterns & Clean Engineering Replacements (EN & AR)

Synthesized from `ofershap/ai-humanizer`, `blader/humanizer` (§19–§26), and `conorbronsdon/avoid-ai-writing`.

---

## 1. Source Code Comments

### Bad (Narrating WHAT — Instant AI Signal)
```python
# Initialize an empty list to store results
results = []

# Iterate through each item in the payload
for item in payload:
    # Check if item is active
    if item.is_active:
        # Append active item to results
        results.append(item)
```

### Good (Self-explanatory code + WHY comment only when non-obvious)
```python
# Preserve input order; downstream batch signer hashes items positionally.
results = [item for item in payload if item.is_active]
```

---

## 2. Git Commit Messages

### Bad (AI Marketing Essay + Co-Author Trailer)
```text
feat: implement comprehensive rate-limiting middleware for robust API protection

This commit introduces a seamless, scalable sliding-window rate limiter that
leverages Redis to safeguard endpoints and ensure optimal system reliability.

Co-authored-by: Claude <noreply@anthropic.com>
```

### Good (Human Engineer)
```text
add Redis sliding-window rate limiter

Fail open if Redis times out (>150ms) so transient cache blips don't drop checkout traffic.
```

---

## 3. README Openings (English & Arabic)

### Bad (EN)
> ## 🚀 Overview
> In today's fast-paced microservices landscape, managing configuration — across multiple environments — plays a pivotal role. **EnvCheck** serves as a comprehensive, cutting-edge solution!
> - **Fast:** Blazing-fast validation
> - **Robust:** Comprehensive schema checks
> - **Seamless:** Effortless CI integration
>
> Happy coding! 🎉

### Good (EN)
> Validate `.env` files against a JSON schema before your app boots. Exits non-zero in CI on missing or mistyped keys, with zero runtime dependencies.

### Bad (AR)
> ## 🚀 نظرة عامة
> في ظل التطورات المتسارعة في عالم البرمجيات الحديث، تلعب إدارة الإعدادات دوراً محورياً لا غنى عنه. تقوم هذه الأداة بتوفير حل شامل ومتكامل وسلس لفحص ملفات البيئة!

### Good (AR)
> أداة خفيفة للتحقق من متغيرات البيئة (`.env`) قبل تشغيل التطبيق، وإيقاف البناء في CI عند نقص أي متغير أو اختلاف نوعه.

---

## 4. Code Review & Async Slack Replies (§26 Wrong-Reader Fix)

### Bad (Re-explaining the reviewer's own context, burying the answer at the bottom)
> Great catch! As you noted, `syncUser` runs inside the webhook transaction, and when Stripe retries concurrently, two workers read the stale row before updating `plan_id`. We could add a distributed lock in Redis, or use `SELECT ... FOR UPDATE`. Since Postgres already holds the row, `FOR UPDATE` is simpler. Let's use `FOR UPDATE` here.

### Good (Decision first, minimal delta reasoning)
> Switched to `SELECT ... FOR UPDATE` on the account row in `4f82c1a` so concurrent Stripe retries serialize in Postgres without adding a Redis lock dependency.
