# Temporal Information Verification

## Background

AI models have a knowledge cutoff date and may miss new versions, features, or products released after that date. When encountering potentially time-sensitive information, do not rely solely on training data to judge; actively verify instead.

## Trigger Conditions

When the following types of information may conflict with your knowledge:

- Model names/version numbers (e.g., Gemini, Claude, GPT, etc.)
- Software versions (frameworks, libraries, tools)
- API endpoints or parameters
- Feature updates for known products

## Approach

1. **Do not directly deny**: version numbers in user code may indeed exist
2. **Use Tavily search to verify**: query whether a new version has been released
3. **Provide accurate information**: including complete version number and release date (if available)

## Case Study

### Gemini Model Name (2026-02)

Code contained `gemini-3.0-flash`, initially judged as potentially an invalid model name.

**After verification**: Gemini 3.0 Flash had indeed been released, but the user was missing the `-preview` suffix; the correct name should be `gemini-3.0-flash-preview`.

**Lesson**: if a model name looks "too new," search first to confirm whether it has been released, rather than assuming user error.

## Search Template

```
{product name} {version number} release date
{product name} {version number} official announcement
```

Use Tavily search, `search_depth="advanced"`, `max_results=5`.

## Physical Anchor Verification

### Principle

In digital logic, use physical common sense as the final defense for complex logic verification. AI output may appear reasonable, but should be questioned when it violates physical laws.

### Application Scenarios

- AI-generated technical parameters (e.g., satellite altitude, device specifications)
- Numerical calculation results (is the order of magnitude reasonable?)
- Causal reasoning (does it violate physical laws?)

### Case Study

AI provided orbital parameters for a geosynchronous satellite, but the relationship between altitude and declination did not conform to Kepler's laws. Physical common sense (geosynchronous satellites must be above the equator at approximately 35,786 km) revealed the AI's hallucination.

### Execution Method

1. Identify parts of the output involving physical quantities
2. Perform quick verification using known physical common sense (unit conversion, order of magnitude, laws)
3. When anomalies are found, require AI to re-explain or search for verification
