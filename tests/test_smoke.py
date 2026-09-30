import compileall
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

import debts

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ("debts.py", "prepare.py", "auto_mail.py")


def test_scripts_compile():
    for name in SCRIPTS:
        assert compileall.compile_file(str(ROOT / name), quiet=1)


def test_selenium4_locators_replaced_removed_apis():
    for name in ("debts.py", "auto_mail.py"):
        source = (ROOT / name).read_text(encoding="utf-8")
        assert "find_element_by_" not in source
        assert "chromedriver" not in source.lower()
        assert "By." in source
        assert "--headless=new" in source


def test_xpath_soup_indexes_repeated_tags():
    soup = BeautifulSoup("<div><p>a</p><p id='t'>b</p></div>", "html.parser")
    node = soup.find(id="t")
    assert debts.xpath_soup(node) == "/div/p[2]"


def test_client_csv_lookup_on_pandas3(tmp_path):
    # Same read and column access the scripts use: cp1253 via the "1253" alias, dtype=str, .values[0].
    raw = "LAST,NAME,VATID,USER,PWD,EMAIL\nΓΚΑΤΖΙΑΡΗΣ,ΠΑΝΤΕΛΗΣ,123,user,secret,client@example.com\n"
    path = tmp_path / "clients.csv"
    path.write_bytes(raw.encode("cp1253"))

    db = pd.read_csv(path, encoding="1253", sep=",", dtype=str)
    vat_id = "123"
    true_name = " ".join(
        [
            db.loc[db["VATID"] == vat_id, "LAST"].values[0],
            db.loc[db["VATID"] == vat_id, "NAME"].values[0],
        ]
    )
    assert true_name == "ΓΚΑΤΖΙΑΡΗΣ ΠΑΝΤΕΛΗΣ"

    users = list(zip(db[db.columns[3]].values, db[db.columns[4]].values))
    assert users == [("user", "secret")]

    recon = db[db["VATID"] == vat_id]
    assert not recon.empty
    assert len(recon) == 1
    assert recon[recon.columns[5]].values[0] == "client@example.com"
