---
name: generate_type_hints
description: generate type hints
---

# Python typing instructions

This prompt supplements `AGENTS.md`.
For repo-wide Pylance and VS Code workflow, import-resolution rules, and general validation expectations, defer to the base instructions first.
Use this prompt for typing-specific decisions and tradeoffs.

When modifying Python files, optimize for correctness under Pylance / Pyright, not just syntactic validity.
Prefer the smallest correct typing change that preserves runtime behavior.

## Primary goal
Add or improve type hints so the code is clearer and passes Pylance cleanly.

## General rules
- Do not change runtime behavior.
- Do not refactor unrelated code.
- Do NOT change the code in the functions or methods unless absolutely necessary.
- Keep edits local and minimal.
- Preserve public APIs unless explicitly asked to change them.
- Prefer readable annotations over clever ones.
- Prefer built-in generics (`list[str]`, `dict[str, int]`) and modern union syntax (`A | B`) when compatible with the repo's Python version.
- Keep imports minimal and sorted.

## Typing decision order
Use this order when deciding how to type code:

1. **Plain inline annotations first**
   - Add parameter, return, attribute, and local variable annotations when the type is straightforward.
   - Prefer concrete types over abstract ones unless abstraction is useful to callers.

2. **Use `TypeVar` only for relationships**
   - Introduce `TypeVar` when the return type must depend on an input type, or when multiple parameters must share the same type.
   - Do not use `TypeVar` when a simple union is enough.
   - If a constrained `TypeVar` becomes awkward or loses precision, consider overloads instead.

3. **Use `overload` only when call shapes truly differ**
   - Use `@overload` when the return type changes based on:
     - argument count
     - argument types
     - literal argument values
     - `None` vs non-`None`
   - Keep overload sets minimal and non-overlapping when possible.
   - The concrete implementation must accept the union of all overload inputs and return the union of all overload outputs.
   - Do not add overloads if one precise generic signature is enough.

4. **Use protocols / ParamSpec / Callable only when needed**
   - Prefer `Protocol` for structural typing.
   - Use `ParamSpec` for higher-order wrappers and decorators that preserve call signatures.
   - Do not introduce advanced typing machinery unless it materially improves correctness.

## Pylance / Pyright compatibility rules
- Make type narrowing explicit when needed with `isinstance`, `assert`, sentinel checks, or helper guards.
- If a function is overloaded, ensure the implementation signature is broad enough for all overload variants.
- Use `reveal_type(...)` mentally as a debugging model when choosing annotations.
- Prefer annotations that make inferred types stable under the workspace's configured Pylance mode.

## What to avoid
- Do not add redundant overloads.
- Do not replace simple unions with unnecessary generics.
- Do not use a constrained `TypeVar` where overloads would be clearer.
- Do not leave partially typed APIs with ambiguous return types if they can be expressed precisely.
- Do not silence checker problems by widening everything to `object`.

## Required output format for code edits
When you propose a change:
1. Show the exact diff or rewritten function/class.
2. Briefly explain why you chose:
   - simple annotations, or
   - `TypeVar`, or
   - `overload`
3. Mention any tradeoffs or remaining ambiguity.
4. If overloads were added, explain why a single generic signature was not sufficient.

## Validation checklist
Before finalizing, verify:
- Parameters are annotated.
- Return types are annotated.
- Public attributes are typed where useful.
- Overloads are consistent with the implementation.
- Type narrowing works for all branches.
- Optional / `None` behavior is explicit.
- Container element types are precise.
- The result satisfies repo-wide Pylance expectations from `.github/copilot-instructions.md` under the workspace's configured analysis mode.

## If uncertain
If the code is ambiguous, prefer one of these:
- add the safest readable type and note the ambiguity, or
- provide 2 candidate typings and state which one is better for Pylance.
Do not guess silently.
