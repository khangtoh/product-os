# Adopt ProductOS

The copy boundary is `template/product/`. It is self-contained and can live inside an application repository or a dedicated product-context repository.

## 1. Copy the bare instance

Clone this repository if needed:

```sh
git clone https://github.com/khangtoh/product-os.git
cd product-os
```

From this checkout, copy the template into an existing target project that has no `product/` path:

```sh
test ! -e ../my-project/product && cp -R template/product ../my-project/product
```

Replace `../my-project` with your project path. Check that it exists. If it already has product documentation, map and merge the relevant sections manually; do not overwrite existing context. The command intentionally refuses an existing `product/` path.

To create a separate product-context repository, copy `template/product/` to an empty destination and initialize Git there. Connect it to the app with explicit repository and environment references in its operations register. Creating a repository from this entire framework includes the guides and examples too; copying the inner folder produces the bare instance.

## 2. Connect agent context

Merge this paragraph into the project's existing root AGENTS.md or equivalent agent instructions:

```markdown
## Product context

For product work, read product/AGENTS.md, product/PRODUCT.md, and
product/STATE.md before making changes. Follow linked product records as
needed and update product context after material decisions or results.
```

Preserve existing repository instructions. Do not replace them with the template's nested AGENTS.md. No special filename guarantees automatic loading across every agent tool.

## 3. Establish intent and current truth

Fill the known parts of PRODUCT.md: name, promise, users, core job, desired change, constraints, and non-goals. Reference existing briefs or owner direction. Fill VISION and STRATEGY only with relevant context; unknowns are valid.

Update STATE.md with the actual project stage, owner, current work, blockers, and next action. Record the adoption date there. Link verified app code, release environments, observation sources, and existing operating scope in operations/README.md.

Do not copy facts or permissions from another project to make this one look complete.

## 4. Choose one outcome

Copy `templates/outcome.md` to a new `outcomes/OUT-001-descriptive-slug.md`. Assign an owner and define the desired change, evidence, baseline, target, evaluation window, and guardrails appropriate to the project.

If those are not yet known, keep the outcome proposed and define a bounded discovery action to establish them. Select a real next step in ROADMAP and STATE. Do not make speculative targets appear accepted.

## 5. Complete one small loop

For substantive work, create a cycle record and link it from STATE. Research a problem, implement a small change, or evaluate existing behavior. Add a feature or experiment only when needed. Preserve acceptance criteria and experiment criteria before collecting results.

Record what happened, what remains uncertain, and the resulting decision. Update the relevant product records and next action. Start with the [operating guide](OPERATING_GUIDE.md) or [fictional worked example](../examples/first-learning-loop.md).

## Check adoption

- Can a human and an agent find the product purpose and next action?
- Do internal links work in the copied folder without this framework checkout?
- Are unknowns, proposed targets, and actual permissions distinguishable?
- Is there one real priority rather than a fabricated sample backlog?
- Does active work have an owner, criteria, and a handoff?

You can now use ProductOS manually or with an assistant. Follow [automation](AUTOMATION.md) when you want recurring autonomous execution; copying the template does not configure it.
