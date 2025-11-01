#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_geotext
----------------------------------

Functional checks for `geotext` module.
(Not identical to official unit tests — for model evaluation use only)
"""

import unittest
from geotext.geotext import GeoText


class CheckGeoText(unittest.TestCase):
    def setUp(self):
        pass

    def test_detect_cities_from_english_text(self):
        text = (
            "During my trip across Europe, I stopped in London, "
            "visited Paris, and later flew to Berlin before returning to Madrid. "
            "Next year, I plan to explore Prague and Vienna."
        )
        result = GeoText(text).cities
        expected = ['London', 'Paris', 'Berlin', 'Madrid', 'Prague', 'Vienna']
        self.assertEqual(result, expected)

        text = (
            "In the United States, major tech companies are based in San Francisco, "
            "Seattle, and Austin. Some startups also appear in Boston."
        )
        result = GeoText(text).cities
        expected = ['San Francisco', 'Seattle', 'Austin', 'Boston']
        self.assertEqual(result, expected)

    def test_detect_countries_from_various_sentences(self):
        text = (
            "I have worked in Canada and Australia, but I studied in Germany. "
            "Someday I wish to visit Brazil and South Africa too."
        )
        result = GeoText(text).countries
        expected = ['Canada', 'Australia', 'Germany', 'Brazil', 'South Africa']
        self.assertEqual(result, expected)

        text = (
            "The project involves cooperation between Norway, Sweden, and Denmark."
        )
        result = GeoText(text).countries
        expected = ['Norway', 'Sweden', 'Denmark']
        self.assertEqual(result, expected)

    def test_detect_nationalities_in_text(self):
        text = (
            "Italian chefs make great pasta, while Indian engineers excel in software. "
            "Spanish artists are also quite creative, and Korean pop culture is booming."
        )
        result = GeoText(text).nationalities
        expected = ['Italian', 'Indian', 'Spanish', 'Korean']
        self.assertEqual(result, expected)

        text = "They met with Japanese officials."
        result = GeoText(text).nationalities
        expected = ['Japanese']
        self.assertEqual(result, expected)

    def test_country_mentions_frequency(self):
        text = (
            "Beijing is in China, and Shanghai is also in China. "
            "Tokyo is located in Japan, while Osaka is another Japanese city."
        )
        result = GeoText(text).country_mentions
        # CN = China, JP = Japan
        expected = {'CN': 4, 'JP': 3}
        self.assertEqual(result, expected)

        text = (
            "I have visited Nairobi (Kenya) and Cairo in Egypt, "
            "and next I will travel to Cape Town, South Africa."
        )
        result = GeoText(text).country_mentions
        expected = {'KE': 2, 'EG': 2, 'ZA': 2}
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
