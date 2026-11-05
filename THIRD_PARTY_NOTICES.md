# Third-party notices

Cave Pony combines two ideas: [Caveman](https://github.com/JuliusBrussee/caveman) (say less) and [Ponytail](https://github.com/DietrichGebert/ponytail) (build less). It is independently written. It is not a fork, and neither project has endorsed it.

## Caveman

- Project: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), © 2026 Julius Brussee.
- Cave Pony 0.1.x reviewed snapshot [`0d95a81`](https://github.com/JuliusBrussee/caveman/tree/0d95a81d35a9f2d123a5e9430d1cfc43d55f1bb0), MIT at that time. The retained licence is in [`licenses/caveman-MIT.txt`](licenses/caveman-MIT.txt).
- Caveman 3.0.0 and later are Apache-2.0. The eval compares against commit `2e068f7`, which `eval/fetch-arms.sh` downloads at run time. No Caveman file is redistributed here.
- Influence: answer first, remove filler, keep code and errors exact, and switch to plain prose for risky content.

## Ponytail

- Project: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), © 2026 DietrichGebert, MIT. The retained licence is in [`licenses/ponytail-MIT.txt`](licenses/ponytail-MIT.txt).
- The eval compares against commit `96608e0`, which is downloaded at run time and not redistributed.
- Influence: read the touched code first, take the first rung of a no-change → reuse → stdlib → dependency → new-code ladder, fix the root cause once, and never cut safety.

## Cave Pony's own parts

The single combined contract and its wording, the proof rule ("never say a check passed unless it ran"), the `Done / Proof / Skipped / Risk` report, the eval tasks and harness, and the pixel-art logo.
