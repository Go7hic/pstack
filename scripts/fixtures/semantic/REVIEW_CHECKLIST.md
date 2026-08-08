# Semantic review checklist

After an upstream import, review these skills by hand before merging:

- [ ] `how`
- [ ] `why`
- [ ] `architect`
- [ ] `arena`
- [ ] `swarm`
- [ ] `interrogate`
- [ ] `reflect`
- [ ] `poteto-mode`

For each skill, confirm:

1. Capability verbs name the actual job (`explore` vs `implement` vs `review`).
2. No vendor tool fields remain outside adapters.
3. Model selection goes through `model_role` or the override file.
4. Missing spawn / model selection / verify surfaces degrade explicitly.
5. Prompt templates under `references/` match the skill body.
