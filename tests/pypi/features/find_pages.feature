Feature: Find packages

	As a PyPi user
	I want to search for packages
	So that I can discover packages that contain relevant content.

	Scenario: Search using keywords
		Given I'm on the home page
		When I search for "selenium page adapter"
		Then "selenium_page_adapter" appears in the search results.
		And "ftw.testing" appears in the search results.

	Scenario: Search by exact package name
		Given I'm on the home page
		When I search for "selenium_page_adapter"
		Then I am shown the "selenium_page_adapter" page.
	
	Scenario: Search for garbage keywords
		Given I'm on the home page
		When I search for "I hate test suites that always pass"
		Then no results appear.
