# Changelog

## 1.0.0 (2026-11-23)

First release as its own package, `spherex-quicklook` (import name `spherex`), split from the
[SPHEREx Flipbook app](https://github.com/UTMOS12345/spherex_project) with its history. The
library is the same as in the app's 1.0.0 apart from the changes below; scientific results
are byte-identical (`RESULTS_VERSION` unchanged), so results saved by the app are reused.

- **A stable public interface:** `spherex.api`, as documented in docs/API.md (see "Stability"
  in the README). New in it, so an app never needs the internal modules: `cache_root`,
  `download_workers`, `frame_cache_info`, `clear_frame_cache`, `prestart_workers`,
  `WORKER_IDLE_S`, `result_key`, `preload_results`, `catalogue_names`, `parse_cutout_name`,
  and `Estimate` and `set_style` re-exported.
- **No matplotlib backend is forced:** importing spherex no longer calls
  `matplotlib.use("Agg")`. Headless, matplotlib picks Agg itself; apps that draw from threads
  set it (paramost does). The library's own worker processes still use Agg.
- **Cache location:** `SPHEREX_CACHE`, else the per-user cache folder, still named `paramost`
  so that existing caches stay where they are. The rule "use `cache/` of a source checkout"
  moved to the app, which sets `SPHEREX_CACHE` for its own checkout.
- No streamlit dependency.
