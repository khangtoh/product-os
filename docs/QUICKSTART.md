# Adopt ProductOS

Onboarding turns a conversation into a complete initial product brief, requirements, and a Now / Next / Later roadmap. Start in the actual target project, which may be an empty folder, an existing app, or a dedicated product-context repository.

## 1. Choose an entry point

Obtain this framework checkout if needed:

```sh
git clone https://github.com/khangtoh/product-os.git
cd product-os
```

### Codex skill

From the framework checkout, install into an existing target directory:

```sh
python3 scripts/install_skill.py --project ../my-project
```

The optional installer uses Python's standard library and requires no dependencies or network access. It creates `.agents/skills/product-os/` with the skill and a snapshot of the canonical template under `assets/product/`. It preserves other skills and creates no product context. It refuses existing destinations, symlinked skill directories, and installation inside this framework checkout.

Open the target project in Codex, then invoke:

```text
$product-os init
```

If the skill does not appear, start a new session. A bare `$product-os` invocation explains setup readiness and offers the appropriate next step. This release supplies onboarding and orientation; it does not add run, review, or scheduling subcommands.

### Manual skill installation

Without Python, create `.agents/skills/` in your target project. Copy this checkout's `skills/product-os/` there as `product-os/`, then copy `template/product/` into the installed skill as `assets/product/`. The final layout must be:

```text
.agents/skills/product-os/
  SKILL.md
  assets/product/
    ONBOARDING.md
    MODEL.md
    ...the rest of the template
```

Copy both parts; the source skill alone is not a complete package. Preserve existing destinations and do not copy the framework's maintenance AGENTS.md. [Skill updates](CUSTOMIZATION.md#update-the-installed-skill) are separate from changes to project context.

### Portable prompt or manual documentation

For another agent, or to use the documents yourself, copy only the bare instance. This command requires an existing target directory and refuses an existing product path:

```sh
test -d ../my-project && test ! -e ../my-project/product && test ! -L ../my-project/product && cp -R template/product ../my-project/product
```

If a product folder already exists, inspect and merge relevant additions instead of overwriting it. Open the target project and paste:

```text
Read product/ONBOARDING.md and guide me through ProductOS onboarding.
Inspect this project, ask me for the missing product vision and requirements,
help me make unresolved decisions, and save the initial brief and roadmap.
```

You can also follow [the guide](../template/product/ONBOARDING.md) manually. The skill and prompt paths use the same procedure and [completion rules](../template/product/MODEL.md#onboarding-completion).

## 2. Work through the interview

The agent reads existing context, summarizes it, and asks small groups of related questions. It covers product vision, users and their problem, essential workflows, initial requirements and acceptance criteria, boundaries, success, priorities, and the current starting point. You do not need to know ProductOS terminology.

If you are unsure, it offers options and tradeoffs. Choose a hypothesis or explicitly defer a decision with a follow-up. Unknowns stay unknown; an unanswered question is not agreement. The agent saves answers and a checkpoint between rounds so you can pause and resume with the same prompt.

Existing products reuse confirmed answers. A person joining an initialized product receives an orientation and a place to contribute rather than a repeated setup interview. See the [fictional walkthrough](../examples/onboarding.md).

The interaction pattern is inspired by [Impeccable's project setup](https://impeccable.style/tutorials/getting-started/). ProductOS extends the interview to requirements, outcome priorities, and a resumable operating handoff.

## 3. Review the saved context

For a newly initialized project, the resulting layout is:

```text
my-project/
  AGENTS.md                 Existing instructions plus a product-context pointer
  PRODUCT.md                Canonical product contract
  product/
    PRODUCT.md              Navigation pointer to the root contract
    VISION.md
    REQUIREMENTS.md
    STRATEGY.md
    ROADMAP.md
    STATE.md
    operations/
    ...model, guides, templates, and real records as needed
```

Existing established contracts keep their current location. An untouched copied blueprint can be promoted to the root during onboarding; a populated local contract is preserved unless consolidation is requested. If the copied product folder itself is the root of a dedicated context repository, retain its contract in place. See [contract placement](PRODUCT_MD.md).

The promoted contract uses the open PRODUCT.md canonical headings plus ProductOS operating sections. The local blueprint is intentionally incomplete until onboarding establishes the product name, promise, Register, Users, and Product Purpose. After setup, run `npx productmd check` when the checker is available; do not force placeholder values merely to pass it.

For the default new-project layout, merge this into the existing root agent instructions:

```markdown
## Product context

For product work, read PRODUCT.md, product/AGENTS.md, and product/STATE.md
before making changes. Follow linked vision, requirements, roadmap, and
work records as needed. Update the affected context after material
product decisions or results.
```

The agent does this during guided onboarding. Manual users should adapt paths to their layout and preserve unrelated instructions.

## 4. Finish setup and choose the first loop

Check that every required brief area is addressed, hypotheses and explicit deferrals are visible, context is saved, links resolve, and the roadmap agrees with the first action. Correct any misunderstood answers. A complete brief can still need discovery before implementation; the handoff must say so.

Onboarding offers the first loop without starting it. When ready, ask:

```text
Read the product context and current state. Carry out the next eligible
bounded action using the ProductOS loop, verify the result, and save a handoff.
```

Substantive work follows [the operating guide](OPERATING_GUIDE.md) and uses a cycle. A completed setup is not evidence that a product outcome was achieved.

For recurring work, request scheduling setup separately and follow [automation](AUTOMATION.md). A proposed schedule in a document is not a registered task. The current onboarding release neither installs a runner nor registers schedules.
