---
description: pstack model overrides
alwaysApply: true
---

```json
{
  "schema_version": 1,
  "roles": {
    "fast_explore": "inherit-parent",
    "feature_impl": "auto",
    "bug_impl": "inherit-parent",
    "judgment": "inherit-parent",
    "critic": "inherit-parent"
  },
  "arena_runners": ["inherit-parent", "inherit-parent"],
  "arena_cross_judge_pool": ["inherit-parent"],
  "interrogate_reviewers": ["inherit-parent", "inherit-parent", "inherit-parent"],
  "architect_runners": ["inherit-parent", "inherit-parent"]
}
```
