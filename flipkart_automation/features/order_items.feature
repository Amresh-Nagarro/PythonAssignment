Feature: Flipkart Item Ordering

  Scenario: Order two items and verify cart operations
    Given I open Flipkart website
    When I search for "Samsung S24 128 GB" and select the second item
    And I check the item's availability with pin code "122017" and add it to the cart
    And I return to the home page
    And I search for "bajaj iron majesty" and select the second item
    And I check the item's availability with pin code "122017" and add it to the cart
    Then I navigate to the cart
    And I verify both items are present and total price reflects the sum
    And I remove one item and confirm the total price is updated
