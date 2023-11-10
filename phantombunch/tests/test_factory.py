import collections
import re
import pytest

import phantombunch as pb
import phantombunch.util as pbu

UINT_RE = re.compile(r"^[0-9]+$")  # unsigned integer regex


class TestCID:
    def test_type(self):
        # Check that the CID is a string.
        assert isinstance(pb.cid(), str)

    def test_length(self):
        # Check that the CID is 8 digits long.
        assert len(pb.cid()) == 8

    def test_all_digits(self):
        # Check that the CID is all digits.
        assert UINT_RE.search(pb.cid())

    def test_first_digit(self):
        # Check that the first digit is always 0.
        assert int(pb.cid()[0]) == 0

    def test_second_digit(self):
        # Check that the second digit is always 1 or 2.
        assert int(pb.cid()[1]) in [1, 2]

    def test_remaining_digits(self):
        # Check that the remaining 6 digits are always between 0 and 9.
        assert UINT_RE.search(pb.cid()[2:])

    def test_all_digits_present(self):
        # Check that all digits (0-9) can be present in the CID.
        assert len(set("".join(pb.cid() for _ in range(50)))) == 10

    def test_convertible(self):
        # Check that the CID is convertible to an integer.
        assert isinstance(int(pb.cid()), int)


class TestGender:
    def test_type(self):
        # Check that gender is a string.
        assert isinstance(pb.gender(), str)

    def test_values(self):
        # Check the output is one of the expected ones.
        assert pb.gender() in pbu.GENDERS

    def test_probability_certain_outcome(self):
        # Check that the probabilities are respected.
        assert pb.gender(distribution={"outcome1": 1, "outcome2": 0}) == "outcome1"

    def test_probabilities_uncertain_outcome(self):
        # Check that the probabilities are respected.
        distribution = {"male": 0.2, "female": 0.75, "nonbinary": 0.05}
        counts = collections.Counter(
            pb.gender(distribution=distribution) for _ in range(1000)
        )
        assert counts["nonbinary"] < counts["male"] < counts["female"]


class TestTitle:
    def test_type(self):
        # Check that title is a string.
        assert isinstance(pb.title(), str)

    def test_use_period(self):
        # Check that the title ends with a period if use_period is True.
        assert pb.title(use_period=True).endswith(".")

    def test_no_period(self):
        # Check that the title does not end with a period if use_period is False.
        assert not pb.title(use_period=False).endswith(".")

    def test_startswith_upper(self):
        # Check that the title starts with an uppercase M.
        assert pb.title().startswith("M")

    def test_no_gender(self):
        # Check that the title is one of the expected ones.
        assert pb.title() in pbu.TITLES

    def test_male(self):
        # Check that the title is one of the expected ones for a male.
        assert pb.title(genderval="male") == "Mr"

    def test_female(self):
        # Check that the title is one of the expected ones for a female.
        assert pb.title(genderval="female") in ["Ms", "Mrs", "Miss"]

    def test_nonbinary(self):
        # Check that the title is one of the expected ones for a nonbinary.
        assert pb.title(genderval="nonbinary") == "Mx"

    def test_wrong_gender(self):
        # Check the exception is raised.
        with pytest.raises(ValueError):
            pb.title(genderval="wrong")


class TestCourse:
    def test_type(self):
        assert isinstance(pb.course(), str)

    def test_values(self):
        assert pb.course() in pb.COURSES

    def test_probabilities(self):
        # Check that the probabilities are respected.
        probabilities = [0.2, 0.75, 0.05]
        courses = [pb.course(probabilities=probabilities) for _ in range(10000)]
        counts = collections.Counter(courses)
        assert counts["gems"] < counts["acse"] < counts["edsml"]


class TestCountry:
    def test_type(self):
        assert isinstance(pb.country(), str)

    def test_values(self):
        assert pb.country() in pb.COUNTRIES

    def test_bias(self):
        bias = {"China": 0.5, "United Kingdom": 0.2}
        countries = [pb.country(bias=bias) for _ in range(100)]
        counts = collections.Counter(countries)
        assert counts["China"] > counts["United Kingdom"] > counts["Croatia"]


class TestName:
    def test_type(self):
        assert isinstance(pb.name(), str)

    def test_space(self):
        assert " " in pb.name()

    def test_country_gender(self):
        for _ in range(25):
            assert isinstance(pb.name(gender=pb.gender(), country=pb.country()), str)

    def test_china(self):
        names = set(" ".join(pb.name(country="China") for _ in range(100)).split())
        assert len({"Jang", "Jing", "Wei", "Fang", "Lei", "Tao"} & names) > 0


class TestUsername:
    def test_type(self):
        assert isinstance(pb.username("John Smith"), str)

    def test_length(self):
        assert 4 <= len(pb.username("John Smith")) <= 7

    def test_lower(self):
        assert pb.username("John Smith").islower()

    def test_no_space(self):
        assert " " not in pb.username("John Smith")

    def test_first_letter(self):
        assert pb.username("John Smith")[0] == "j"

    def test_last_letter(self):
        assert "s" in pb.username("John Smith")

    def test_digits(self):
        assert 2 <= sum(i.isdigit() for i in pb.username("John Smith")) <= 4

    def test_letters(self):
        assert 2 <= sum(i.isalpha() for i in pb.username("John Smith")) <= 3


class TestEmail:
    def test_type(self):
        assert isinstance(pb.email(), str)

    def test_at(self):
        assert "@" in pb.email()

    def test_dot(self):
        assert "." in pb.email()

    def test_domain(self):
        assert pb.email(domain="gmail.com").endswith("@gmail.com")

    def test_valid(self):
        assert all(pb.valid_email(pb.email()) for _ in range(25))
