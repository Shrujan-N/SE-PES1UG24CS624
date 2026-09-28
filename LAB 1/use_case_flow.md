# Use-Case Flow Specification

**Use Case ID:** UC-02
**Use Case Name:** Manage Subscription

**Actors:** Subscriber (Primary)

**Description:** This use case allows a registered and authenticated Subscriber to view their subscription details and perform modifications such as pausing, skipping a week, or cancelling their subscription.

**Preconditions:**
1. The Subscriber must have an active account.
2. The Subscriber must be successfully logged into the system.
3. The Subscriber must have an existing, active subscription.

**Postconditions:**
*   **On Success:** The subscriber's subscription status is updated in the system (e.g., status changed to "Paused"). A confirmation email is dispatched to the subscriber's registered email address.
*   **On Failure:** The subscriber's subscription status remains unchanged. The system displays an appropriate error message.

---

### Main Success Scenario (Pausing a Subscription)

| Step | Actor Action                                      | System Response                                                                                                      |
| :--- | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------- |
| 1    | Subscriber navigates to the "My Subscription" page. | System retrieves and displays the current subscription status, next billing date, and available management options ("Pause", "Skip Week", "Cancel"). |
| 2    | Subscriber clicks the "Pause" button.             | System checks if the modification request is outside the 12-hour lock-in period before the next dispatch (as per NFR-001). The check passes. |
| 3    |                                                   | System displays a confirmation dialog: "Are you sure you want to pause your subscription? Your deliveries will resume on [Date]." |
| 4    | Subscriber clicks "Confirm Pause".                | System updates the subscription status to "Paused" in the database.                                                  |
| 5    |                                                   | System displays a success message on the screen: "Your subscription has been paused."                                |
| 6    |                                                   | System triggers the email service to send a confirmation email to the Subscriber.                                    |
| **-**| **Use Case Ends**                                 |                                                                                                                      |

---

### Alternate Flow (Modification Deadline Passed)

This flow begins at Step 2 of the Main Success Scenario.

| Step | Actor Action                          | System Response                                                                                                                                                                     |
| :--- | :------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2a   |                                       | The system checks if the modification request is outside the 12-hour lock-in period. The check **fails**; the request is within 12 hours of the next scheduled dispatch. |
| 2b   |                                       | The system displays an error message: "Subscription changes cannot be made less than 12 hours before your next delivery. Your next meal is already being prepared."    |
| **-**| **Use Case Ends**                     | The subscription status remains active.                                                                                                                                             |