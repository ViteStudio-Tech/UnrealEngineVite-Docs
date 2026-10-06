# Tools and Automation

<tldr>
<p>
Vite ships batch tooling for the whole engine lifecycle: <code>ViteSetup.bat</code> for setup and building,
<code>RunUAT.bat</code> for installed builds, the <code>LocalBuilds\</code> scripts for packaging and
registration, and <code>WipeShaderCache.bat</code> for when caches go stale.
</p>
</tldr>

Building Unreal from source involves a long sequence of steps, each with its own failure modes. Vite wraps
that sequence in tooling so the common paths do not require remembering the exact command lines.

## In this section

| Topic | Covers |
|---|---|
| [ViteSetup Assistant](ViteSetup.md) | The guided setup and build assistant, and its menu mode |
| [Installed Builds](Installed-Builds.md) | Producing and packaging a redistributable binary engine |
| [Cache Management](Cache-Management.md) | Wiping shader and DDC caches when things go wrong |
| [Compiler Explorer](Compiler-Explorer.md) | MSVC vs Clang assembly on Godbolt; timings go to Quick Bench or a local bench |

## The tools at a glance

| Tool | Location | Purpose |
|---|---|---|
| `ViteSetup.bat` | Engine root | Guided nine-step setup with an Express path, or a menu of individual operations |
| `ViteDefaults.bat` | Engine root | Switches the overlap and skeletal mesh defaults between Vite and stock 4.27. See [Engine Default Changes](Engine-Defaults.md). |
| `RunUAT.bat` | Engine root | Installed engine build via BuildGraph |
| `WipeShaderCache.bat` | Engine root | Clears engine-level shader and DDC caches |
| `LocalBuilds\CompressBuild*.bat` | `LocalBuilds\` | Packages a staged installed build into a 7z archive |
| `LocalBuilds\RegistryAdd.bat` | `LocalBuilds\` | Registers the build as `UEViteFork` (ViteSetup uses `UE_ViteFork`) |
| `LocalBuilds\RegistryRemove.bat` | `LocalBuilds\` | Unregisters it |
| `LocalBuilds\MakeShortcut.bat` | `LocalBuilds\` | Creates `UEViteFork.lnk` |
| `devops\ueVite-debloat-*.bat` | `devops\` | Engine debloat suite &mdash; see [Debloat Guide](Debloat-Guide.md) |
| `devops\ueVite-ApplyVitePluginDefaults.bat` | `devops\` | Applies or reverts Vite's engine plugin profile &mdash; see [Engine Default Changes](Engine-Defaults.md#disabled-plugins) |

## Which one you want

<deflist>
<def title="I just cloned the repository">
Run <code>ViteSetup.bat</code> and take the Express path. It walks the whole sequence from environment check
to a launched editor. See <a href="ViteSetup.md">ViteSetup Assistant</a>.
</def>
<def title="I want a binary engine to hand to artists">
Run <code>ViteSetup.bat</code> and choose the precompiled binary option at step 2, or drive
<code>RunUAT.bat</code> and the <code>LocalBuilds\</code> scripts directly. See
<a href="Installed-Builds.md">Installed Builds</a>.
</def>
<def title="Shaders are behaving strangely after a change">
Run <code>WipeShaderCache.bat</code>. See <a href="Cache-Management.md">Cache Management</a>.
</def>
<def title="The engine is taking too much disk space">
Run <code>ViteSetup.bat menu</code> and choose option 9, or run the <code>devops\</code> debloat suite
directly. See <a href="Debloat-Guide.md">Debloat Guide</a>.
</def>
<def title="I only need to regenerate project files">
<code>ViteSetup.bat menu</code> and choose option 3, or run <code>GenerateProjectFiles.bat</code>
directly.
</def>
<def title="I want to compare MSVC and Clang codegen">
Open <a href="https://gcc.godbolt.org/">Compiler Explorer</a>. It shows assembly, not timings. See
<a href="Compiler-Explorer.md">Compiler Explorer</a>.
</def>
</deflist>

## See also

- [Build from Source](Build-From-Source.md)
- [Toolchain Requirements](Toolchain-Requirements.md)
- [Build Troubleshooting](Build-Troubleshooting.md)
- [Debloat Guide](Debloat-Guide.md)
- [Compiler Explorer](Compiler-Explorer.md)
