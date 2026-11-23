"""A target's files in the cache (spherex.cachefiles), no network. Moved from the app repo."""
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table

from spherex import cachefiles, download, frames, net, results


def test_target_files_takes_only_its_own_images(tmp_path, monkeypatch):
    for mod in (net, cachefiles):
        monkeypatch.setattr(mod, "CACHE_ROOT", tmp_path)
    monkeypatch.setattr(cachefiles, "CACHE_DIR", tmp_path / "cutouts")
    monkeypatch.setattr(download, "CACHE_DIR", tmp_path / "cutouts")
    monkeypatch.setattr(frames, "TABLE_DIR", tmp_path / "frames")
    monkeypatch.setattr(results, "RESULTS_DIR", tmp_path / "results")
    star = SkyCoord(150.0 * u.deg, 2.0 * u.deg)
    url = "https://irsa.example/level2_X_1D2_spx_l2b.fits"
    (tmp_path / "frames").mkdir()
    Table({"mjd": [60000.0], "access_url": [url]}).write(tmp_path / "frames" / "150_2.ecsv")
    (tmp_path / "cutouts").mkdir()
    mine = download.cache_path(url, star, 0.25)
    other = download.cache_path(url, SkyCoord(150.03 * u.deg, 2.0 * u.deg), 0.25)   # a neighbour, same frame
    mine.write_bytes(b"1" * 100)
    other.write_bytes(b"2" * 100)
    files = cachefiles.target_files("150 2", star)
    assert files["images"] == [mine] and files["n_images"] == 1
    cachefiles.remove_target_files("150 2", star)
    assert not mine.exists() and other.exists() and not (tmp_path / "frames" / "150_2.ecsv").exists()
