# Third-party notices

This Windows x64 preview includes a Rust worker, the MIT-licensed KryptoCore
library and the self-contained .NET 10.0.9 Windows runtime. Original license
and copyright texts accompany the distribution in third-party/. The resolved
normal/build Rust graph, across targets and workspace feature unification,
is recorded in RUST-DEPENDENCIES.tsv; not every entry is linked on Windows.
Preserve the applicable notices when redistributing incorporated components.
Build-tool and Rust standard-library notices accompany the runtime notices.
First-party application code, including its interface, is MIT licensed at
https://github.com/kryptocorelabs/apps-source. Third-party components retain
their own terms; this change does not relicense them.

Rescue does not bundle Tor. ClamAV is an optional external scanner, not part of this distribution.
