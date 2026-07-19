# Implementation Prompt

Implement only the assigned task.

Inputs:

- task record
- context pack
- prompt policy decision and scheduler lease
- relevant policies
- validation plan

Rules:

- change only listed files unless a blocker requires re-planning
- stop when lease expires, policy denies an action, or a conflicting user change is detected
- keep changes minimal and consistent with local patterns
- add or update tests when behavior changes
- run validation gates and report evidence

Completion requires:

- acceptance criteria satisfied
- validation evidence recorded
- residual risks listed
- execution, validation, and audit artifact IDs reported
