Feature: Find pages

	As a web user
	I want to search for web pages using keywords
	So that I can discover pages that contain relevant content.

	Scenario: selenium page adapter pypi
		Given I'm on the home page
		When I search for "selenium page adapter pypi"
		Then the selenium_page_adapter PyPi page appears in the search results.
