# SMMS Feature Plan and Update Notes

## Purpose
This document is a living planning sheet for the Smart Mess Management System (SMMS). It collects the current feature scope, extra feature ideas for Flutter and web, and review questions so the plan can be updated as the project evolves.

## Product Direction
- Build the app in Flutter so it works on Android, iOS, and web from one codebase.
- Keep the first version focused on core mess operations, then add automation and smart analytics.
- Design the UI for both mobile and desktop so the same app works well on website deployment.

## Current Scope Already Visible In The Prototype
- Student and admin login flow.
- Student dashboard with crowd status, QR pass, meal toggle, menu preview, and personal stats.
- Menu browsing with meal-wise items.
- Leave management.
- Dish voting.
- Feedback collection.
- Notifications.
- Profile screen.
- Admin dashboard.
- QR scanner for attendance.
- Menu management.
- Analytics.
- Inventory tracking.
- Feedback inbox.
- User management.
- Kitchen display.
- Advanced features already planned in the codebase: crowd heatmap, surge management, simulation, leftover routing, and weather-aware planning.

## Feature Backlog

### A. Core Student Features
- Secure login with role selection (login with the help of college email id with otp).
- University SSO support.
- Student profile with photo, roll number, preferences, allergies, and meal history.
- Daily dashboard with live mess occupancy.
- QR meal pass generation.
- Meal attendance marking.
- Not-eating toggle for daily meal skip.
- Today's menu view.
- Full weekly menu view.
- Nutritional information for dishes.
- Allergen warnings.
- Dish ratings.
- Meal-wise notifications.
- Leave request submission.
- Leave history.
- Feedback submission.
- Complaint tracking.
- Dish voting for upcoming menu items.
- Reward points and rebate balance.
- Meal reminders.
- Queue or waiting-time estimate.

### B. Core Admin Features
- Admin login and dashboard.
- Live attendance scanning.
- QR validation and fraud prevention, including student ID card scan before plate issuance.
- Menu planning for daily and weekly meals.
- Edit dish items and categories.
- Approval flow for menu changes.
- Inventory tracking with low-stock alerts.
- Kitchen display for live serving status.
- Feedback inbox with sorting and filtering.
- User management for students and staff.
- Manual attendance override with audit trail.
- Analytics dashboard for footfall, ratings, waste, and peak times.
- Export reports in PDF or CSV.
- Notifications management.

### C. Smart And Advanced Features

#### 1. QR Validation And Fraud Prevention
- Generate time-bound QR passes for each meal window.
- Scan the student ID card at the mess counter before the plate is served.
- Validate the QR code against the user profile, meal slot, and current date.
- Cross-check the scanned ID card with the QR pass and student account.
- Block replay attacks by expiring codes after a short interval.
- Prevent duplicate meal claims by checking attendance history and serving logs.
- Lock the serving action until both ID verification and QR validation succeed.
- Allow a supervised manual override for lost card, damaged QR, or emergency cases.
- Log invalid scans, mismatched IDs, repeated attempts, and override actions for audit review.
- Store scan timestamp, counter number, and operator ID for traceability.
- Support quick error messages for invalid, expired, or already-used passes.
- Keep the flow fast enough for peak-time serving while still preventing misuse.

#### Supporting Serving Counter Features
- ID card scanner integration for the admin or counter staff device.
- Student lookup screen showing name, roll number, meal eligibility, and leave status.
- One-tap approve or reject action after validation.
- Visual indicator for verified, blocked, pending, and overridden scans.
- Counter-wise serving logs for audit and reconciliation.
- Duplicate detection if the same student tries to collect a second plate.
- Optional offline queue so scans can continue briefly if the network drops.
- Notification to the student when a plate is successfully issued or rejected.
- Analytics on scan failures, peak counter load, and override frequency.

#### 2. Crowd Heatmap Inside The Mess
- Visualize live congestion across counters, seating areas, entry points, and wash zones.
- Use color-coded zones so staff can quickly identify bottlenecks.
- Show heat intensity by current scans, manual updates, or sensor data.
- Allow admin users to drill into a zone to see the cause of crowding.
- Support both quick mobile summary and large-screen kitchen or admin views.

#### 3. Footfall Prediction By Time Slot
- Forecast student count for each meal block based on past attendance trends.
- Highlight expected peak windows and low-traffic windows.
- Help kitchen staff prepare quantity, staffing, and serving speed in advance.
- Use historical attendance, academic events, weekday patterns, and weather inputs.
- Display confidence bands so managers know how reliable the forecast is.

#### 4. Weather-Based Menu Suggestions
- Adapt menu suggestions using temperature, rain, humidity, and seasonal patterns.
- Recommend hot meals, cold drinks, or lighter foods based on the forecast.
- Improve student comfort and food acceptance during extreme weather.
- Let admins see why a suggestion was made before applying it to the menu.
- Combine weather data with allergies, nutrition goals, and stock levels.

#### 5. Academic Calendar-Based Demand Forecasting
- Increase or reduce expected demand based on exams, holidays, fests, and semester breaks.
- Predict unusual spikes when students stay on campus longer than normal.
- Link the mess plan to the institute calendar so planning is more accurate.
- Support manual event overrides for special college activities.
- Use calendar events to guide procurement and meal preparation.

#### 6. Surge Management And Incentive Slots
- Detect meal slots likely to become overcrowded.
- Offer reward points, bonus rebates, or badges to students who dine during low-traffic periods.
- Shift some meal demand away from the peak window.
- Let admins configure incentive strength by day, event, or occupancy level.
- Show the effect of incentives on queue reduction and crowd balancing.

#### 7. Happy-Hour Style Dining Rewards
- Create short off-peak windows where students get extra points or benefits.
- Combine rewards with menu highlights so the offer feels attractive.
- Display countdowns for active bonus windows.
- Track how many students responded to each reward campaign.
- Reuse the same reward engine for attendance streaks, reviews, or referrals later.

#### 8. Digital Twin Or Simulation Of Expected Load
- Simulate the next day or next week’s mess traffic before service begins.
- Test what happens if menu items, timings, or incentives are changed.
- Compare different serving strategies without affecting real users.
- Help management choose between staffing, portion size, and queue strategies.
- Present the simulation in a simple dashboard with scenario comparison cards.

#### 9. Waste Prediction And Optimization
- Estimate leftover food before cooking starts.
- Compare current stock, expected attendance, and menu preference history.
- Suggest smaller or larger batch sizes for each meal.
- Show which dishes repeatedly generate more waste.
- Reduce cost by making procurement and portion decisions more accurate.

#### 10. Leftover Routing Suggestions
- Recommend whether leftovers should be reused, repurposed, donated, or discarded.
- Suggest safe next-use recipes where policy allows.
- Support local shelter or NGO routing if the campus has an approved partner.
- Track leftovers by item, weight, and disposition status.
- Keep a record of waste-routing decisions for compliance and sustainability reporting.

#### 11. Ingredient Fatigue Detection
- Detect when the same ingredient is used too often across consecutive days.
- Flag ingredient repetition that can reduce student satisfaction.
- Suggest alternatives to improve menu variety while keeping cost under control.
- Help the chef rotate ingredients across seasonal and weekly plans.
- Use the output to balance variety, nutrition, and procurement stability.

#### 12. A/B Testing For New Dishes
- Compare two dish options before fully adding them to the weekly menu.
- Collect student votes, ratings, and repeat interest.
- Measure which dish performs better by meal type and user segment.
- Use results to reduce bad menu decisions.
- Keep test results in the analytics dashboard for future planning.

#### 13. Recipe Bank And Reusable Menu Templates
- Store approved recipes with ingredients, portions, calories, and prep notes.
- Reuse recipes for weekly menu planning and seasonal rotation.
- Speed up menu creation by using templates for breakfast, lunch, snacks, and dinner.
- Reduce dependency on manual editing every week.
- Let admin and kitchen staff maintain a standardized recipe library.

#### 14. Sustainability Dashboard
- Show how much food waste was reduced over time.
- Track cost savings and environmental impact from optimization features.
- Help the institute present sustainability outcomes in reports and presentations.
- Surface trends by week, month, and semester.
- Make sustainability visible to students to encourage responsible dining behavior.

#### 15. Carbon Or Waste-Saved Tracking
- Convert waste reduction into measurable saved kilograms and estimated carbon impact.
- Present simple impact counters that students and staff can understand quickly.
- Use the data in reports, dashboards, and awareness campaigns.
- Allow comparison across menus, months, or incentive campaigns.
- Support sustainability goals and institutional reporting.

#### 16. Smart Suggestions For Healthier Dishes
- Recommend healthier menu swaps based on calories, oil, protein, and user preferences.
- Highlight balanced alternatives for students who want lighter meals.
- Combine health advice with allergen and diet rules.
- Let admins tag recipes as healthy, balanced, high-protein, or low-calorie.
- Use the feature to support wellness-focused dining.

#### 17. Multi-Mess Support
- Support more than one canteen, hostel mess, or dining location.
- Allow each branch to have its own menu, inventory, attendance, and analytics.
- Compare performance across branches from one admin dashboard.
- Route students to their assigned mess automatically.
- Scale the same app across campus without redesigning the system.

## Chatbot Plan
- Add a built-in chatbot for students, admins, and kitchen staff.
- Make it available on web and mobile as a floating helper or dedicated support screen.
- Connect it to mess data, FAQs, notifications, menu details, and policy rules.
- Keep the first chatbot version focused on assistance, then expand it into a smart operations assistant.

### Chatbot Release Phases
- Phase 1: FAQ chatbot for common queries like menu, timings, leave rules, QR pass, and complaints.
- Phase 2: Context-aware assistant that can read user role, current menu, attendance, and notifications.
- Phase 3: AI operations assistant that can summarize trends, recommend actions, and draft responses.
- Phase 4: Voice-enabled and multilingual assistant for broader accessibility.

### AI Chatbot Functionalities
- Answer questions about today’s menu, tomorrow’s menu, and weekly meal plans.
- Explain calories, protein, allergens, and dietary suitability of dishes.
- Help students generate or retrieve their QR pass.
- Explain how to submit leave requests and what the leave status means.
- Help students report complaints or feedback step by step.
- Show live crowd level and recommend the best dining window.
- Suggest healthier meal choices based on profile preferences.
- Recommend meals for vegetarian, vegan, high-protein, or allergy-safe diets.
- Notify users about special meals, rewards, and happy-hour slots.
- Summarize admin alerts like inventory shortages, crowd spikes, or abnormal attendance.
- Draft menu suggestions for upcoming days based on weather and academic events.
- Summarize feedback themes from students.
- Guide staff through QR validation, override steps, and attendance handling.
- Explain what a heatmap zone means and where congestion is happening.
- Help users search historical records such as past menus, past complaints, or prior reward activity.
- Support multilingual natural-language queries for easier adoption.
- Offer voice-to-text input for quicker interaction on mobile.

### Chatbot Intelligence Inputs
- User profile and role.
- Menu data and nutrition data.
- Attendance and QR history.
- Feedback and complaint records.
- Crowd and occupancy data.
- Inventory and stock alerts.
- Weather data.
- Academic calendar events.
- Reward and incentive rules.
- Admin configuration and campus policies.

### Chatbot Guardrails
- Restrict admin-only answers to authenticated staff.
- Avoid giving unsafe food advice for allergies or medical conditions.
- Show a clear fallback response when the bot is unsure.
- Escalate complex complaints to a human admin.
- Log sensitive or repeated queries for improvement.

### Chatbot UI Ideas
- Floating assistant button on mobile and web.
- Quick-action chips for common tasks like menu, leave, QR pass, and complaint.
- Conversation history with searchable threads.
- Role-based welcome prompts.
- Rich cards for menu items, rewards, and alerts.
- Inline action buttons such as Open Menu, Submit Leave, or View Notification.

## AI Research And Advancements We Can Use
This section lists the AI capabilities that can make the project stand out during evaluation. The goal is to show that SMMS is not only a management app, but also an applied-AI system for prediction, automation, personalization, and decision support.

### 1. Time-Series Forecasting
- Predict mess footfall by meal slot, day, week, and event.
- Forecast food demand, queue length, and expected attendance.
- Use models such as Prophet, ARIMA, XGBoost, LSTM, or Temporal Fusion Transformer.
- Show confidence intervals so the panel sees uncertainty handling, not just raw prediction.
- Compare predicted vs actual demand to prove model improvement over time.

### 2. Recommendation Systems
- Recommend meals based on taste history, ratings, diet preferences, and allergy constraints.
- Suggest healthier alternatives, off-peak dining windows, and reward campaigns.
- Use collaborative filtering, content-based filtering, or hybrid recommenders.
- Personalize menu cards for each student without changing the core menu for everyone.
- Extend recommendations to chefs for ingredient rotation and menu planning.

### 3. Natural Language Processing And LLMs
- Power the chatbot for menu queries, leave questions, complaints, and policy help.
- Summarize feedback into themes, priorities, and action items.
- Draft notices, menu explanations, and admin replies automatically.
- Use retrieval-augmented generation so the chatbot answers from actual mess data.
- Support prompt-based summarization of analytics for management reports.

### 4. Computer Vision And OCR
- Scan student ID cards before plate issuance.
- Read QR codes at the counter.
- Support camera-based validation if needed in the future.
- Detect face, card, or plate movement only if the institute later approves it.
- Use OCR for extracting text from student cards, printed tokens, or receipts.

### 5. Fraud Detection And Anomaly Detection
- Flag duplicate scans, suspicious attendance patterns, and repeated override use.
- Detect unusual crowd spikes that do not match normal trends.
- Detect abnormal inventory usage or unexpected waste.
- Use anomaly scoring to help admins review suspicious activity faster.
- Keep audit logs so every AI decision can be explained later.

### 6. Crowd Intelligence And Spatial Analytics
- Estimate congestion from scan density and zone-level activity.
- Build a crowd heatmap for the mess floor.
- Predict which serving counter will become overloaded next.
- Use spatial clustering to locate bottlenecks.
- Present the result visually so it looks like a real operations intelligence system.

### 7. Optimization And Decision Support
- Optimize meal portions, staff allocation, and serving schedules.
- Suggest batch sizes to reduce waste and keep items available.
- Optimize incentive slots to move students away from peak periods.
- Use rule-based optimization, linear programming, or heuristic search.
- Combine AI predictions with operational constraints so recommendations are practical.

### 8. Digital Twin And Simulation
- Simulate the mess for the next meal or the next week.
- Test menu changes, weather changes, holiday effects, and reward campaigns.
- Show what happens if demand increases or staff count drops.
- Create what-if scenarios for the panel to demonstrate advanced research thinking.
- Compare scenarios visually before applying them in the live system.

### 9. Demand Segmentation And Clustering
- Group students by meal habits, dining frequency, preference patterns, and response to incentives.
- Identify clusters such as regular diners, off-peak diners, diet-sensitive users, and high-feedback users.
- Use the groups to target reward campaigns and menu planning.
- Analyze ingredient fatigue and dish popularity by segment.
- Make the app smarter without treating all students the same.

### 10. Multimodal AI
- Combine text, image, QR, and possibly voice interactions.
- Let users scan, speak, or type depending on the situation.
- Support richer assistant flows like showing a dish card plus explanation.
- Prepare the system for future camera-based or voice-based interfaces.
- Demonstrate that the platform can evolve into a smart campus assistant.

### 11. Speech AI
- Add voice input for the chatbot.
- Add text-to-speech for accessibility and hands-free use.
- Help visually impaired users or staff working in the kitchen.
- Support quick command-style interactions on mobile.
- Make the assistant feel more advanced and usable in real-world settings.

### 12. Translation And Multilingual AI
- Support multiple languages for students and staff.
- Translate chatbot responses, notices, and menu descriptions.
- Make the app useful for a diverse campus population.
- Use this to improve accessibility and adoption.

### 13. Explainable AI
- Show why a meal or incentive was recommended.
- Explain why a day is predicted to be crowded.
- Explain why a QR attempt was blocked.
- Present simple reasons such as weather, attendance history, or event calendar.
- This is important for trust when presenting to the panel.

### 14. RAG And Vector Search
- Use retrieval-augmented generation so the chatbot responds from mess data, FAQs, policies, menus, and reports.
- Store menus, rules, complaints, and analytics summaries in a searchable vector index.
- Keep answers grounded in the actual app data instead of generic model output.
- Improve accuracy and reduce hallucination risk.

### 15. Generative AI For Operations
- Auto-draft announcements, menu updates, complaint replies, and weekly summaries.
- Generate synthetic examples for testing dashboards and chatbot flows.
- Produce report narratives from charts and analytics.
- Draft alternative menu plans based on ingredient availability.
- This makes the system feel more complete during demonstration.

### 16. Privacy-Preserving And Responsible AI
- Use role-based access so the AI only shows information the user is allowed to see.
- Avoid exposing personal or sensitive student data in chatbot responses.
- Keep model outputs logged for auditing and debugging.
- Prefer on-device or backend-isolated handling for sensitive steps where possible.
- Mentioning responsible AI helps the project feel academically strong and production-ready.

### 17. Suggested AI Models And Tools
- Forecasting: Prophet, ARIMA, XGBoost, LightGBM, LSTM.
- Recommendation: collaborative filtering, content-based filtering, hybrid ranking.
- NLP and chatbot: LLM with RAG, intent classification, summarization.
- Vision: OCR and QR scanning models, optional future object detection.
- Clustering: K-Means, DBSCAN, hierarchical clustering.
- Anomaly detection: Isolation Forest, Autoencoders, statistical thresholds.
- Optimization: linear programming, greedy heuristics, constraint-based search.

### 18. How To Present The AI Story To The Panel
- Start with the problem: messy queues, waste, low visibility, and manual planning.
- Show that the project uses prediction, recommendation, conversation, and optimization.
- Explain that the chatbot is not isolated; it is connected to menus, attendance, and analytics.
- Emphasize that the system uses real mess data for forecasting and decision support.
- Highlight that the AI features improve operations, sustainability, and student experience together.

### D. Flutter Web And Platform Features
- Responsive layout for mobile, tablet, and desktop.
- Browser-friendly navigation and keyboard support.
- PWA installation for web users.
- Offline caching for menu and QR data.
- Cross-platform notifications.
- Shared components for student and admin portals.
- Better desktop side navigation for admin workflows.
- Accessibility support for contrast, font scaling, and screen readers.

### E. Operational And Governance Features
- Role-based access control.
- Audit logs for edits and approvals.
- Data backup and restore.
- Complaint escalation workflow.
- Staff shift planning.
- Guest meal handling.
- Payment integration if fee collection is needed later.
- Multi-language support.
- Settings for campus-specific rules.

## Suggested Release Phases

### Phase 1: MVP
- Login and role-based routing.
- Student dashboard.
- QR pass and attendance.
- Menu viewing.
- Leave management.
- Feedback submission.
- Admin dashboard.
- Menu management.
- Inventory basics.
- Notifications.

### Phase 2: Operations Upgrade
- Analytics.
- Feedback inbox.
- User management.
- Kitchen display.
- Export reports.
- Reward system.
- Profile preferences.
- Allergen and nutrition tagging.

### Phase 3: Smart Automation
- Crowd heatmap.
- Demand forecasting.
- Surge management.
- Simulation.
- Weather-aware planning.
- Leftover routing.
- A/B testing.

### Phase 4: Scale And Quality
- Multi-mess support.
- PWA hardening.
- Offline mode.
- Accessibility polish.
- Multilingual support.
- Security and audit improvements.

## Questions For Update Review
- Which features are mandatory for the first release? - 
- What roles should be supported on day one?
- Should the app use university SSO or a custom login first?
- Do we want the website to be a full portal or only a companion dashboard?
- Should QR codes be static, rotating, or time-limited?
- Who approves leave requests, if anyone?
- Should feedback be anonymous?
- Should dish voting be limited to eligible students only?
- What data source will provide live occupancy?
- How should inventory be updated?
- Do we need payment integration in the first version?
- Should rewards be points, rebates, or both?
- Do we need guest meal support?
- Which analytics matter most to management?
- What reports should be exportable?
- How much history should the system store?
- Should the app support multiple mess branches?
- What are the accessibility requirements?
- Do we need offline support on web?
- What is the preferred deployment target for the website?

## Comment And Update Log
Use this section for future revisions.

| Date | Area | Change Requested | Comment | Status |
| --- | --- | --- | --- | --- |
|  |  |  |  | Pending |
|  |  |  |  | Pending |
|  |  |  |  | Pending |

## Notes For Future Updates
- Keep the document aligned with the Flutter codebase.
- Move completed items from this plan into implementation notes.
- Add new features only after confirming scope and priority.
- Review web deployment requirements before UI implementation.
- Update this file whenever the PPT or stakeholder feedback changes.