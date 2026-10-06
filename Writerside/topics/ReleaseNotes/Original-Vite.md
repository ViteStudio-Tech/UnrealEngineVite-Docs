# Original Vite

<tldr>
<p>
The first Vite line, built on <b>NVIDIA's NvRTX 5.0</b> (Unreal Engine 5). It proved out the PhysX and
ray-tracing direction, then was retired in November 2025 when matched tests showed the 4.27-based NvRTX
branch to be faster. It is archived and no longer supported; its public repository history was not
preserved.
</p>
</tldr>

| Status | Base | Superseded by |
|---|---|---|
| Archived | NvRTX 5.0 (Unreal Engine 5) | [ueVite25 LTS](ueVite25-LTS.md), November 2025 |

## What it established

- **PhysX on a modern engine.** The original line ported PhysX back into a UE5-era codebase, which is where
  Vite's position on Chaos started.
- **Ray tracing without Lumen.** NvRTX's RTXGI/DDGI path, rather than Lumen, as the primary GI solution.
- **Measured decisions.** The comparisons run on this line &mdash; ray-traced GI frame rate and the cost
  of integrating PhysX into UE5 &mdash; are what drove the move to a 4.27 base.

## Why it was replaced

Matched ray-tracing tests ran slower on the NvRTX 5.0 base than on NvRTX Caustics 4.27, and keeping PhysX
working against UE5's physics architecture was a continuing cost. The full reasoning is in
[Why NvRTX 4.27](Why-NvRTX-427.md) and the
[base transition record](https://docs.google.com/document/d/1gA0MGkzeWWzKkgwBDOP5xRPouSKaOIW6xlPZ2q6BXO0/edit).

## Commit record

No verifiable public commit history survives for this line, so this page has no commit table. The
transition record above is the authoritative account.

## See also

- [All release notes](Release-Notes.md)
- [ueVite25 LTS](ueVite25-LTS.md)
- [UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md)
