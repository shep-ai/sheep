# Image Description

The image is a screenshot of the **Shep** application's user interface, showing a feature development workflow dashboard.

---

## Layout

The interface is divided into two visual columns against a light grey dotted-grid background:

- **Left column** — two repository cards
- **Right column** — three feature/task cards

Dashed lines connect each repository card to its associated feature cards, visually representing which features belong to which repository.

---

## Repository Cards (Left)

Each repository card is a rounded white pill-shaped element displaying:

- A GitHub cat icon
- The repository name
- Four action icons: code view (`</>`), terminal (`>_`), folder, and plus (`+`)

**Repositories shown:**
1. **cli** — connected to two feature cards (Dynamic LLM Model Selection, Attachment Support)
2. **sheep** — connected to one feature card (Arctic Detector)

---

## Feature Cards (Right)

Each card shows the feature's status label, title, description excerpt, UUID, and a call-to-action button.

### 1. Dynamic LLM Model Selection for Ag...
- **Status:** `COMPLETED`
- **Description:** Enable agent providers to expose their suppor...
- **UUID:** `745ffb22-9a27-4dc6-aae8-7bfe08f01cdf`
- **Action:** `Completed` (green badge with checkmark icon)

### 2. Attachment Support for UI and CLI
- **Status:** `IMPLEMENTATION`
- **Description:** Enable file and image attachment support acr...
- **UUID:** `8ea64770-8caf-4f1a-94ee-56d97f33e1c4`
- **Action:** `Review Technical Planning` (purple badge with wrench icon)

### 3. Arctic Detector
- **Status:** `REVIEW`
- **Description:** Wire up a arctic detector to the application
- **UUID:** `7a92475a-93e2-4a03-a62c-8b2a83f960e8`
- **Action:** `Review Merge Request` (green badge with branch icon)

---

## Summary

The screenshot illustrates the Shep workflow tool's main view: repositories on the left are linked via dashed connector lines to their in-progress or completed features on the right. Each feature card captures its current phase in the development lifecycle — from implementation planning through code review to completion.
