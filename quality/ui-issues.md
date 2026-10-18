# Portfolio application issues and changes

These relate to the actual locally built portfolio viewer, not SAP UAT defects. No production system or stakeholder test is represented.

| ID | Observation | Change | Verification |
|---|---|---|---|
| UIISS-001 | Real Chromium test: searching FR-004 also returned NFR-004 because the ID matched a substring | Recognize a complete BR/FR/NFR identifier and use exact ID matching; retain keyword/fragment search otherwise | Retest recorded in browser-checks.json when current-source checks pass |
| UIISS-002 | Initial navigation focus scrolled the overview past its top; order details appeared after a 300-row list | Prevent focus-induced scrolling; reset navigation to top; place detail panels before lists | Screenshot inspection and browser navigation test |
| UIISS-003 | Changing a filter could leave a previously selected record displayed above unrelated results | Clear detail panels when search/status filters change | Browser no-result and subsequent detail checks |

No user preference or operational outcome was inferred from these fixes. The browser evidence file records the source hashes tested after corrections.
