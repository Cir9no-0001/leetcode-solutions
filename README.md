# LeetCode Solutions Sync

This repository automatically syncs my accepted LeetCode submissions into GitHub using GitHub Actions.

GitHub Actions workflow was designed and made by me, and edited by ChatGPT and Gemini

Each solved problem is saved as a `.sql` file and organized by difficulty.

## How it works

A GitHub Actions workflow runs automatically and:

- Fetches recently accepted LeetCode submissions
- Retrieves problem metadata (title, slug, difficulty)
- Fetches the latest accepted submission code
- Organizes solutions into folders by difficulty
- Commits and pushes updates to this repository

## Folder structure

leetcode/
- easy/
- medium/
- hard/

Each file follows this format:

-- Problem Title
-- https://leetcode.com/problems/problem-slug/

-- SQL solution

## Setup

To run this project, you need to configure GitHub Secrets:

- LEETCODE_USERNAME: your LeetCode username
- LEETCODE_SESSION: your LeetCode session cookie

These are required to access your accepted submissions.

## GitHub Actions

The sync runs automatically via:

- Scheduled workflow (daily)
- Manual trigger via workflow_dispatch

Workflow file is located at:
.github/workflows/sync.yml

## Notes

- LeetCode does not provide a fully stable public API for submission code retrieval.
- This project relies on internal GraphQL endpoints, which may occasionally change.
- Difficulty is fetched dynamically and used for folder organization.

## Purpose

This repository is used for:

- Tracking solved problems
- Maintaining a structured coding log
- Building a public portfolio of SQL solutions
- Automating GitHub activity from LeetCode progress

## Future improvements

- Support for multiple programming languages
- Duplicate detection
- Stats dashboard for problem breakdown
- Tags per problem type
