"""The app-support calls of spherex.api: what paramost uses instead of the internal modules."""
from pathlib import Path

from spherex import api, net, results, workers, framecache


def test_cache_root_is_the_active_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(net, "CACHE_ROOT", tmp_path)
    assert api.cache_root() == tmp_path and isinstance(api.cache_root(), Path)


def test_result_key_matches_the_saved_results_folder():
    assert api.result_key("Barnard's Star") == results.safe_name("Barnard's Star")
    assert results.target_dir("Barnard's Star").name == api.result_key("Barnard's Star")


def test_parse_cutout_name():
    assert api.parse_cutout_name("level2_2026W19_2A_0952_1D3_spx_l2b-v20__133.79458_-7.24528_4.0.fits") == {
        "stem": "level2_2026W19_2A_0952_1D3_spx_l2b-v20", "ra": "133.79458", "dec": "-7.24528", "size": "4.0"}
    assert api.parse_cutout_name("frames.ecsv") is None


def test_catalogue_names_parse_without_network():
    names = api.catalogue_names()
    assert "WISE 0855" in names and len(names) == 5
    for n in names:
        assert api.resolve(n)["known"]


def test_frame_cache_calls(monkeypatch, tmp_path):
    monkeypatch.setattr(framecache, "FRAME_DIR", tmp_path / "frames_proc")
    info = api.frame_cache_info()
    assert info["entries"] == 0 and info["folder"] == tmp_path / "frames_proc"
    assert api.clear_frame_cache() == (0, 0)


def test_reexports():
    from spherex.progress import Estimate
    from spherex.plots import set_style
    import spherex
    assert api.Estimate is Estimate and api.set_style is set_style is spherex.set_style
    assert api.WORKER_IDLE_S == workers.IDLE_S
    assert isinstance(api.download_workers(), int) and api.download_workers() >= 1
