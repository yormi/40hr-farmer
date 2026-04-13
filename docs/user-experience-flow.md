# User Experience Flow

```mermaid
flowchart TD
    A[User discovers 40hr Farmer] --> B[Lands on landing page]
    B --> C[Scrolls through sections]
    C --> D{Clicks 'Join' CTA}
    D -->|Not ready| E[Leaves site]
    D -->|Ready| F[Fills out HubSpot form<br>Name, Email, Farm name,<br>Greenhouse yes/no]

    F --> G[Form submitted]
    G --> H[Contact created in HubSpot CRM]
    G --> I[GA4 waitlist_signup event fires]
    G --> J[HubSpot workflow triggers]

    J --> K["Email 01: Welcome<br><i>You're in — here's what's coming</i><br>(immediate)"]
    K -->|3 days| L["Email 02: Why<br><i>Why we're building this</i><br>(burnout story, empathy)"]
    L -->|3 days| M["Email 03: Greenhouse<br><i>The greenhouse trick nobody talks about</i><br>(teach multiplier concept)"]
    M -->|3 days| N["Email 04: Drew<br><i>How Drew got his wife back on the farm</i><br>(social proof)"]
    N -->|4 days| O["Email 05: How It Works<br><i>Here's how it works, simply</i><br>(program details + CTA)"]

    O --> P{Clicks 'Join the 40hr Farmer'}
    P -->|Yes| Q[Returns to landing page #join]
    P -->|No| R[Sequence ends]

    style A fill:#EAF3DE,stroke:#3B6D11
    style F fill:#EAF3DE,stroke:#3B6D11
    style G fill:#639922,stroke:#27500A,color:#fff
    style K fill:#fff,stroke:#639922
    style L fill:#fff,stroke:#639922
    style M fill:#fff,stroke:#639922
    style N fill:#fff,stroke:#639922
    style O fill:#fff,stroke:#639922
    style Q fill:#EAF3DE,stroke:#3B6D11
```

## Timeline

```
Day 0   ──── Form submit + Email 01 (Welcome)
Day 3   ──── Email 02 (Why we're building this)
Day 6   ──── Email 03 (Greenhouse trick)
Day 9   ──── Email 04 (Drew's story)
Day 13  ──── Email 05 (How it works + Join CTA)
```

## Touchpoints summary

| Touchpoint | Channel | Goal |
|---|---|---|
| Landing page | Web | Educate + capture lead |
| Form submit | Web | Convert visitor to contact |
| Email 01 | Email | Welcome, set expectations |
| Email 02 | Email | Build empathy (burnout problem) |
| Email 03 | Email | Teach (greenhouse = leverage) |
| Email 04 | Email | Social proof (Drew's story) |
| Email 05 | Email | CTA to join the program |
