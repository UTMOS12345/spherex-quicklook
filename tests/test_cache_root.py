"""Where the cache lives: SPHEREX_CACHE, else the user cache folder named "paramost"."""
from spherex import net


def test_env_wins(monkeypatch, tmp_path):
    monkeypatch.setenv("SPHEREX_CACHE", str(tmp_path / "c"))
    assert net.default_cache_root() == tmp_path / "c"


def test_user_cache_keeps_the_paramost_name(monkeypatch, tmp_path):
    """The folder existing users already have (the library shipped inside paramost before 1.0)."""
    monkeypatch.delenv("SPHEREX_CACHE", raising=False)
    import platformdirs
    monkeypatch.setattr(platformdirs, "user_cache_dir", lambda name, appauthor=None: str(tmp_path / "user" / name))
    assert net.default_cache_root() == tmp_path / "user" / "paramost"


def test_a_cache_folder_next_to_the_package_is_not_used(monkeypatch, tmp_path):
    """The source-checkout cache/ rule belongs to the app (paramost sets SPHEREX_CACHE for it)."""
    monkeypatch.delenv("SPHEREX_CACHE", raising=False)
    repo = tmp_path / "repo"
    (repo / "spherex").mkdir(parents=True)
    (repo / "cache").mkdir()
    (repo / "pyproject.toml").write_text("")
    monkeypatch.setattr(net, "__file__", str(repo / "spherex" / "net.py"))
    import platformdirs
    monkeypatch.setattr(platformdirs, "user_cache_dir", lambda name, appauthor=None: str(tmp_path / "user" / name))
    assert net.default_cache_root() == tmp_path / "user" / "paramost"
