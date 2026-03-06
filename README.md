# InfoSec Bharat 🇮🇳

InfoSec Bharat is an open-source, community-driven directory mapping cybersecurity conferences, meetups, workshops, and hacker events across India. Built by the community, for the community.

## Overview

The Indian infosec community is vast but highly fragmented. Finding upcoming conferences or local meetups often involves searching through Twitter threads, LinkedIn posts, or private community groups. **InfoSec Bharat** centralizes this information into a single, comprehensive platform.

# Submitting Events to InfoSec Bharat via GitHub PR

Welcome to the InfoSec Bharat event submission guide! While you can submit events one by one using our website's interface, using our **YAML template via GitHub Pull Request (PR)** is the **recommended approach if you are submitting multiple events at once**. 

This method uses a GitOps pipeline that allows the InfoSec Bharat maintainers to review, approve, and merge your events quickly in bulk.

## Step 1: Get the YAML Template

You can find the required YAML template as [events_template.yaml](/events_template.yaml).
Here is the exact schema you need to follow:

```yaml
# InfoSec Bharat Event Submission Template
# Submit via PR to the maintainers

events:
  - name: "Your Conference Name 2025" # Event Name (required)
    description: "A brief description of your event (2-3 sentences)" # Event Description (required)
    start_date: "2026-04-12"  # YYYY-MM-DD format (required)
    end_date: "2026-04-13" # YYYY-MM-DD format (required)
    location: "Venue Name" # Venue/Location (required)
    city: "Mumbai"  # Bangalore, Mumbai, Delhi, Hyderabad, Online, etc (required)
    category: "Conference" # Conference, Meetup (required)
    event_type: "offline"  # offline, online, hybrid (required)
    website_url: "https://yourconference.com" # Website (required)
    event_socials: "https://x.com/yourconf" # Social Handle (optional)
    is_paid: true # Event is paid or free (optional)
    price_min: 1000  # INR, remove if free (optional)
    price_max: 5000  # INR, remove if free (optional)
    cfp_deadline: "2026-03-30"  # Optional, remove if no CFP (optional)
    organizer_name: "Hitesh Patra" # Submitted By (required)
    organizer_email: "hello@infosecbharat.com" # Submitted By (required)
    tags:         # Event tags (optional)
      - Conference
      - AppSec
      - Workshop

  # Add more events below following the exact same format
  - name: "Your Next Meetup"
    # ...
```

> [!IMPORTANT]
> Ensure all your events are correctly nested under the `events:` array. The schema requires all listed fields to exist. Remove optional fields like `price_min`, `price_max` or `cfp_deadline` completely from the block if they don't apply to an event (e.g. for free events).

## Step 2: Add Your Events

Create an `events.yaml` file on your machine and copy the template above into it. Fill in the details for all the events you want to submit. You can list as many as you need under the `events:` key.

## Step 3: Fork and Submit a Pull Request

1. **Fork this Repository**: Click **Fork** to create your own copy on your GitHub account.
2. **Commit Your changes**:
   - In your forked repository, upload your `events.yaml` file. 
   - You can also just create a publicly accessible GitHub Gist with your `events.yaml` file.
3. **Open a Pull Request** (if using the repo): Submit a PR from your fork's branch to the main InfoSec Bharat repository.

## Approval Process

Once your PR is submitted, our AI Agent Nakul handles the rest.
- Nakul will send a notification to the maintainer regarding the PR.
- Maintainers will review the submission. 
- Once the maintainers approve, PR will be merged and event will be listed on InfoSec Bharat.
- You will be notified once they are live!

> [!TIP]
> Bulk submitting events for an entire community or series of monthly meetups? Using the YAML GitOps method will save you and the maintainers significant time compared to individual UI submissions.