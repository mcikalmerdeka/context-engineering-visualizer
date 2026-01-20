# Product Strategy & Decision Handbook

**Product:** AtlasPay

**Company:** Atlas Fintech Solutions

**Last Updated:** 12 January 2026

**Document Owner:** Product Strategy Team

**Audience:** Product Managers, Product Analysts, Data Analysts, Engineering Leads, Business Stakeholders

---

## 1. Purpose of This Document

This handbook serves as the **single source of truth** for AtlasPay’s product strategy, key decisions, and the rationale behind them. It is designed to preserve institutional knowledge as the company scales and to reduce repeated discussions about *why* certain product choices were made.

This document should be consulted when:
- Making new product or roadmap decisions
- Evaluating trade-offs
- Designing experiments
- Interpreting product metrics
- Onboarding new team members

---

## 2. Product Overview

### 2.1 What Is AtlasPay?

AtlasPay is a **B2B payment orchestration platform** that helps mid-sized e-commerce and SaaS companies manage:
- Multiple payment gateways
- Transaction routing
- Fraud detection
- Settlement and reconciliation

AtlasPay abstracts payment complexity behind a unified API and dashboard.

### 2.2 Core User Personas

- **Finance Managers** – care about settlement accuracy, reconciliation, and reporting
- **Developers** – care about API reliability, documentation, and integration speed
- **Operations Teams** – care about uptime, incident response, and fraud prevention

---

## 3. Product Vision & Principles

### 3.1 Product Vision

> *“AtlasPay aims to be the invisible infrastructure that businesses trust for every transaction, regardless of scale or geography.”*

### 3.2 Product Principles

1. **Reliability Over Novelty**  
   We prioritize stability and predictability over experimental features.

2. **Abstraction Without Obscurity**  
   Complexity should be hidden, but behavior should remain explainable.

3. **Enterprise-Grade by Default**  
   Features are designed with compliance, auditability, and scale in mind.

4. **Metrics-Driven Decisions**  
   Product changes must be supported by data or a clearly stated hypothesis.

---

## 4. Strategic Goals (2025–2027)

### 4.1 Company-Level Goals

- Expand into Southeast Asia and LATAM markets
- Reduce merchant churn below 5% annually
- Achieve 99.95% API uptime

### 4.2 Product-Level Goals

- Reduce integration time from **14 days → 3 days**
- Improve payment success rate by **+2% globally**
- Provide self-serve analytics for 90% of merchant use cases

---

## 5. Key Metrics & Success Criteria

This section defines the primary metrics used to evaluate AtlasPay’s product performance. While strategic intent and interpretation are documented here, **exact calculation formulas are intentionally not included**. All official metric computations are owned by the Data team and implemented in the centralized metrics service.

---

### 5.1 North Star Metric

#### Successful Transactions per Active Merchant (STAM)

STAM measures the average number of successful transactions processed per active merchant over a given period. It captures both **merchant engagement** and **platform reliability**, making it the primary indicator of long-term product health.

STAM is used to:
- Evaluate whether merchants are successfully operating on AtlasPay
- Compare performance across regions and merchant segments
- Assess the impact of reliability and routing improvements

**Calculation Notice:**  
STAM involves multiple internal filters, normalization steps, and merchant eligibility rules. The exact computation logic is maintained in the official metrics service and must not be manually reimplemented in product analyses.

---

### 5.2 Retention & Revenue Quality Metrics

#### Net Revenue Retention (NRR)

Net Revenue Retention measures how revenue from existing merchants changes over time, accounting for:
- Expansion revenue
- Contraction
- Churn

NRR is a critical indicator of:
- Long-term customer value
- Pricing effectiveness
- Product stickiness

NRR is primarily used in:
- Quarterly business reviews
- Market expansion evaluations
- Pricing and packaging decisions

**Calculation Notice:**  
NRR calculation logic is owned by the Data team and implemented in the centralized metrics system. Product teams should rely on official NRR values rather than attempting to reconstruct the formula.

---

### 5.3 Platform Reliability Metrics

#### Payment Success Rate (Adjusted)

Adjusted Payment Success Rate represents the percentage of valid payment attempts that result in successful transactions.

This metric intentionally excludes:
- Merchant-side validation errors
- User-abandoned checkouts
- Duplicate retry attempts

Adjusted Payment Success Rate is used to:
- Evaluate routing and gateway performance
- Detect regional reliability issues
- Measure the impact of infrastructure changes

**Important:**  
The adjusted version of this metric relies on standardized filtering logic and event classification rules defined in the metrics service. Manual calculation is discouraged to avoid inconsistencies across teams.

---

## 6. Target Customer Segments

### 6.1 Primary Segment

- Online businesses with **$5M–$100M annual revenue**
- Operate in at least 2 regions
- Use more than one payment provider

### 6.2 Secondary Segment

- SaaS platforms with recurring billing
- Marketplaces with split payouts

### 6.3 Non-Target Segments

- Small businesses using a single gateway
- Offline-only merchants

---

## 7. Feature Prioritization Framework

### 7.1 Evaluation Dimensions

Each feature is scored on:
- **Customer Impact** (1–5)
- **Revenue Impact** (1–5)
- **Strategic Alignment** (1–5)
- **Engineering Effort** (1–5, inverse)

### 7.2 Priority Score Formula

```
Priority Score = (Customer Impact + Revenue Impact + Strategic Alignment) / Engineering Effort
```

### 7.3 Known Limitations

- Does not account well for regulatory deadlines
- Requires subjective judgment in scoring

---

## 8. Major Product Decisions (Historical)

### 8.1 Decision: Build vs Buy Fraud Detection (2024)

**Outcome:** Build in-house fraud engine

**Rationale:**
- Existing vendors lacked region-specific signals
- Long-term cost efficiency
- Better control over false positives

**Trade-offs:**
- Slower initial rollout
- Increased engineering maintenance

---

### 8.2 Decision: Unified Dashboard vs Per-Gateway Views (2025)

**Outcome:** Unified dashboard

**Rationale:**
- Merchants prefer a single operational view
- Reduces cognitive load
- Aligns with abstraction principle

**Risks Identified:**
- Power users losing detailed gateway-level controls

**Mitigation:**
- Advanced filters and export options

---

## 9. Assumptions & Risks

### 9.1 Core Assumptions

- Merchants value time-to-integration more than feature richness
- Payment success rate improvements directly reduce churn
- Regulatory complexity will continue to increase

### 9.2 Key Risks

- Over-abstraction may reduce transparency
- Expansion into new regions may slow core roadmap
- Dependence on third-party gateways

---

## 10. Experimentation & Learning

### 10.1 When We Run Experiments

- UI/UX changes
- Onboarding flow updates
- Routing algorithm adjustments

### 10.2 When We Do NOT Experiment

- Compliance-related changes
- Incident response procedures
- Security controls

### 10.3 Experiment Success Criteria

- Statistically significant improvement in primary metric
- No degradation of secondary metrics

---

## 11. Launch & Rollout Strategy

### 11.1 Feature Flags

All major features are released behind feature flags.

### 11.2 Phased Rollout

1. Internal testing
2. Beta merchants (5–10)
3. Gradual regional rollout
4. General availability

---

## 12. Post-Launch Evaluation

### 12.1 Required Reviews

- 7-day metrics review
- 30-day impact analysis
- 90-day strategic fit assessment

### 12.2 Common Failure Patterns

- Metrics improve but merchant satisfaction drops
- Feature adoption lower than expected
- Increased support ticket volume

---

## 13. Decision Log (Summary)

| Date | Decision | Owner | Status |
|-----|--------|------|--------|
| 2024-06 | Build Fraud Engine | Product | Completed |
| 2025-03 | Unified Dashboard | Product | Completed |
| 2025-11 | Self-Serve Analytics | Data | In Progress |

---

## 14. How to Use This Document

- **Before proposing a feature:** Review Sections 3–7
- **When questioning a decision:** Review Section 8
- **When analyzing metrics:** Review Section 5
- **When onboarding:** Read Sections 1–4

---

## 15. Open Questions & Future Considerations

- Should AtlasPay offer native BNPL integrations?
- How much customization should enterprise merchants get?
- When do we sunset legacy gateway integrations?

---

**End of Document**

