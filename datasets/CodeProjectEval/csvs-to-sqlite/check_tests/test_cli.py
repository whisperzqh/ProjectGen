from click.testing import CliRunner
from csvs_to_sqlite import cli
from six import string_types, text_type
from cogapp import Cog
import sys
from io import StringIO
import pathlib
import sqlite3

CSV = """city,zipcode,category,subcategory,brand,item,price
Austin,78701,Electronics,Phones,Apple,iPhone 14,999
Austin,78701,Electronics,Phones,Samsung,Galaxy S23,899
Austin,78702,Home,Kitchen,Nespresso,Coffee Maker,249
Austin,78702,Home,Kitchen,Dyson,Air Purifier,549
Dallas,75201,Fashion,Shoes,Nike,Air Max,150
Dallas,75201,Fashion,Shoes,Adidas,Ultraboost,180"""

CSV_MULTI = """book,author_1,author_2
Dune,Frank Herbert,Brian Herbert
Foundation,Isaac Asimov,Gregory Benford
Children of Dune,Brian Herbert,Kevin J. Anderson"""

CSV_DATES = """title,published,updated
Breaking News,12th July 2023,3pm on March 15 2024
Weather Alert,11/22/2022,9:30 5 January 2025"""

CSV_DATES_CUSTOM_FORMAT = """title,date
Special Report,05/04/03"""

CSV_CUSTOM_PRIMARY_KEYS = """id1,id2,description
alpha,alpha,aa
alpha,beta,ab
beta,alpha,ba"""

CSV_STRINGS_AND_DATES = """product,revenue,launch_date
iPhone 15,94.3,12 of September in the year 2023
MacBook Air,29.8,5 of June in the year 2023
iPad Pro,18.2,18 of May in the year 2023"""


def test_flat():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(cli.cli, ["test.csv", "test.db"])
        assert result.exit_code == 0
        assert result.output.strip().endswith("Created test.db from 1 CSV file")
        conn = sqlite3.connect("test.db")
        assert [
            (0, "city", "TEXT", 0, None, 0),
            (1, "zipcode", "INTEGER", 0, None, 0),
            (2, "category", "TEXT", 0, None, 0),
            (3, "subcategory", "TEXT", 0, None, 0),
            (4, "brand", "TEXT", 0, None, 0),
            (5, "item", "TEXT", 0, None, 0),
            (6, "price", "INTEGER", 0, None, 0),
        ] == list(conn.execute("PRAGMA table_info(test)"))
        rows = conn.execute("select * from test").fetchall()
        assert [
            ("Austin", 78701, "Electronics", "Phones", "Apple", "iPhone 14", 999),
            ("Austin", 78701, "Electronics", "Phones", "Samsung", "Galaxy S23", 899),
            ("Austin", 78702, "Home", "Kitchen", "Nespresso", "Coffee Maker", 249),
            ("Austin", 78702, "Home", "Kitchen", "Dyson", "Air Purifier", 549),
            ("Dallas", 75201, "Fashion", "Shoes", "Nike", "Air Max", 150),
            ("Dallas", 75201, "Fashion", "Shoes", "Adidas", "Ultraboost", 180),
        ] == rows
        last_row = rows[-1]
        for i, t in enumerate(
            (string_types, int, string_types, string_types, string_types, string_types, int)
        ):
            assert isinstance(last_row[i], t)


def test_extract_columns():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(
            cli.cli,
            "test.csv extracted.db -c category -c subcategory -c brand -c item".split(),
        )
        assert result.exit_code == 0
        assert result.output.strip().endswith("Created extracted.db from 1 CSV file")
        conn = sqlite3.connect("extracted.db")
        assert [
            (0, "city", "TEXT", 0, None, 0),
            (1, "zipcode", "INTEGER", 0, None, 0),
            (2, "category", "INTEGER", 0, None, 0),
            (3, "subcategory", "INTEGER", 0, None, 0),
            (4, "brand", "INTEGER", 0, None, 0),
            (5, "item", "INTEGER", 0, None, 0),
            (6, "price", "INTEGER", 0, None, 0),
        ] == list(conn.execute("PRAGMA table_info(test)"))
        rows = conn.execute(
            """
            select
                city, zipcode, category.value, subcategory.value,
                brand.value, item.value, price
            from test
                left join category on test.category = category.id
                left join subcategory on test.subcategory = subcategory.id
                left join brand on test.brand = brand.id
                left join item on test.item = item.id
            order by test.rowid
        """
        ).fetchall()
        assert [
            ("Austin", 78701, "Electronics", "Phones", "Apple", "iPhone 14", 999),
            ("Austin", 78701, "Electronics", "Phones", "Samsung", "Galaxy S23", 899),
            ("Austin", 78702, "Home", "Kitchen", "Nespresso", "Coffee Maker", 249),
            ("Austin", 78702, "Home", "Kitchen", "Dyson", "Air Purifier", 549),
            ("Dallas", 75201, "Fashion", "Shoes", "Nike", "Air Max", 150),
            ("Dallas", 75201, "Fashion", "Shoes", "Adidas", "Ultraboost", 180),
        ] == rows
        last_row = rows[-1]
        for i, t in enumerate(
            (
                string_types,
                int,
                string_types,
                string_types,
                string_types,
                string_types,
                int,
            )
        ):
            assert isinstance(last_row[i], t)

        assert [
            (1, "Electronics"),
            (2, "Home"),
            (3, "Fashion"),
        ] == conn.execute("select * from category").fetchall()
        assert [(1, "Phones"), (2, "Kitchen"), (3, "Shoes")] == conn.execute(
            "select * from subcategory"
        ).fetchall()
        assert [(1, "Apple"), (2, "Samsung"), (3, "Nespresso"), (4, "Dyson"), (5, "Nike"), (6, "Adidas")] == conn.execute(
            "select * from brand"
        ).fetchall()
        assert [
            (1, "iPhone 14"),
            (2, "Galaxy S23"),
            (3, "Coffee Maker"),
            (4, "Air Purifier"),
            (5, "Air Max"),
            (6, "Ultraboost"),
        ] == conn.execute("select * from item").fetchall()

        fts_tables = [
            r[0]
            for r in conn.execute(
                """
            select name from sqlite_master
            where type='table' and name like '%_fts'
            and sql like '%USING FTS%'
        """
            ).fetchall()
        ]
        assert set(fts_tables) == {
            "category_value_fts",
            "subcategory_value_fts",
            "brand_value_fts",
            "item_value_fts",
        }


def test_fts():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(
            cli.cli, "test.csv fts.db -f category -f brand -f item".split()
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("fts.db")
        assert (
            [("Austin", 78701, "Electronics", "Samsung", "Galaxy S23")]
            == conn.execute(
                """
            select city, zipcode, category, brand, item
            from test
            where rowid in (
                select rowid from test_fts
                where test_fts match 'electronics galaxy'
            )
        """
            ).fetchall()
        )

def test_shape():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(
            cli.cli,
            ["test.csv", "test-reshaped.db", "--shape", "city:City,price:Price(REAL)"],
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("test-reshaped.db")
        assert [
            (0, "City", "TEXT", 0, None, 0),
            (1, "Price", "REAL", 0, None, 0),
        ] == conn.execute("PRAGMA table_info(test);").fetchall()
        results = conn.execute(
            """
            select City, Price from test
        """
        ).fetchall()
        assert [
            ("Austin", 999.0),
            ("Austin", 899.0),
            ("Austin", 249.0),
            ("Austin", 549.0),
            ("Dallas", 150.0),
            ("Dallas", 180.0),
        ] == results
        for city, price in results:
            assert isinstance(city, text_type)
            assert isinstance(price, float)


def test_filename_column():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test1.csv", "w").write(CSV)
        open("test2.csv", "w").write(CSV_MULTI)
        result = runner.invoke(
            cli.cli, [".", "test-filename.db", "--filename-column", "source"]
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("test-filename.db")
        assert [("./test1",), ("./test2",)] == conn.execute(
            "select name from sqlite_master order by name"
        ).fetchall()
        assert [("Austin", "iPhone 14", 999, "./test1")] == conn.execute(
            "select city, item, price, source from [./test1] limit 1"
        ).fetchall()
        assert [
            ("Dune", "Frank Herbert", "Brian Herbert", "./test2")
        ] == conn.execute(
            "select book, author_1, author_2, source from [./test2] limit 1"
        ).fetchall()

def test_fixed_column():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(
            cli.cli,
            [
                "test.csv",
                "test.db",
                "--fixed-column",
                "tag",
                "electronics",
                "--fixed-column",
                "region",
                "southwest",
                "--fixed-column-int",
                "version",
                "2",
                "--fixed-column-float",
                "discount",
                "0.15",
            ],
        )
        assert result.exit_code == 0
        assert result.output.strip().endswith("Created test.db from 1 CSV file")
        conn = sqlite3.connect("test.db")
        assert [
            (0, "city", "TEXT", 0, None, 0),
            (1, "zipcode", "INTEGER", 0, None, 0),
            (2, "category", "TEXT", 0, None, 0),
            (3, "subcategory", "TEXT", 0, None, 0),
            (4, "brand", "TEXT", 0, None, 0),
            (5, "item", "TEXT", 0, None, 0),
            (6, "price", "INTEGER", 0, None, 0),
            (7, "tag", "TEXT", 0, None, 0),
            (8, "region", "TEXT", 0, None, 0),
            (9, "version", "INTEGER", 0, None, 0),
            (10, "discount", "REAL", 0, None, 0),
        ] == list(conn.execute("PRAGMA table_info(test)"))
        rows = conn.execute("select * from test").fetchall()
        assert [
            (
                "Austin",
                78701,
                "Electronics",
                "Phones",
                "Apple",
                "iPhone 14",
                999,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
            (
                "Austin",
                78701,
                "Electronics",
                "Phones",
                "Samsung",
                "Galaxy S23",
                899,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
            (
                "Austin",
                78702,
                "Home",
                "Kitchen",
                "Nespresso",
                "Coffee Maker",
                249,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
            (
                "Austin",
                78702,
                "Home",
                "Kitchen",
                "Dyson",
                "Air Purifier",
                549,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
            (
                "Dallas",
                75201,
                "Fashion",
                "Shoes",
                "Nike",
                "Air Max",
                150,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
            (
                "Dallas",
                75201,
                "Fashion",
                "Shoes",
                "Adidas",
                "Ultraboost",
                180,
                "electronics",
                "southwest",
                2,
                0.15,
            ),
        ] == rows

def test_custom_indexes():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV)
        result = runner.invoke(
            cli.cli,
            ["test.csv", "test.db", "--index", "city", "-i", "brand,item"],
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("test.db")
        assert [
            ('"test_brand_item"', "test"),
            ('"test_city"', "test"),
        ] == conn.execute(
            'select name, tbl_name from sqlite_master where type = "index" order by name'
        ).fetchall()


def test_dates_and_datetimes():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV_DATES)
        result = runner.invoke(
            cli.cli, ["test.csv", "test.db", "-d", "published", "-dt", "updated"]
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("test.db")
        expected = [
            ("Breaking News", "2023-07-12", "2024-03-15T15:00:00"),
            ("Weather Alert", "2022-11-22", "2025-01-05T09:30:00"),
        ]
        actual = conn.execute("select * from test").fetchall()
        assert expected == actual


def test_dates_custom_formats():
    """Newly constructed test"""

    runner = CliRunner()
    with runner.isolated_filesystem():
        open("test.csv", "w").write(CSV_DATES_CUSTOM_FORMAT)
        result = runner.invoke(
            cli.cli, ["test.csv", "test.db", "-d", "date", "-df", "%y/%d/%m"]
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("test.db")
        expected = [("Special Report", "2005-03-04")]
        actual = conn.execute("select * from test").fetchall()
        assert expected == actual

def test_custom_primary_keys():
    """Newly constructed test"""
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("pks.csv", "w").write(CSV_CUSTOM_PRIMARY_KEYS)
        result = runner.invoke(
            cli.cli, ("pks.csv pks.db -pk id1 --primary-key id2").split()
        )
        assert result.exit_code == 0
        conn = sqlite3.connect("pks.db")
        pks = [
            r[1] for r in conn.execute('PRAGMA table_info("pks")').fetchall() if r[-1]
        ]
        assert ["id1", "id2"] == pks
