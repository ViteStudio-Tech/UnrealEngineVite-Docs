# Commit Conventions

<tldr>
<p>
Prefix every commit with one of six category tags. Backports and plugin additions must link to the original
commit or repository.
</p>
</tldr>

A fork that tracks an upstream engine accumulates a long history of changes from many sources. Being able
to scan that history and tell an optimisation from a rendering feature from a backport is what makes future
merges tractable.

## Prefixes

Use one of the following at the start of the commit subject:

| Prefix | Use for |
|---|---|
| `[Optimization]` | Performance work with no behaviour change |
| `[Rendering Feature]` | New or changed rendering functionality |
| `[VR]` | VR-specific work |
| `[Mobile]` | Mobile-specific work |
| `[Plugin]` | Adding, updating or removing a plugin |
| `[Fix]` | Bug fixes |

Examples:

```
[Optimization] Skip overlap event dispatch for actors with no bound delegates
[Rendering Feature] Add Smooth Terminator input to Callisto BRDF
[Plugin] Add Kawaii Physics 1.18.0, backported from UE5
[Fix] Guard RTXDI CVar behind ShouldRenderRayTracingSampledLighting
```

If a change genuinely spans categories, split it. A commit that is both an optimisation and a rendering
feature is usually two commits.

## Attribution

<warning>
When making backports or adding a plugin, include the correct links to the original commits or
repositories in the commit body.
</warning>

This is not a courtesy, it is a practical requirement. Without the link, nobody can determine what version
was integrated, whether upstream has since fixed a bug in it, or whether the licence permits redistribution.

```
[Plugin] Add Kawaii Physics 1.18.0, backported from UE5

Source: https://github.com/pafuhana1213/KawaiiPhysics
Upstream tag: v1.18.0
Changes: UE5 API calls replaced with 4.27 equivalents in
KawaiiPhysicsEditMode.cpp and AnimNode_KawaiiPhysics.cpp
```

For backports of individual upstream commits, link the commit itself, not just the repository. See
[Backporting](Backporting.md).

## Commit body

The subject line says what changed. The body should say why, and what a reviewer needs to know:

- What problem the change solves
- Measured impact, for anything claiming to be an optimisation
- Any console variable or [compile-time switch](Compile-Time-Switches.md) added, with its default
- Anything deliberately left undone

Measured impact matters. A commit prefixed `[Optimization]` with no numbers is an assertion, not a result.
See [Profiling](Profiling.md) for how to produce a credible before-and-after.

## Branches

| Rule | |
|---|---|
| Work in progress goes on alternative branches | Do not push half-finished work to shared branches |
| Note what remains | A brief comment on the branch or in the commit body |
| Delete temporary branches | Once merged or abandoned |
| Tell other forkers | So parallel effort is not wasted |

## Console variables and switches

New console variables follow the engine's existing naming. Vite-specific ones are prefixed with the
subsystem, then `Vite`:

| Example | Subsystem |
|---|---|
| `r.Vite.SMAA.Mode` | Renderer |
| `r.Vite.SSAO` | Renderer |
| `p.VitePhysXFixedTimestep.Enabled` | Physics |

Compile-time switches use the `VITE_` prefix and must be defined with a default in
`Engine\Source\Runtime\Core\Public\Misc\CoreDefines.h`:

```c++
#ifndef VITE_MY_FEATURE
	#define VITE_MY_FEATURE 0
#endif
```

Document any new switch in [Compile-Time Switches](Compile-Time-Switches.md) in the same change. A switch
that is not documented will be discovered by someone debugging a console variable that silently does
nothing &mdash; which is exactly the failure mode `VITE_RT_PSO_DEBLOAT` caused before it was written up.

## See also

- [Contributing](Contributing.md)
- [Coding Guidelines](Coding-Guidelines.md)
- [Backporting](Backporting.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
