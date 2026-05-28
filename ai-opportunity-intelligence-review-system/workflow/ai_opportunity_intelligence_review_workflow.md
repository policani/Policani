# AI Opportunity Intelligence Review Workflow

This workflow converts rough AI ideas into intelligence-stack maps, route recommendations, and decision-ready proof plans.

## End-To-End Review

```mermaid
flowchart TD
    A[Raw AI Idea] --> B[Concept Intake]
    B --> C[Problem Clarity Test]
    C --> D[Intelligence Stack Decomposition]
    D --> E[Work Shape Review]
    E --> F[Value And Proof Review]
    F --> G[Govern And Assure Review]
    G --> H{Route}
    H --> I[Prototype]
    H --> J[Build]
    H --> K[Buy]
    H --> L[Automate With Existing Tools]
    H --> M[Hire Or Upskill]
    H --> N[Wait]
    H --> O[Process First]
    H --> P[Decompose Further]
    H --> Q[Stop]
    I --> R[Architecture Brief]
    J --> R
    K --> R
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
    R --> S[Human Portfolio Review]
```

## Intelligence Stack

```mermaid
flowchart LR
    P[Purpose] --> S[Sensing]
    S --> I[Interpretation]
    I --> D[Decision]
    D --> O[Orchestration]
    O --> L[Learning]
    L --> S
    G[Govern And Assure] -. evals, logs, permissions, review, rollback .-> D
```

## Route Logic

```mermaid
flowchart TD
    A[Decomposed Opportunity] --> B{Workflow clear?}
    B -- No --> C[Decompose Further]
    B -- Broken process --> D[Process First]
    B -- Yes --> E{Value evidenced?}
    E -- No --> F[Stop Or Manual Proof]
    E -- Directional --> G{Data and controls ready?}
    E -- Strong --> G
    G -- Blocked --> H[Wait]
    G -- High risk --> I[Control Review Before Proof]
    G -- Ready --> J{Differentiated workflow?}
    J -- Common --> K[Buy Or Existing Tools]
    J -- Strategic --> L[Prototype Or Build]
    J -- Capability gap --> M[Hire Or Upskill]
```
